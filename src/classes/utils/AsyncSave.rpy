init python in JK:
    _constant = True

    import threading
    import io
    import sys
    import time
    from json import dumps as json_dumps

    class PendingAsyncSave(x52NonPicklable):
        def __init__(self, slotname):
            self.slotname = slotname
            # Stashed so retry flows (e.g. quicksave's overwrite-confirm) can reuse
            # the same raw pixels instead of grabbing a new (possibly dialog-obscured) frame.
            self.raw_screenshot = None
            self.error = None
            self._event = threading.Event()

        def wait(self, timeout=None):
            return self._event.wait(timeout)

        @property
        def is_done(self):
            return self._event.is_set()

        def _finish(self, error=None):
            self.error = error
            self._event.set()

    class AsyncSave(x52NonPicklable):
        # Safety-net bound for waiters (full disk, network extra_savedirs, etc).
        # A normal write is expected to finish well under a second.
        DEFAULT_WAIT_TIMEOUT = 10.0

        _UNSET = object()

        # Tri-state cache: None = not yet probed, True/False once known. Ren'Py
        # 6.99-7.x's draw.screenshot() requires (surftree, fullscreen_video); Ren'Py
        # 8's draw backends (gl/gl2/sw) dropped the fullscreen_video parameter.
        # Probed once per process since the draw backend never changes mid-run.
        _screenshot_wants_fullscreen_video = None

        @staticmethod
        def capture_raw_screenshot():
            interface = renpy.game.interface

            if not interface.started or interface.surftree is None:
                return None

            return AsyncSave._draw_screenshot(interface.surftree, interface.fullscreen_video)

        @staticmethod
        def _draw_screenshot(surftree, fullscreen_video):
            draw = renpy.display.draw

            if AsyncSave._screenshot_wants_fullscreen_video is None:
                try:
                    surf = draw.screenshot(surftree, fullscreen_video)
                    AsyncSave._screenshot_wants_fullscreen_video = True
                    return surf
                except TypeError:
                    AsyncSave._screenshot_wants_fullscreen_video = False

            if AsyncSave._screenshot_wants_fullscreen_video:
                return draw.screenshot(surftree, fullscreen_video)

            return draw.screenshot(surftree)

        @staticmethod
        def begin(location, slotname, extra_info="", raw_screenshot=_UNSET):
            """
            Must be called on the thread that's currently handling the interaction
            (i.e. wherever a renpy.save() call would previously have been made).

            Synchronously captures the raw screenshot pixels and freezes/pickles the
            current game state (fast, in-memory - this is what must reflect the exact
            calling instant), then hands the slow, state-independent tail (PNG encode,
            zip write, replication across every active save location) to a background
            thread. Returns a PendingAsyncSave immediately; never raises - synchronous
            failures are reported via the returned handle's `.error`, already done.
            """

            pending = PendingAsyncSave(slotname)
            pending.raw_screenshot = (
                AsyncSave.capture_raw_screenshot() if raw_screenshot is AsyncSave._UNSET else raw_screenshot
            )

            try:
                roots = renpy.game.log.freeze(None)

                if renpy.config.save_dump:
                    # Optional debug convenience (renpy.loadsave.save_dump on Ren'Py
                    # 6.99-7.x, replaced by dump_paths with a different signature on
                    # Ren'Py 8+) - never let a failure here fail the actual save.
                    try:
                        renpy.loadsave.save_dump(roots, renpy.game.log)
                    except Exception:
                        pass

                logf = io.BytesIO()
                try:
                    renpy.loadsave.dump((roots, renpy.game.log), logf)
                except Exception:
                    t, e, tb = sys.exc_info()

                    try:
                        bad = renpy.loadsave.find_bad_reduction(roots, renpy.game.log)
                    except Exception:
                        bad = None

                    if bad is not None and e.args:
                        e.args = (e.args[0] + ' (perhaps {})'.format(bad),) + e.args[1:]

                    raise

                # Matches native renpy.loadsave.save()'s base dict for the running
                # engine (Ren'Py 8+ includes _renpy_version/_version/_game_runtime/
                # _ctime; all four are available back through Ren'Py 7) so
                # save_json_callbacks - and anything reading these fields back out
                # of the save later - see the same shape a native save would produce.
                json_dict = {
                    "_save_name": extra_info,
                    "_renpy_version": list(renpy.version_tuple),
                    "_version": renpy.config.version,
                    "_game_runtime": renpy.exports.get_game_runtime(),
                    "_ctime": time.time(),
                }

                for callback in renpy.config.save_json_callbacks:
                    callback(json_dict)

                json_str = json_dumps(json_dict)
            except Exception as e:
                print("[JK] AsyncSave: synchronous capture for slot '{}' failed:".format(slotname), e)
                pending._finish(error=e)
                return pending

            log_bytes = logf.getvalue()
            raw_screenshot = pending.raw_screenshot

            def worker():
                try:
                    screenshot_bytes = AsyncSave._encode_screenshot(raw_screenshot)
                    record = renpy.loadsave.SaveRecord(screenshot_bytes, extra_info, json_str, log_bytes)

                    with disk_lock:
                        location.save(slotname, record)
                        location.scan()
                        renpy.loadsave.clear_slot(slotname)

                    pending._finish(error=None)
                except Exception as e:
                    print("[JK] AsyncSave: background write to slot '{}' failed:".format(slotname))
                    import traceback
                    traceback.print_exc()
                    pending._finish(error=e)

            renpy.invoke_in_thread(worker)
            return pending

        @staticmethod
        def _encode_screenshot(raw_surface):
            if raw_surface is None:
                return b""

            scale = (renpy.config.thumbnail_width, renpy.config.thumbnail_height)
            surf = renpy.display.scale.smoothscale(raw_surface, scale)
            renpy.display.render.mutated_surface(surf)

            sio = io.BytesIO()
            renpy.display.module.save_png(surf, sio, 0)
            return sio.getvalue()

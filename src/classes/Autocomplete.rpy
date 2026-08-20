init python in JK:
    _constant = True

    # Extension point for games whose choice screen isn't Ren'Py's default "choice" screen
    # (see Utils.is_displaying_choices()/game_specific_processors for other examples of that
    # kind of divergence). Each callback is called with no arguments while a menu is being
    # displayed and should return a list of (label_text, action) tuples for the currently
    # shown choices, or None/[] if it doesn't apply to the current screen.
    autocomplete_get_current_choices_callbacks = []

    class AutocompleteClass(x52NonPicklable):
        ICON_UPCOMING = "\ue5c5"
        ICON_PAUSE = "\ue034"
        ICON_RESUME = "\ue037"
        ICON_STOP = "\ue99a"

        # At 0.2s/tick (see the bar's timer), 15 ticks is a 3 second grace period before a
        # motionless node is treated as an unskippable interruption rather than a transient
        # hiccup (e.g. a transition/frame timing quirk landing on the same node twice).
        STUCK_TICK_THRESHOLD = 15

        def __init__(self):
            self.active = False
            self.paused = False
            self.loading = False

            self.playthrough = None
            self.choices = []
            self.cursor = 0

            self.last_node = None
            self.pause_reason = None
            self.previous_skip_unseen = None
            self.tick_count = 0
            self.stuck_ticks = 0

        def __log(self, message):
            if Settings.debugEnabled:
                print("[JK] Autocomplete: {}".format(message))

        def start(self, playthrough):
            if self.active:
                return

            self.playthrough = playthrough
            self.choices = []
            self.cursor = 0
            self.active = True
            self.paused = False
            self.loading = True
            self.last_node = None
            self.pause_reason = None
            self.previous_skip_unseen = renpy.game.preferences.skip_unseen
            self.tick_count = 0
            self.stuck_ticks = 0

            self.__log("start() playthrough='{}' (id={})".format(playthrough.name, playthrough.id))

            renpy.show_screen("JK_AutocompleteBar")
            renpy.restart_interaction()

            renpy.invoke_in_thread(self.__load_choices)

        def __load_choices(self):
            try:
                instance = SaveSystem.get_or_create_playthrough_save_instance(self.playthrough)
                instance.location.scan()

                # Not Utils.get_sorted_saves() - that lists slots in the globally *active*
                # location, which is only the same as instance.location when self.playthrough
                # happens to be the active playthrough. list_including_inactive() lists slots
                # that actually belong to this specific (possibly inactive) location instead.
                slots = Utils.sort_saves(instance.location.list_including_inactive())

                self.__log("__load_choices() found {} save slot(s): {}".format(len(slots), slots))

                # Likewise, MultiLocation.json() (the base Ren'Py implementation) resolves
                # through newest(), which only looks at active_locations() - always None for
                # a non-active playthrough. save_json(..., include_inactive=True) is JK's own
                # MultiLocation method that looks the slot up regardless of active state.
                choices = []
                for slot in slots:
                    slot_json = instance.location.save_json(slot, include_inactive=True)
                    text = slot_json.get("_JK_choice", None) if slot_json else None

                    if text:
                        choices.append(text)

                self.choices = choices

                self.__log("__load_choices() loaded {} choice(s): {}".format(len(choices), choices))
            except Exception as e:
                print("[JK] Autocomplete: failed to load choices - {}".format(e))
                self.choices = []
            finally:
                self.loading = False

                self.__engage_skip()

                renpy.restart_interaction()

        def tick(self):
            if not self.active or self.paused or self.loading:
                return None

            self.tick_count += 1

            # A heartbeat, not a trace of every tick (which would flood log.txt at 5/sec) -
            # tick #1 confirms the bar's timer is actually reaching the engine at all, and the
            # periodic follow-ups confirm it's still alive during a long skip run.
            if self.tick_count == 1 or self.tick_count % 25 == 0:
                self.__log("tick #{} (skipping={}, cursor={}/{})".format(self.tick_count, renpy.config.skipping, self.cursor, len(self.choices)))

            try:
                return self.__tick()
            except Exception as e:
                print("[JK] Autocomplete: tick failed - {}".format(e))
                self.pause("Autocomplete hit an error - see log.txt.")
                return None

        def __tick(self):
            current = self.__current_location()

            # Checked unconditionally, every tick - NOT gated behind "config.skipping just
            # turned itself off". That was this method's original (wrong) premise: it assumed
            # native skip always halts at a menu via choice_for_skipping(), but that function
            # only clears config.skipping when the player's "Skip After Choices" preference is
            # off. With it on, config.skipping stays "fast" straight through a menu - that
            # preference only controls whether skip PERSISTS AFTER a choice is made, not
            # whether the menu interaction itself blocks - so waiting for skipping to go falsy
            # could sit at an already-reached, already-blocking menu forever.
            if Utils.is_displaying_choices():
                self.__log("at a menu: {}".format(self.__describe_location(current)))

                result = self.__try_resolve_menu()

                if result is not None:
                    self.last_node = None
                    self.stuck_ticks = 0

                    # That was the last recorded choice - there's nothing left to replay, so
                    # stop fast-skipping into whatever unrecorded content comes next instead
                    # of blindly continuing until something eventually stops it. pause()
                    # already disengages skip and restores skip_unseen.
                    if self.cursor >= len(self.choices):
                        self.pause("Finished replaying all recorded choices.")
                    else:
                        self.__engage_skip()

                    return result

                self.pause("No remaining choice in the list matches the current menu.")
                return None

            # The player has stepped away to the save/load screen (reachable from the
            # sidepanel, which is how autocomplete itself gets started) - Ren'Py's own
            # _enter_menu() already clears config.skipping on the way in, and the underlying
            # game genuinely can't advance while it's up, but this isn't an "interruption"
            # needing manual resolution the way a minigame/hard pause is. Wait quietly for as
            # long as they're there instead of counting it toward "stuck".
            if Utils.is_save_load_screen():
                self.stuck_ticks = 0
                self.last_node = current
                return None

            # Also checked unconditionally - a hard pause (renpy.pause(..., hard=True)), a
            # custom minigame/input screen, or anything else that doesn't consult
            # config.skipping at all would otherwise leave autocomplete reporting
            # "skipping=fast" forever while nothing actually moves.
            if self.last_node is not None and current == self.last_node:
                self.stuck_ticks += 1

                if self.stuck_ticks >= self.STUCK_TICK_THRESHOLD:
                    self.__log("stuck at {} for {} ticks - pausing".format(self.__describe_location(current), self.stuck_ticks))
                    self.pause("Autocomplete hit something it can't skip through - resolve it manually, then press Resume.")
                    return None
            else:
                self.stuck_ticks = 0

            self.last_node = current
            self.__engage_skip()

            return None

        def __current_location(self):
            try:
                return renpy.game.context().current
            except:
                return None

        # renpy.game.context().current is an opaque key into renpy.game.script.namemap, not
        # a directly human-readable location - this resolves it the same way
        # renpy.exports.get_filename_line() and Utils.is_displaying_choices() do (namemap
        # lookup), for log messages, and also reports the actual AST node type so it's
        # possible to tell from the log alone whether a "stuck" point is really a Menu node
        # Utils.is_displaying_choices() should have caught, or something else entirely (a
        # custom minigame/input screen, a Python node, a hard pause, etc.).
        def __describe_location(self, current):
            try:
                node = renpy.game.script.namemap.get(current, None)
            except:
                node = None

            if node is None:
                return "{} (not found in namemap)".format(current)

            return "{}:{} ({})".format(node.filename, node.linenumber, type(node).__name__)

        # The screen's own item.caption is renpy.config.say_menu_text_filter's OUTPUT, not
        # the label as written - some games/mods (e.g. URM's jump-target preview) hook that
        # filter to decorate the on-screen text. The AST Menu node's own .items is the
        # original, undecorated label - the same "present node context" the choice statement
        # itself was compiled from - so read labels from there and only fall back to the
        # screen's (filtered) caption if the two disagree on how many choices are available
        # (e.g. a `menu ... set` clause pruning already-chosen options, which this doesn't
        # replicate).
        def __get_raw_menu_labels(self):
            try:
                menu_node = renpy.game.script.lookup(renpy.game.context().current)
            except:
                return None

            if not isinstance(menu_node, renpy.ast.Menu):
                return None

            labels = []
            for label, condition, block in menu_node.items:
                if block is None:
                    continue

                try:
                    if not renpy.python.py_eval(condition):
                        continue
                except:
                    return None

                labels.append(label)

            return labels

        def __get_live_choices(self):
            screen = renpy.get_screen("choice")

            if screen is not None and "items" in screen.scope:
                screen_items = screen.scope["items"]
                actions = [getattr(item, "action", None) for item in screen_items]

                raw_labels = self.__get_raw_menu_labels()

                if raw_labels is not None and len(raw_labels) == len(actions):
                    return list(zip(raw_labels, actions))

                self.__log("raw AST label count didn't match the 'choice' screen's item count (raw={}, screen={}) - falling back to the screen's own (possibly filtered) caption".format(
                    None if raw_labels is None else len(raw_labels), len(actions)))

                live = []
                for item in screen_items:
                    live.append((getattr(item, "caption", None), getattr(item, "action", None)))
                return live

            self.__log("no 'choice' screen with an 'items' scope var is currently shown - trying {} autocomplete_get_current_choices_callbacks".format(len(autocomplete_get_current_choices_callbacks)))

            for callback in autocomplete_get_current_choices_callbacks:
                result = callback()
                if result:
                    return result

            self.__log("no live choices could be extracted for this menu - if this game uses a custom choice screen, register a callback in JK.api.callbacks.autocomplete_get_current_choices_callbacks")
            return []

        # Searches self.choices forward from the cursor - never wrapping back to the start -
        # for the first entry that matches one of the choices currently on screen. Runs the
        # matched choice's real action (renpy.display.behavior.run, same dispatcher a real
        # click goes through) so autosave-on-choice and the injects/ui.rpy ChoiceReturn hook
        # still fire normally. The returned value is handed back up through TickAction, and
        # since the Timer displayable's own event() returns whatever its action returns, this
        # ends the current interaction exactly as if the player had clicked it.
        def __try_resolve_menu(self):
            raw_live_choices = self.__get_live_choices()

            live = []
            for caption, action in raw_live_choices:
                if caption is None or action is None:
                    continue

                text = Utils.derive_choice_text(caption)
                for callback in before_storing_choice_text_callbacks:
                    text = callback(text, text, action) or text

                live.append((Utils.normalize_choice_text(text), action))

            self.__log("live choices on screen (raw): {}".format([caption for caption, action in raw_live_choices]))
            self.__log("live choices on screen (normalized): {}".format([normalized for normalized, action in live]))

            if not live:
                return None

            # A menu with only one real option isn't a decision a player actually made - it's
            # never recorded as a choice in the first place (see Settings.autosaveOnSingletonChoice),
            # so there's nothing to look up here either. Just take it, same as a player would.
            if len(live) == 1:
                self.__log("only one live choice - taking it automatically without consulting the recorded list")
                return renpy.display.behavior.run(live[0][1])

            remaining = self.choices[self.cursor:]
            self.__log("searching recorded choices from cursor={}: raw={} normalized={}".format(
                self.cursor, remaining, [Utils.normalize_choice_text(c) for c in remaining]))

            for i in range(self.cursor, len(self.choices)):
                target = Utils.normalize_choice_text(self.choices[i])

                if not target:
                    continue

                for normalized, action in live:
                    if normalized == target:
                        self.__log("matched recorded choice #{}: {!r} - advancing cursor to {}".format(i, self.choices[i], i + 1))
                        self.cursor = i + 1
                        return renpy.display.behavior.run(action)

            self.__log("no recorded choice (from cursor={} onward) matches any live choice on screen".format(self.cursor))
            return None

        def __engage_skip(self):
            renpy.game.preferences.skip_unseen = True
            renpy.config.skipping = "fast"

        def pause(self, reason=None):
            if not self.active or self.paused:
                return

            self.__log("pausing at cursor={}: {}".format(self.cursor, reason))

            self.paused = True
            self.pause_reason = reason
            renpy.config.skipping = None

            if self.previous_skip_unseen is not None:
                renpy.game.preferences.skip_unseen = self.previous_skip_unseen

            renpy.restart_interaction()

        def resume(self):
            if not self.active or not self.paused:
                return

            self.__log("resuming at cursor={}".format(self.cursor))

            self.paused = False
            self.pause_reason = None
            self.last_node = None
            self.stuck_ticks = 0

            self.__engage_skip()

            renpy.restart_interaction()

        def stop(self):
            if not self.active:
                return

            self.__log("stopping at cursor={}".format(self.cursor))

            self.active = False
            self.paused = False
            self.loading = False
            self.pause_reason = None

            renpy.config.skipping = None

            if self.previous_skip_unseen is not None:
                renpy.game.preferences.skip_unseen = self.previous_skip_unseen
                self.previous_skip_unseen = None

            renpy.hide_screen("JK_AutocompleteBar")
            renpy.restart_interaction()

        def set_cursor(self, index):
            self.cursor = max(0, min(index, len(self.choices)))
            renpy.restart_interaction()

        def move_entry(self, index, delta):
            new_index = index + delta

            if 0 <= index < len(self.choices) and 0 <= new_index < len(self.choices):
                self.choices[index], self.choices[new_index] = self.choices[new_index], self.choices[index]
                renpy.restart_interaction()

        def edit_entry(self, index, text):
            if 0 <= index < len(self.choices) and text:
                self.choices[index] = text
                renpy.restart_interaction()

        def delete_entry(self, index):
            if 0 <= index < len(self.choices):
                del self.choices[index]

                if self.cursor > index:
                    self.cursor -= 1

                renpy.restart_interaction()

        def insert_entry(self, text, index=None):
            if not text:
                return

            if index is None:
                index = len(self.choices)

            self.choices.insert(index, text)
            renpy.restart_interaction()

        class StartAutocompleteAction(renpy.ui.Action):
            def __init__(self, playthrough):
                self.playthrough = playthrough

            def __call__(self):
                Autocomplete.start(self.playthrough)

        class TickAction(renpy.ui.Action):
            def __call__(self):
                return Autocomplete.tick()

        class PauseAction(renpy.ui.Action):
            def __call__(self):
                Autocomplete.pause()

        class ResumeAction(renpy.ui.Action):
            def __call__(self):
                Autocomplete.resume()

        class StopAction(renpy.ui.Action):
            def __call__(self):
                Autocomplete.stop()

        class SetCursorAction(renpy.ui.Action):
            def __init__(self, index):
                self.index = index

            def __call__(self):
                Autocomplete.set_cursor(self.index)

        class MoveEntryAction(renpy.ui.Action):
            def __init__(self, index, delta):
                self.index = index
                self.delta = delta

            def __call__(self):
                Autocomplete.move_entry(self.index, self.delta)

        class EditEntryAction(renpy.ui.Action):
            def __init__(self, index, text):
                self.index = index
                self.text = text

            def __call__(self):
                Autocomplete.edit_entry(self.index, self.text)

        class DeleteEntryAction(renpy.ui.Action):
            def __init__(self, index):
                self.index = index

            def __call__(self):
                Autocomplete.delete_entry(self.index)

        class InsertEntryAction(renpy.ui.Action):
            def __init__(self, text, index=None):
                self.text = text
                self.index = index

            def __call__(self):
                Autocomplete.insert_entry(self.text, self.index)

init python in JK:
    _constant = True
    import threading
    import time
    import os

    class MoveCopySavesViewModel(x52NonPicklable):
        def __init__(self, source_playthrough, destination_playthrough):
            self.source_playthrough = source_playthrough
            self.destination_playthrough = destination_playthrough

            self.processing = False
            self.saves_to_process = []
            self.processed = 0
            self.overwrite_all = False
            self.skip_all = False
            self.mode = "COPY"  # "COPY"|"MOVE"
            self.stage = "COPY"  # "COPY"|"CLEANUP"
            self.error = None
            self.success = None

            self.source_instance = None
            self.destination_instance = None

            self.source_saves = []
            self.destination_saves = []
            self.skipped = []

            self.loadSaves()
            self.save_thread = None  # To track the active copy thread
            self.cleanup_thread = None  # To track the cleanup thread
            self.skip_conflicts_thread = None  # To handle skip conflicts in background
            self._last_progress_notify = 0.0

            self.source_instance = SaveSystem.get_or_create_playthrough_save_instance(self.source_playthrough)
            if not self.source_instance:
                self.error = "Couldn't find the source location."
                self.processing = False
                renpy.restart_interaction()
                return

            self.destination_instance = SaveSystem.get_or_create_playthrough_save_instance(self.destination_playthrough)
            if not self.destination_instance:
                self.error = "Couldn't find the destination location."
                self.processing = False
                renpy.restart_interaction()
                return

        def loadSaves(self):
            self.source_saves = Utils.sort_saves(SaveSystem.list_all_saves_for_playthrough(self.source_playthrough))
            self.destination_saves = SaveSystem.list_all_saves_for_playthrough(self.destination_playthrough)

        def process_saves(self, saves, mode="COPY"):
            # saves is a list of (save, location) tuples; location is None for a per-save selection
            # (operate across every active location) or a specific source FileLocation for a per-directory one.
            self.mode = mode
            self.stage = "COPY"
            self.overwrite_all = False
            self.skip_all = False
            self.processing = True
            self.processed = 0
            self.saves_to_process = saves
            self.skipped = []
            self._last_progress_notify = 0.0

            renpy.restart_interaction()

            # Start processing saves with a background thread
            self.process_next_save()

        def get_matching_destination_location(self, source_location):
            if source_location is None:
                return None

            source_base = os.path.dirname(source_location.directory)

            for destination_location in self.destination_instance.location.locations:
                if os.path.dirname(destination_location.directory) == source_base:
                    return destination_location

            return None

        def process_next_save(self, force=False):
            force = self.overwrite_all or force

            if not self.processing:
                return

            # Check if all saves are processed
            if self.processed >= len(self.saves_to_process):
                # All saves processed
                if self.mode == "MOVE":
                    # Start cleanup in a separate thread
                    self.cleanup_thread = threading.Thread(target=self.process_cleanup)
                    self.cleanup_thread.daemon = True
                    self.cleanup_thread.start()
                else:
                    self.process_done()

                return

            save, location = self.saves_to_process[self.processed]
            destination_location = self.get_matching_destination_location(location)

            if location is not None and destination_location is None:
                self.error = "Couldn't find a save location in the destination playthrough matching \"" + location.directory + "\"."
                renpy.restart_interaction()
                self.process_stop()
                return

            # Check for conflicts and show confirmation screen if needed
            has_conflict = destination_location.mtime(save) is not None if destination_location else self.destination_instance.location.has_save(save, check_inactive=True)

            if has_conflict and not force:
                if self.skip_all:
                    self.skipped.append((save, location))
                    self.process_continue()
                    return

                renpy.show_screen("JK_MoveCopySavesOverwriteConfirm", save=save, source_location=location, destination_location=destination_location, view_model=self)
                time.sleep(0.1)
                renpy.restart_interaction()
                return

            # Create a thread to copy the save to avoid blocking the main thread
            self.save_thread = threading.Thread(target=self.copy_save_and_continue, args=(save, location, destination_location))
            self.save_thread.daemon = True
            self.save_thread.start()

        def copy_save_and_continue(self, save, location, destination_location):
            try:
                # Perform the save copy
                if location is not None:
                    location.copy_into_other_directory(save, save, destination_location.directory, scan=False)
                else:
                    self.source_instance.location.copy_save_into_other_multilocation(save, self.destination_instance.location, scan=False)

                self.process_continue()
            except Exception as e:
                print(e)
                self.error = "An error occurred while copying save \"" + save + "\":\n{color=[JK.Colors.error]}" + str(e) + "{/color}"
                renpy.restart_interaction()
                self.process_stop()

        def process_continue(self):
            # Update progress
            self.processed += 1
            self._notify_progress()

            # Continue with the next save, without waiting on the UI
            self.process_next_save()

        def _notify_progress(self, force=False):
            # Refresh the UI at most a few times a second instead of after every
            # single save, so the actual copy/cleanup work isn't throttled down
            # to the notification rate.
            now = time.time()
            if force or now - self._last_progress_notify >= 0.05:
                self._last_progress_notify = now
                renpy.restart_interaction()

        def process_skip_current_save(self, apply_to_all=False):
            self.skip_all = apply_to_all

            if apply_to_all:
                self.skipped.append(self.saves_to_process[self.processed])

                self.skip_conflicts_thread = threading.Thread(target=self.process_continue)
                self.skip_conflicts_thread.daemon = True
                self.skip_conflicts_thread.start()

                return

            self.process_continue()

        def process_overwrite_current_save(self, apply_to_all=False):
            self.overwrite_all = apply_to_all
            # Overwrite the current save
            self.process_next_save(force=True)
            renpy.restart_interaction()

        def process_overwrite_all_saves(self):
            # Overwrite all following saves
            self.overwrite_all = True
            self.process_next_save()
            renpy.restart_interaction()

        def process_stop(self, success=False):
            self.success = success
            self.processed = 0
            self.processing = False

            renpy.restart_interaction()

            if self.save_thread and self.save_thread.is_alive():
                self.save_thread.join()  # Wait for the thread to finish if stopping early

            if self.cleanup_thread and self.cleanup_thread.is_alive():
                self.cleanup_thread.join()  # Wait for cleanup to complete

            if self.skip_conflicts_thread and self.skip_conflicts_thread.is_alive():
                self.skip_conflicts_thread.join()  # Wait for skip to complete

            SaveSystem.multilocation.scan()

        def process_cleanup(self):
            self.stage = "CLEANUP"
            self.processed = 0
            self._last_progress_notify = 0.0

            self._notify_progress(force=True)

            save = None
            location = None
            try:
                for save, location in self.saves_to_process:
                    if not self.processing:
                        return

                    if (save, location) not in self.skipped:
                        if location is not None:
                            location.unlink_save(save, scan=False)
                        else:
                            self.source_instance.location.unlink_save(save, scan=False)

                    self.processed += 1

                    self._notify_progress()

                self.process_done()
            except Exception as e:
                print(e)
                self.error = "An error occurred while cleaning up save \"" + save + "\":\n{color=[JK.Colors.error]}" + str(e) + "{/color}"
                self.process_stop()

        def process_done(self):
            self.success = True
            self.processing = False

            SaveSystem.multilocation.scan()
            renpy.restart_interaction()

        class SelectDestinationAndStartAction(renpy.ui.Action):
            def __init__(self, source_playthrough, destination_playthrough, saves, mode):
                self.source_playthrough = source_playthrough
                self.destination_playthrough = destination_playthrough
                self.saves = saves
                self.mode = mode

            def __call__(self):
                cs = renpy.current_screen()
                if not cs:
                    return

                view_model = MoveCopySavesViewModel(self.source_playthrough, self.destination_playthrough)

                cs.scope["move_copy_destination_playthrough"] = self.destination_playthrough
                cs.scope["move_copy_view_model"] = view_model

                if not view_model.error:
                    view_model.process_saves(self.saves, mode=self.mode)

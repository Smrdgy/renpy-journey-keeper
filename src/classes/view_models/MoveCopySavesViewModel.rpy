init 1 python in SSSSS:
    _constant = True
    import threading
    import time

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

            self.source_instance = SaveSystem.getPlaythroughSaveInstance(self.source_playthrough.id)
            if not self.source_instance:
                self.error = "Couldn't find the source location."
                self.processing = False
                renpy.restart_interaction()
                return

            self.destination_instance = SaveSystem.getPlaythroughSaveInstance(self.destination_playthrough.id)
            if not self.destination_instance:
                self.error = "Couldn't find the destination location."
                self.processing = False
                renpy.restart_interaction()
                return

        def loadSaves(self):
            self.source_saves = Utils.sortSaves(SaveSystem.listAllSavesForPlaythrough(self.source_playthrough))
            self.destination_saves = SaveSystem.listAllSavesForPlaythrough(self.destination_playthrough)

        def process_saves(self, saves, mode="COPY"):
            self.mode = mode
            self.stage = "COPY"
            self.overwrite_all = False
            self.skip_all = False
            self.processing = True
            self.processed = 0
            self.saves_to_process = saves
            self.skipped = []

            renpy.restart_interaction()

            # Start processing saves with a background thread
            self.process_next_save()

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

            save = self.saves_to_process[self.processed]

            # Check for conflicts and show confirmation screen if needed
            if self.destination_instance.location.has_save(save, check_inactive=True) and not force:
                if self.skip_all:
                    self.skipped.append(save)
                    self.process_continue()
                    return

                renpy.show_screen("SSSSS_MoveCopySavesOverwriteConfirm", save=save, viewModel=self)
                time.sleep(0.1)
                renpy.restart_interaction()
                return

            # Create a thread to copy the save to avoid blocking the main thread
            self.save_thread = threading.Thread(target=self.copy_save_and_continue, args=(save,))
            self.save_thread.daemon = True
            self.save_thread.start()

        def copy_save_and_continue(self, save):
            try:
                # Perform the save copy
                self.source_instance.location.copy_save_into_other_multilocation(save, self.destination_instance.location, scan=False)

                self.process_continue()
            except Exception as e:
                print(e)
                self.error = "An error occurred while copying save \"" + save + "\":\n{color=[SSSSS.Colors.error]}" + str(e) + "{/color}"
                renpy.restart_interaction()
                self.process_stop()

        def process_continue(self):
            # Update progress and refresh the UI
            self.processed += 1
            renpy.restart_interaction()

            # Give time for the UI to update
            time.sleep(0.05)

            # Continue with the next save
            self.process_next_save()

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

            renpy.restart_interaction()
            time.sleep(0.05)

            save = None
            try:
                for save in self.saves_to_process:
                    if not self.processing:
                        return

                    if not save in self.skipped:
                        self.source_instance.location.unlink_save(save, scan=False)

                    self.processed += 1

                    # Allow UI updates during cleanup
                    time.sleep(0.05)
                    renpy.restart_interaction()

                self.process_done()
            except Exception as e:
                print(e)
                self.error = "An error occurred while cleaning up save \"" + save + "\":\n{color=[SSSSS.Colors.error]}" + str(e) + "{/color}"
                self.process_stop()

        def process_done(self):
            self.success = True
            self.processing = False

            SaveSystem.multilocation.scan()
            renpy.restart_interaction()

        class StartProcessAction(renpy.ui.Action):
            def __init__(self, viewModel, saves, mode="COPY"):
                self.viewModel = viewModel
                self.saves = saves
                self.mode = mode

            def __call__(self):
                self.viewModel.process_saves(self.saves, mode=self.mode)

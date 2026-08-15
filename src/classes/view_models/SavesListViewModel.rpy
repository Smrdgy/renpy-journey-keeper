init python in JK:
    _constant = True
    import threading
    import time

    class SavesListViewModel(x52NonPicklable):
        def __init__(self, playthrough):
            self.playthrough = playthrough

            self.screen = "SELECTION" # "SELECTION"|"PENDING"

            self.locations = []
            self.saves_length = 0
            self.saves_multilocation = None

            self.selection = SelectionState()

            self.processing = False
            self.processed = 0
            self.saves_to_process = []
            self.error = None
            self.success = False
            self.return_on_success = False

            self.delete_thread = None  # To track the delete thread
            self._last_progress_notify = 0.0

            self.load_saves()

        def load_saves(self):
            SaveSystem.multilocation.scan()

            instance = SaveSystem.get_playthrough_save_instance(self.playthrough.id)
            if not instance:
                return

            self.saves_multilocation = instance.location

            all_saves = set()

            self.locations = []
            self.saves_length = 0
            for location in instance.location.active_locations():
                saves = Utils.sort_saves(location.list())

                all_saves.update(saves)
                self.locations.append((location, saves))

                current_len = len(saves)
                if current_len > self.saves_length:
                    self.saves_length = current_len

            self.all_saves = Utils.sort_saves(all_saves)

            renpy.restart_interaction()

        def process_delete_start(self):
            self.processing = True
            self.processed = 0
            self._last_progress_notify = 0.0

            self.process_next_save()

        def process_next_save(self):
            if not self.processing:
                return

            # Check if all saves are processed
            if self.processed >= len(self.saves_to_process):
                # All saves processed
                self.process_done()

                return

            save = self.saves_to_process[self.processed]

            # Create a thread to copy the save to avoid blocking the main thread
            self.delete_thread = threading.Thread(target=self.delete_save_and_continue, args=(save,))
            self.delete_thread.daemon = True
            self.delete_thread.start()

        def delete_save_and_continue(self, save):
            save, location = save

            try:
                # Perform the save copy
                if location:
                    location.unlink_save(save, scan=False)
                else:
                    self.saves_multilocation.unlink_save(save, include_inactive=False, scan=False)

                self.process_continue()
            except Exception as e:
                print(e)
                self.error = "An error occurred while deleting save \"" + save + "\":\n{color=[JK.Colors.error]}" + str(e) + "{/color}"
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
            # single save, so the actual deletion work isn't throttled down to
            # the notification rate.
            now = time.time()
            if force or now - self._last_progress_notify >= 0.05:
                self._last_progress_notify = now
                renpy.restart_interaction()

        def process_done(self):
            self.success = True
            self.processed = 0
            self.processing = False

            renpy.restart_interaction()
            SaveSystem.multilocation.scan()

            if self.return_on_success:
                self.load_saves()

        def process_stop(self, success=False):
            self.success = success
            self.processed = 0
            self.processing = False

            renpy.restart_interaction()

            if self.delete_thread and self.delete_thread.is_alive():
                self.delete_thread.join()  # Wait for the thread to finish if stopping early

            SaveSystem.multilocation.scan()

        class SelectionAction(renpy.ui.Action):
            def __init__(self, view_model, id, all_saves):
                self.view_model = view_model
                self.id = id
                self.all_saves = all_saves

            def __call__(self):
                selection = self.view_model.selection
                same_directory = selection.anchor is not None and selection.anchor[1] == self.id[1]
                ordered_ids = [(save, self.id[1]) for save in self.all_saves]

                selection.click(self.id, ordered_ids, range_eligible=same_directory)

        class SetSelectionModeAction(renpy.ui.Action):
            def __init__(self, view_model, mode):
                self.view_model = view_model
                self.mode = mode

            def __call__(self):
                cs = renpy.current_screen()
                if not cs:
                    return

                self.view_model.selection.reset()

                cs.scope["selection_mode"] = self.mode

                renpy.restart_interaction()

        class SelectAllAction(renpy.ui.Action):
            def __init__(self, view_model, selection_mode):
                self.view_model = view_model
                self.selection_mode = selection_mode

            def __call__(self):
                ids = []

                if self.selection_mode == "PER_SAVE":
                    for save in self.view_model.locations[0][1]:
                        ids.append((save, None))
                else:
                    for location, saves in self.view_model.locations:
                        for save in saves:
                            ids.append((save, location))

                self.view_model.selection.select_all(ids)


        class MassDeleteConfirmAction(renpy.ui.Action):
            def __init__(self, view_model):
                self.view_model = view_model

            def __call__(self):
                showConfirm(
                    title="Delete " + str(len(self.view_model.selection.items)) + " save(s)",
                    message="Do you really wish to delete these saves?\nThis action {u}{color=[JK.Colors.error]}is irreversible{/c}{/u}.",
                    yes=SavesListViewModel.MassDeleteAction(self.view_model),
                    yes_icon="\ue92b",
                    yes_color=Colors.error
                )

        class MassDeleteAction(renpy.ui.Action):
            def __init__(self, view_model):
                self.view_model = view_model

            def __call__(self):
                self.view_model.saves_to_process = [] + self.view_model.selection.items
                self.view_model.return_on_success = False
                self.view_model.process_delete_start()

        class DeleteSingleConfirmAction(renpy.ui.Action):
            def __init__(self, view_model, save):
                self.view_model = view_model
                self.save = save

            def __call__(self):
                showConfirm(
                    title="Delete save \"" + self.save[0] + "\"",
                    message="Do you really wish to delete \"" + self.save[0] + "\"" + (" from \"" + self.save[1].directory + "\"" if self.save[1] else "") + "?\nThis action {u}{color=[JK.Colors.error]}is irreversible{/c}{/u}.",
                    yes=SavesListViewModel.DeleteSingleAction(self.view_model, self.save),
                    yes_icon="\ue92b",
                    yes_color=Colors.error
                )

        class DeleteSingleAction(renpy.ui.Action):
            def __init__(self, view_model, save):
                self.view_model = view_model
                self.save = save

            def __call__(self):
                self.view_model.saves_to_process = [self.save]
                self.view_model.return_on_success = True
                self.view_model.process_delete_start()

        class ClearSuccessAction(renpy.ui.Action):
            def __init__(self, view_model):
                self.view_model = view_model

            def __call__(self):
                self.view_model.success = False

                renpy.restart_interaction()

        class StartMoveCopyAction(renpy.ui.Action):
            def __init__(self, view_model, mode):
                self.view_model = view_model
                self.mode = mode

            def __call__(self):
                cs = renpy.current_screen()
                if not cs:
                    return

                cs.scope["move_copy_mode"] = self.mode
                cs.scope["move_copy_saves"] = [] + self.view_model.selection.items

                renpy.restart_interaction()

        class CancelMoveCopyAction(renpy.ui.Action):
            def __call__(self):
                cs = renpy.current_screen()
                if not cs:
                    return

                cs.scope["move_copy_mode"] = None
                cs.scope["move_copy_saves"] = []
                cs.scope["move_copy_destination_playthrough"] = None
                cs.scope["move_copy_view_model"] = None

                renpy.restart_interaction()

        class FinishMoveCopyAction(renpy.ui.Action):
            def __init__(self, view_model):
                self.view_model = view_model

            def __call__(self):
                cs = renpy.current_screen()
                if not cs:
                    return

                cs.scope["move_copy_mode"] = None
                cs.scope["move_copy_saves"] = []
                cs.scope["move_copy_destination_playthrough"] = None
                cs.scope["move_copy_view_model"] = None

                self.view_model.selection.reset()
                self.view_model.load_saves()

                renpy.restart_interaction()

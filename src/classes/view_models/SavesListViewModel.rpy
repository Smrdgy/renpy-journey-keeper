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

            self.selection = []

            self.processing = False
            self.processed = 0
            self.saves_to_process = []
            self.error = None
            self.success = False
            self.return_on_success = False

            self.delete_thread = None  # To track the delete thread

            self.load_saves()

        def load_saves(self):
            SaveSystem.multilocation.scan()

            instance = SaveSystem.getPlaythroughSaveInstance(self.playthrough.id)
            if not instance:
                return

            self.saves_multilocation = instance.location

            all_saves = set()

            self.locations = []
            self.saves_length = 0
            for location in instance.location.active_locations():
                saves = Utils.sortSaves(location.list())

                all_saves.update(saves)
                self.locations.append((location, saves))

                current_len = len(saves)
                if current_len > self.saves_length:
                    self.saves_length = current_len

            self.all_saves = Utils.sortSaves(all_saves)

            renpy.restart_interaction()

        def process_delete_start(self):
            self.processing = True
            self.processed = 0

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
            # Update progress and refresh the UI
            self.processed += 1
            renpy.restart_interaction()

            # Give time for the UI to update
            time.sleep(0.05)

            # Continue with the next save
            self.process_next_save()

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
            def __init__(self, viewModel, id, all_saves, last_selected_save):
                self.viewModel = viewModel
                self.id = id
                self.all_saves = all_saves
                self.last_selected_save = last_selected_save

            def __call__(self):
                matching_directory = self.last_selected_save and self.last_selected_save[1] == self.id[1]

                if matching_directory and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    directory = self.id[1]
                    start_index = self.all_saves.index(self.last_selected_save[0]) if self.last_selected_save[0] in self.all_saves else -1
                    end_index = self.all_saves.index(self.id[0]) if self.id[0] in self.all_saves else -1

                    if start_index > -1 and end_index > -1:
                        new_saves = []
                        for save in self.all_saves[min(start_index, end_index):max(start_index, end_index) + 1]:
                            if save in new_saves:
                                new_saves.remove((save, directory))
                            else:
                                new_saves.append((save, directory))

                        self.viewModel.selection = new_saves
                        renpy.restart_interaction()
                        return
                elif pygame.key.get_mods() & pygame.KMOD_LCTRL:
                    if self.id in self.viewModel.selection:
                        self.viewModel.selection.remove(self.id)
                    else:
                        self.viewModel.selection.append(self.id)
                else:
                    self.viewModel.selection = [self.id]
                
                cs = renpy.current_screen()
                if not cs:
                    return

                cs.scope["last_selected_save"] = self.id

                renpy.restart_interaction()
                

        class SetSelectionModeAction(renpy.ui.Action):
            def __init__(self, viewModel, mode):
                self.viewModel = viewModel
                self.mode = mode

            def __call__(self):
                cs = renpy.current_screen()
                if not cs:
                    return

                self.viewModel.selection = []

                cs.scope["last_selected_save"] = None
                cs.scope["selection_mode"] = self.mode

                renpy.restart_interaction()

        class SelectAllAction(renpy.ui.Action):
            def __init__(self, viewModel, selection_mode):
                self.viewModel = viewModel
                self.selection_mode = selection_mode

            def __call__(self):
                self.viewModel.selection = []

                if self.selection_mode == "PER_SAVE":
                    for save in self.viewModel.locations[0][1]:
                        self.viewModel.selection.append((save, None))
                else:
                    for location, saves in self.viewModel.locations:
                        for save in saves:
                            self.viewModel.selection.append((save, location))

                renpy.restart_interaction()
                

        class MassDeleteConfirmAction(renpy.ui.Action):
            def __init__(self, viewModel):
                self.viewModel = viewModel

            def __call__(self):
                showConfirm(
                    title="Delete " + str(len(self.viewModel.selection)) + " save(s)",
                    message="Do you really wish to delete these saves?\nThis action {u}{color=[JK.Colors.error]}is irreversible{/c}{/u}.",
                    yes=SavesListViewModel.MassDeleteAction(self.viewModel),
                    yesIcon="\ue92b",
                    yesColor=Colors.error
                )

        class MassDeleteAction(renpy.ui.Action):
            def __init__(self, viewModel):
                self.viewModel = viewModel

            def __call__(self):
                self.viewModel.saves_to_process = [] + self.viewModel.selection
                self.viewModel.return_on_success = False
                self.viewModel.process_delete_start()

        class DeleteSingleConfirmAction(renpy.ui.Action):
            def __init__(self, viewModel, save):
                self.viewModel = viewModel
                self.save = save

            def __call__(self):
                showConfirm(
                    title="Delete save \"" + self.save[0] + "\"",
                    message="Do you really wish to delete \"" + self.save[0] + "\"" + (" from \"" + self.save[1].directory + "\"" if self.save[1] else "") + "?\nThis action {u}{color=[JK.Colors.error]}is irreversible{/c}{/u}.",
                    yes=SavesListViewModel.DeleteSingleAction(self.viewModel, self.save),
                    yesIcon="\ue089",
                    yesColor=Colors.error
                )

        class DeleteSingleAction(renpy.ui.Action):
            def __init__(self, viewModel, save):
                self.viewModel = viewModel
                self.save = save

            def __call__(self):
                self.viewModel.saves_to_process = [self.save]
                self.viewModel.return_on_success = True
                self.viewModel.process_delete_start()

        class ClearSuccessAction(renpy.ui.Action):
            def __init__(self, viewModel):
                self.viewModel = viewModel

            def __call__(self):
                self.viewModel.success = False

                renpy.restart_interaction()

        class RefreshSavesAction(renpy.ui.Action):
            def __init__(self, viewModel):
                self.viewModel = viewModel

            def __call__(self):
                self.viewModel.load_saves()
                renpy.restart_interaction()

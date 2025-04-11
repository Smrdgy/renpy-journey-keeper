init python in JK:
    _constant = True

    import json
    import time
    import base64
    import re

    class PlaythroughsClass(x52NonPicklable):
        _playthroughs = []
        _activePlaythrough = None

        def __init__(self):
            # Legacy conversion #TODO: Remove at some point
            if renpy.store.persistent.SSSSS_playthroughs:
                renpy.store.persistent.JK_Playthroughs = renpy.store.persistent.SSSSS_playthroughs
                renpy.store.persistent.JK_PlaythroughsMtime = int(time.time())
                renpy.store.persistent.SSSSS_playthroughs = None
            if renpy.store.persistent.URPS_Playthroughs:
                renpy.store.persistent.JK_Playthroughs = renpy.store.persistent.URPS_Playthroughs
                renpy.store.persistent.JK_PlaythroughsMtime = int(time.time())
                renpy.store.persistent.URPS_Playthroughs = None

            # For some reason the __init__ is called twice in Ren'Py 7.0.0.196.
            # When that happens the playthroughs are loaded twice which led to a buildup of playthroughs when saved. This if should mitigate that.
            if hasattr(renpy.config, "JK_Playthroughs_initialized"): return
            renpy.config.JK_Playthroughs_initialized = True

            hasNative = False
            hasMemories = False

            userdir_playthroughs = UserDir.load_playthroughs()
            persistent_playthroughs = self.load_from_persistent()

            userdir_mtime = UserDir.playthroughs_mtime()
            persistent_mtime = renpy.store.persistent.JK_PlaythroughsMtime or 0

            playthroughs = None
            if userdir_mtime > persistent_mtime:
                playthroughs = userdir_playthroughs
            else:
                playthroughs = persistent_playthroughs

            if(playthroughs != None):
                for playthrough in playthroughs:
                    if(playthrough.get("id") == 1):
                        hasNative = True
                    elif playthrough.get("id") == 2:
                        hasMemories = True

                    self._playthroughs.append(self.create_playthrough_from_serialization(playthrough))

            native, memories = PlaythroughsClass.get_default_playthroughs()

            if(not hasNative):
                self._playthroughs.insert(0, native)

            if not hasMemories and Settings.memoriesEnabled:
                self._playthroughs.insert(1, memories)

        @property
        def playthroughs(self):
            return self._playthroughs

        @property
        def active_playthrough(self):
            if(self._activePlaythrough != None):
                return self._activePlaythrough

            return self._playthroughs[0]

        @property
        def active_playthrough_or_none(self):
            if(self._activePlaythrough != None):
                return self._activePlaythrough

            return None

        def load_from_persistent(self):
            if renpy.store.persistent.JK_Playthroughs:
                return json.loads(renpy.store.persistent.JK_Playthroughs)

            return []

        @staticmethod
        def get_default_playthroughs():
            return (
                PlaythroughClass(id=1, directory="", name="Native", autosaveOnChoices=False, useChoiceLabelAsSaveName=False),#MODIFY HERE
                PlaythroughClass(id=2, directory="_memories", name="Memories", autosaveOnChoices=False, useChoiceLabelAsSaveName=False)#MODIFY HERE
            )

        def create_playthrough_from_serialization(self, data):
            return PlaythroughClass(id=data.get("id"), directory=data.get("directory"), name=data.get("name"), description=data.get("description"), thumbnail=data.get("thumbnail"), storeChoices=data.get("storeChoices"), autosaveOnChoices=data.get("autosaveOnChoices"), selectedPage=data.get("selectedPage"), filePageName=data.get("filePageName"), useChoiceLabelAsSaveName=data.get("useChoiceLabelAsSaveName"), enabledSaveLocations=data.get("enabledSaveLocations"))#MODIFY HERE

        def get_instance_for_edit(self):
            playthrough = self.create_playthrough_from_serialization(Settings.playthroughTemplate) if Settings.playthroughTemplate else PlaythroughClass()
            playthrough.directory = None

            return playthrough

        def list_available_directories_to_create_playthrough_from(self):
            directories = Utils.list_save_directories()
            playthrough_dirnames = [playthrough.directory for playthrough in Playthroughs.playthroughs]

            relevant_directories = set()
            for dirname, path in directories:
                if dirname not in playthrough_dirnames and dirname.lower() not in ["_memories", "sync"]:
                    relevant_directories.add(dirname)

            return relevant_directories

        def add(self, playthrough, activate=True, save=True, restart_interaction=True):
            self._playthroughs.append(playthrough)

            if activate:
                self.activate_by_instance(playthrough)

            if save:
                self.save()

            if restart_interaction:
                renpy.restart_interaction()

            return playthrough

        def get(self, name):
            for playthrough in self.playthroughs:
                if(playthrough.name == name):
                    return playthrough

            return None

        def get_by_id(self, id):
            for playthrough in self.playthroughs:
                if(playthrough.id == id):
                    return playthrough

            return None

        def get_index_by_id(self, id):
            i = 0
            for playthrough in self.playthroughs:
                if playthrough.id == id:
                    return i

                i += 1

            return -1

        def remove(self, playthroughID, delete_save_files=False, keepActive=False):
            playthrough = self.get_by_id(playthroughID)
            if playthrough:
                if delete_save_files:
                    SaveSystem.remove_save_files_for_playthrough(playthrough, remove_dir=True)

                self.playthroughs.remove(playthrough)

            if keepActive == False:
                self.activate_first_or_none()

            return True

        def edit(self, playthrough, originalPlaythrough, moveSaveDirectory=False):
            rv = originalPlaythrough.edit_from_playthrough(playthrough, moveSaveDirectory=moveSaveDirectory)
                
            self.save()
            renpy.restart_interaction()

            return rv

        def add_or_edit(self, playthrough, moveSaveDirectory=False, force=False):
            sourcePlaythrough = self.get_by_id(playthrough.id)
            if(sourcePlaythrough != None):
                if moveSaveDirectory and sourcePlaythrough.name != playthrough.name and playthrough.id != 1 and self.is_valid_name(playthrough.name):
                    result = self.rename_save_directory(sourcePlaythrough, Utils.name_to_directory_name(playthrough.name), force=force)

                    if result != True:
                        renpy.show_screen("JK_MovePlaythroughDirectoryError", playthrough=playthrough, errors=result)
                        return None

                rv = self.edit(playthrough, sourcePlaythrough, moveSaveDirectory=moveSaveDirectory)

                if self.active_playthrough.id == rv.id:
                    SaveSystem.regenerate_playthrough_save_instance(rv)

                return rv

            return self.add(playthrough)

        def toggle_autosave_on_choices_for_active(self):
            self.active_playthrough.edit(autosaveOnChoices=not self.active_playthrough.autosaveOnChoices)

            Autosaver.pending_save = None
            renpy.restart_interaction()

            self.save()

            renpy.notify("Autosave on choice is " + ("enabled" if self.active_playthrough.autosaveOnChoices else "disabled"))

        def activate_by_name(self, playthroughName):
            self.activate_by_instance(self.get(playthroughName))

        def activate_by_id(self, playthroughID):
            self.activate_by_instance(self.get_by_id(playthroughID))

        def activate_by_instance(self, playthrough):
            if(playthrough == None):
                return

            SaveSystem.get_or_create_playthrough_save_instance(playthrough, autoActivate=True)

            self.__set_active_playthrough(playthrough)

            self.save()
            renpy.restart_interaction()

        def activate_native(self):
            self.activate_by_instance(self.playthroughs[0])

        def activate_first_or_none(self):
            self.activate_native()

        def save(self):
            self.save_to_user_dir()
            self.save_to_persistent()

        def get_playthrough_as_json(self):
            arr = []
            for playthrough in self.playthroughs:
                if playthrough.id != 2:
                    arr.append(playthrough.serializable())

            return json.dumps(arr)

        def save_to_user_dir(self):
            save_to_userdir = UserDir.has_playthroughs()
            if len(self.playthroughs) <= 2:
                if self.get_by_id(1).serializable() != PlaythroughsClass.get_default_playthroughs()[0].serializable():
                    save_to_userdir = True
            else:
                save_to_userdir = True

            if save_to_userdir:
                UserDir.save_playthroughs(self.get_playthrough_as_json())

        def save_to_persistent(self):
            renpy.store.persistent.JK_Playthroughs = self.get_playthrough_as_json()
            renpy.store.persistent.JK_PlaythroughsMtime = int(time.time())

            renpy.save_persistent()

        def is_valid_name(self, name):
            for playthrough in self.playthroughs:
                if playthrough.name == name:
                    return False

            return True

        def rename_save_directory(self, playthrough, newName, force=False):
            instance = SaveSystem.get_or_create_playthrough_save_instance(playthrough)

            if instance:
                errors = [] if force else instance.location.validate_locations_for_change_of_directory_name(newName)

                if len(errors) == 0:
                    instance.location.change_locations_directory_name(newName, force=force)
                    instance.location.scan()

                    return True

            return errors

        def __set_active_playthrough(self, playthrough=None):
            prev_playthrough = self.active_playthrough_or_none
            if prev_playthrough:
                self.active_playthrough.before_deactivation()

            renpy.store.persistent.JK_ActivePlaythrough = playthrough.id if playthrough != None else None
            self._activePlaythrough = playthrough

            if prev_playthrough:
                renpy.store.persistent._file_page = str(playthrough.selectedPage or 1)
                renpy.store.persistent._file_page_name = playthrough.filePageName or {}

            self.save_to_persistent()

        class ActivateNative(renpy.ui.Action):
            def __call__(self):
                Playthroughs.activate_native()

        class SetThumbnail(renpy.ui.Action):
            def __init__(self, playthrough):
                self.playthrough = playthrough

            def __call__(self):
                self.playthrough.make_thumbnail()

                renpy.restart_interaction()

        class AddOrEditAction(renpy.ui.Action):
            def __init__(self, playthrough, name, description, storeChoices, autosaveOnChoices, useChoiceLabelAsSaveName, enabledSaveLocations, moveSaveDirectory):#MODIFY HERE
                self.playthrough = playthrough
                self.name = name
                self.description = description
                self.storeChoices = storeChoices
                self.autosaveOnChoices = autosaveOnChoices
                self.useChoiceLabelAsSaveName = useChoiceLabelAsSaveName
                self.enabledSaveLocations = enabledSaveLocations
                self.moveSaveDirectory = moveSaveDirectory
                #MODIFY HERE

            def __call__(self):
                playthrough = self.playthrough if not callable(self.playthrough) else self.playthrough()
                name = self.name if not callable(self.name) else self.name()
                description = self.description if not callable(self.description) else self.description()
                storeChoices = self.storeChoices if not callable(self.storeChoices) else self.storeChoices()
                autosaveOnChoices = self.autosaveOnChoices if not callable(self.autosaveOnChoices) else self.autosaveOnChoices()
                useChoiceLabelAsSaveName = self.useChoiceLabelAsSaveName if not callable(self.useChoiceLabelAsSaveName) else self.useChoiceLabelAsSaveName()
                enabledSaveLocations = self.enabledSaveLocations if not callable(self.enabledSaveLocations) else self.enabledSaveLocations()
                moveSaveDirectory = self.moveSaveDirectory if not callable(self.moveSaveDirectory) else self.moveSaveDirectory()
                #MODIFY HERE

                playthrough = playthrough.copy().edit(name=name, description=description, storeChoices=storeChoices, autosaveOnChoices=autosaveOnChoices, useChoiceLabelAsSaveName=useChoiceLabelAsSaveName, enabledSaveLocations=enabledSaveLocations)#MODIFY HERE

                if moveSaveDirectory and playthrough.id == 1:
                    moveSaveDirectory = False

                Playthroughs.add_or_edit(playthrough, moveSaveDirectory=moveSaveDirectory)
                renpy.restart_interaction()

        class ActivatePlaythroughAction(renpy.ui.Action):
            def __init__(self, playthrough):
                self.playthrough = playthrough

            def __call__(self):
                Playthroughs.activate_by_id(self.playthrough.id)
                renpy.restart_interaction()

        class RemoveAction(renpy.ui.Action):
            def __init__(self, playthroughID, deleteSaves):
                self.playthroughID = playthroughID
                self.deleteSaves = deleteSaves

            def __call__(self):
                playthroughID = self.playthroughID if not callable(self.playthroughID) else self.playthroughID()
                deleteSaves = self.deleteSaves if not callable(self.deleteSaves) else self.deleteSaves()

                Playthroughs.remove(playthroughID=playthroughID, delete_save_files=deleteSaves)
                renpy.restart_interaction()

        class ToggleAutosaveOnChoicesForActiveAction(renpy.ui.Action):
            def __call__(self):
                renpy.invoke_in_thread(Playthroughs.toggle_autosave_on_choices_for_active)

        class QuickSaveAction(renpy.ui.Action):
            temp_save_slotname = "JK-temp"

            def __init__(self, force=False, move_one=False):
                self.force = force
                self.move_one = move_one

            def __call__(self):
                if self.move_one:
                    Autosaver.set_next_slot()

                page, _, slotString = Autosaver.get_current_slot()
                slotString = Utils.format_slotname(slotString)

                if not self.move_one and not self.force:
                    renpy.take_screenshot()

                renpy.save(self.temp_save_slotname)

                if not self.force and SaveSystem.multilocation.newest(slotString):
                    renpy.show_screen("JK_QuickSaveOverwriteConfirm")
                    return

                renpy.rename_save(self.temp_save_slotname, slotString)

                if Settings.offsetSlotAfterQuickSave:
                    Autosaver.set_next_slot()

                if Settings.pageFollowsQuickSave:
                    renpy.store.persistent._file_page = str(page)

                # if Settings.quickSaveNotificationEnabled:
                #     renpy.notify("Quicksave created at {}".format(slotString))

        class TrySequentializeSaves(renpy.ui.Action):
            def __init__(self, playthrough):
                self.playthrough = playthrough

            def __call__(self):
                playthrough = self.playthrough if not callable(self.playthrough) else self.playthrough()

                showConfirm(
                    title="Sequentialize playthrough",
                    message="Sequentialization of a playthrough will rename all your saves, so they start from 1-1 and continue in a sequence without a gap.\nIt may take some time based on the amount of saves and your device.\nThis action {u}{color=[JK.Colors.error]}is irreversible{/c}{/u}. Do you wish to proceed?",
                    yes=Call(playthrough.sequentializeSaves),
                    yes_icon="\ue089",
                    yes_color=Colors.error
                )

        class DeleteAllSavesAction(renpy.ui.Action):
            def __init__(self, playthrough):
                self.playthrough = playthrough

            def __call__(self):
                SaveSystem.remove_save_files_for_playthrough(self.playthrough)
                renpy.restart_interaction()

        class ConfirmDeleteAllSavesAction(renpy.ui.Action):
            def __init__(self, playthrough):
                self.playthrough = playthrough

            def __call__(self):
                name = self.playthrough.name

                showConfirm(
                    title="Remove all saves",
                    message="This action will remove {b}{u}all{/u}{/b} your save files for the \"" + name + "\" playthrough.\nThis action {u}{color=[JK.Colors.error]}is irreversible{/c}{/u}. Do you wish to proceed?",
                    yes=Playthroughs.DeleteAllSavesAction(self.playthrough),
                    yes_icon="\ue92b",
                    yes_color=Colors.error
                )

        class DuplicatePlaythroughAction(renpy.ui.Action):
            def __init__(self, playthrough, name, description):
                self.playthrough = playthrough
                self.name = name
                self.description = description

            def __call__(self):
                new_playthrough = self.playthrough.copy()
                new_playthrough.id = int(time.time())
                new_playthrough.directory = None
                new_playthrough.edit(name=self.name, description=self.description)

                Playthroughs.add(new_playthrough)

                original_instance = SaveSystem.get_playthrough_save_instance(self.playthrough.id)
                if not original_instance:
                    raise Exception("Can't find old save instance")

                new_instance = SaveSystem.get_playthrough_save_instance(new_playthrough.id)
                if not new_instance:
                    raise Exception("Can't find new save instance")

                original_instance.location.scan()
                if not original_instance.location.copy_all_saves_into_other_multilocation(new_instance.location):
                    raise Exception("Playthrough created but failed to transfer saves. Check the logs for more information.")

                renpy.restart_interaction()

                renpy.hide_screen("JK_DuplicatePlaythrough")
        
        class ShowCreatePlaythroughFromDirnameAction(renpy.ui.Action):
            def __init__(self, dirname):
                self.dirname = dirname

            def __call__(self):
                playthrough = Playthroughs.get_instance_for_edit()
                playthrough.name = self.dirname
                playthrough.directory = self.dirname

                renpy.show_screen("JK_EditPlaythrough", playthrough)

        class ForceRenamePlaythroughAction(renpy.ui.Action):
            def __init__(self, playthrough):
                self.playthrough = playthrough

            def __call__(self):
                Playthroughs.add_or_edit(self.playthrough, moveSaveDirectory=True, force=True)

        class ReorderPlaythroughsAction(renpy.ui.Action):
            def __init__(self, source, target):
                self.source = source
                self.target = target

            def __call__(self):
                source_index = Playthroughs.get_index_by_id(self.source)
                target_index = Playthroughs.get_index_by_id(self.target)

                if source_index > -1 and target_index > -1:
                    if source_index > 0 or target_index + 1 == len(Playthroughs.playthroughs):
                        Playthroughs.playthroughs.insert(target_index, Playthroughs.playthroughs.pop(source_index))
                    else:
                        Playthroughs.playthroughs.insert(target_index + 1, Playthroughs.playthroughs.pop(source_index))

                    Playthroughs.save()
                    renpy.restart_interaction()
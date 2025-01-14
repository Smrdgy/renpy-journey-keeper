init 1 python in JK:
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

            userdir_playthroughs = UserDir.loadPlaythroughs()
            persistent_playthroughs = self.loadFromPersistent()

            userdir_mtime = UserDir.playthroughsMtime()
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

                    self._playthroughs.append(self.createPlaythroughFromSerialization(playthrough))

            native, memories = PlaythroughsClass.get_default_playthroughs()

            if(not hasNative):
                self._playthroughs.insert(0, native)

            if not hasMemories and Settings.memoriesEnabled:
                self._playthroughs.insert(1, memories)

        @property
        def playthroughs(self):
            return self._playthroughs

        @property
        def activePlaythrough(self):
            if(self._activePlaythrough != None):
                return self._activePlaythrough

            return self._playthroughs[0]

        @property
        def activePlaythroughOrNone(self):
            if(self._activePlaythrough != None):
                return self._activePlaythrough

            return None

        def loadFromPersistent(self):
            if renpy.store.persistent.JK_Playthroughs:
                return json.loads(renpy.store.persistent.JK_Playthroughs)

            return []

        @staticmethod
        def get_default_playthroughs():
            return (
                PlaythroughClass(id=1, directory="", name="Native", autosaveOnChoices=False, useChoiceLabelAsSaveName=False),#MODIFY HERE
                PlaythroughClass(id=2, directory="_memories", name="Memories", autosaveOnChoices=False, useChoiceLabelAsSaveName=False)#MODIFY HERE
            )

        def createPlaythroughFromSerialization(self, data):
            return PlaythroughClass(id=data.get("id"), directory=data.get("directory"), name=data.get("name"), description=data.get("description"), thumbnail=data.get("thumbnail"), storeChoices=data.get("storeChoices"), autosaveOnChoices=data.get("autosaveOnChoices"), selectedPage=data.get("selectedPage"), filePageName=data.get("filePageName"), useChoiceLabelAsSaveName=data.get("useChoiceLabelAsSaveName"), enabledSaveLocations=data.get("enabledSaveLocations"))#MODIFY HERE

        def get_instance_for_edit(self):
            playthrough = self.createPlaythroughFromSerialization(Settings.playthroughTemplate) if Settings.playthroughTemplate else PlaythroughClass()
            playthrough.directory = None

            return playthrough

        def list_available_directories_to_create_playthrough_from(self):
            directories = Utils.list_save_directories()
            playthrough_dirnames = [playthrough.directory for playthrough in Playthroughs.playthroughs]

            relevant_directories = set()
            for dirname, path in directories:
                if dirname not in playthrough_dirnames:
                    relevant_directories.add(dirname)

            return relevant_directories                     

        def add(self, playthrough):
            self._playthroughs.append(playthrough)
            self.activateByInstance(playthrough)

            self.save()
            renpy.restart_interaction()

            return playthrough

        def get(self, name):
            for playthrough in self.playthroughs:
                if(playthrough.name == name):
                    return playthrough

            return None

        def getByID(self, id):
            for playthrough in self.playthroughs:
                if(playthrough.id == id):
                    return playthrough

            return None

        def getOrAdd(self, name):
            return self.get(name) or self.add(PlaythroughClass(name=name))

        def remove(self, playthroughID, deleteSaveFiles=False, keepActive=False):
            for playthrough in self.playthroughs:
                if(playthrough.id == playthroughID):
                    if(deleteSaveFiles):
                        SaveSystem.removeFilesForPlaythrough(playthrough)

                    self.playthroughs.remove(playthrough)

            if(keepActive == False):
                self.activateFirstOrNone()

            return True

        def edit(self, playthrough, originalPlaythrough, moveSaveDirectory=False):
            rv = originalPlaythrough.editFromPlaythrough(playthrough, moveSaveDirectory=moveSaveDirectory)
                
            self.save()
            renpy.restart_interaction()

            return rv

        def addOrEdit(self, playthrough, moveSaveDirectory=False):
            sourcePlaythrough = self.getByID(playthrough.id)
            if(sourcePlaythrough != None):
                if moveSaveDirectory and sourcePlaythrough.name != playthrough.name and playthrough.id != 1:
                    result = self.renameSaveDirectory(sourcePlaythrough, Utils.name_to_directory_name(playthrough.name))

                    if result != True:
                        renpy.show_screen("JK_MovePlaythroughDirectoryError", errors=result)
                        return None

                rv = self.edit(playthrough, sourcePlaythrough, moveSaveDirectory=moveSaveDirectory)

                if self.activePlaythrough.id == rv.id:
                    SaveSystem.regeneratePlaythroughSaveInstance(rv)

                return rv

            return self.add(playthrough)

        def toggleAutosaveOnChoicesOnActive(self):
            self.activePlaythrough.edit(autosaveOnChoices=not self.activePlaythrough.autosaveOnChoices)

            Autosaver.pendingSave = None

            self.save()
            renpy.restart_interaction()

            renpy.notify("Autosave on choice is " + ("enabled" if self.activePlaythrough.autosaveOnChoices else "disabled"))

        def activateByName(self, playthroughName):
            self.activateByInstance(self.get(playthroughName))

        def activateByID(self, playthroughID):
            self.activateByInstance(self.getByID(playthroughID))

        def activateByInstance(self, playthrough):
            if(playthrough == None):
                return

            SaveSystem.getOrCreatePlaythroughSaveInstance(playthrough, autoActivate=True)

            self.__setActivePlaythrough(playthrough)

            self.save()
            renpy.restart_interaction()

        def activateNative(self):
            self.activateByInstance(self.playthroughs[0])

        def activateFirstOrNone(self):
            self.activateNative()

        def save(self):
            self.saveToUserDir()
            self.saveToPersistent()

        def getPlaythroughsAsJson(self):
            arr = []
            for playthrough in self.playthroughs:
                if playthrough.id != 2:
                    arr.append(playthrough.serializable())

            return json.dumps(arr)

        def saveToUserDir(self):
            save_to_userdir = UserDir.hasPlaythroughs()
            if len(self.playthroughs) <= 2:
                if self.getByID(1).serializable() != PlaythroughsClass.get_default_playthroughs()[0].serializable():
                    save_to_userdir = True
            else:
                save_to_userdir = True

            if save_to_userdir:
                UserDir.savePlaythroughs(self.getPlaythroughsAsJson())

        def saveToPersistent(self):
            renpy.store.persistent.JK_Playthroughs = self.getPlaythroughsAsJson()
            renpy.store.persistent.JK_PlaythroughsMtime = int(time.time())

            renpy.save_persistent()

        def isValidName(self, name):
            for playthrough in self.playthroughs:
                if(playthrough.name == name):
                    return False

            return True

        def renameSaveDirectory(self, playthrough, newName):
            import os

            instance = SaveSystem.getPlaythroughSaveInstance(playthrough.id)

            if instance:
                errors = []
                paths = []

                for location in instance.location.locations:
                    newPath = os.path.abspath(os.path.join(location.directory, "..", newName))

                    if os.path.exists(newPath):
                        errors.append((newPath, "LOCATION_EXISTS"))
                    else:
                        oldPath = os.path.abspath(location.directory)

                        paths.append((oldPath, newPath))

                if len(errors) == 0:
                    for oldPath, newPath in paths:
                        if os.path.exists(oldPath):
                            os.rename(oldPath, newPath)
                        else:
                            os.mkdir(newPath)

                    return True

            return errors

        def __setActivePlaythrough(self, playthrough=None):
            prev_playthrough = self.activePlaythroughOrNone
            if prev_playthrough:
                self.activePlaythrough.beforeDeactivation()

            renpy.store.persistent.JK_ActivePlaythrough = playthrough.id if playthrough != None else None
            self._activePlaythrough = playthrough

            if prev_playthrough:
                renpy.store.persistent._file_page = str(playthrough.selectedPage or 1)
                renpy.store.persistent._file_page_name = playthrough.filePageName or {}

            self.saveToPersistent()

        class ActivateNative(renpy.ui.Action):
            def __call__(self):
                Playthroughs.activateNative()

        class SetThumbnail(renpy.ui.Action):
            def __init__(self, playthrough):
                self.playthrough = playthrough

            def __call__(self):
                self.playthrough.makeThumbnail()

                renpy.restart_interaction()

        class AddOrEdit(renpy.ui.Action):
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

                Playthroughs.addOrEdit(playthrough, moveSaveDirectory=moveSaveDirectory)
                renpy.restart_interaction()

        class ActivatePlaythrough(renpy.ui.Action):
            def __init__(self, playthrough):
                self.playthrough = playthrough

            def __call__(self):
                Playthroughs.activateByID(self.playthrough.id)
                renpy.restart_interaction()

        class Remove(renpy.ui.Action):
            def __init__(self, playthroughID, deleteSaves):
                self.playthroughID = playthroughID
                self.deleteSaves = deleteSaves

            def __call__(self):
                playthroughID = self.playthroughID if not callable(self.playthroughID) else self.playthroughID()
                deleteSaves = self.deleteSaves if not callable(self.deleteSaves) else self.deleteSaves()

                Playthroughs.remove(playthroughID=playthroughID, deleteSaveFiles=deleteSaves)
                renpy.restart_interaction()

        class ToggleAutosaveOnChoicesOnActive(renpy.ui.Action):
            def __call__(self):
                Playthroughs.toggleAutosaveOnChoicesOnActive()

        class QuickSave(renpy.ui.Action):
            def __call__(self):
                page, _, slotString = Autosaver.getCurrentSlot()
                slotString = Utils.format_slotname(slotString)

                renpy.take_screenshot()
                renpy.save(slotString)

                if not Settings.offsetSlotAfterManualSave:
                    Autosaver.setNextSlot()

                if Settings.pageFollowsQuickSave:
                    renpy.store.persistent._file_page = str(page)

                if Settings.quickSaveNotificationEnabled:
                    renpy.notify("Quicksave created at {}".format(slotString))

        class TrySequentializeSaves(renpy.ui.Action):
            def __init__(self, playthrough):
                self.playthrough = playthrough

            def __call__(self):
                playthrough = self.playthrough if not callable(self.playthrough) else self.playthrough()

                showConfirm(
                    title="Sequentialize playthrough",
                    message="Sequentialization of a playthrough will rename all your saves, so they start from 1-1 and continue in a sequence without a gap.\nIt may take some time based on the amount of saves and your device.\nThis action {u}{color=[JK.Colors.error]}is irreversible{/c}{/u}. Do you wish to proceed?",
                    yes=Playthroughs.SequentializeSaves(playthrough),
                    yesIcon="\ue089",
                    yesColor=Colors.error
                )

        class SequentializeSaves(renpy.ui.Action):
            def __init__(self, playthrough):
                self.playthrough = playthrough

            def __call__(self):
                self.playthrough.sequentializeSaves()
        
        class RemoveThumbnail(renpy.ui.Action):
            def __init__(self, playthrough):
                self.playthrough = playthrough

            def __call__(self):
                self.playthrough.removeThumbnail()
                renpy.restart_interaction()

        class DeleteAllSaves(renpy.ui.Action):
            def __init__(self, playthrough):
                self.playthrough = playthrough

            def __call__(self):
                SaveSystem.removeSaveFilesForPlaythrough(self.playthrough)
                renpy.restart_interaction()

        class ConfirmDeleteAllSaves(renpy.ui.Action):
            def __init__(self, playthrough):
                self.playthrough = playthrough

            def __call__(self):
                name = self.playthrough.name

                showConfirm(
                    title="Remove all saves",
                    message="This action will remove {b}{u}all{/u}{/b} your save files for the \"" + name + "\" playthrough.\nThis action {u}{color=[JK.Colors.error]}is irreversible{/c}{/u}. Do you wish to proceed?",
                    yes=Playthroughs.DeleteAllSaves(self.playthrough),
                    yesIcon="\ue92b",
                    yesColor=Colors.error
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

                original_instance = SaveSystem.getPlaythroughSaveInstance(self.playthrough.id)
                if not original_instance:
                    raise Exception("Can't find old save instance")

                new_instance = SaveSystem.getPlaythroughSaveInstance(new_playthrough.id)
                if not new_instance:
                    raise Exception("Can't find new save instance")

                original_instance.location.scan()
                if not original_instance.location.copy_all_saves_into_other_multilocation(new_instance.location):
                    raise Exception("Playthrough created but failed to transfer saves. Check the logs for more information.")

                renpy.restart_interaction()

                renpy.hide_screen("JK_DuplicatePlaythrough")
        
        class ShowCreatePlaythroughFromDirname(renpy.ui.Action):
            def __init__(self, dirname):
                self.dirname = dirname

            def __call__(self):
                playthrough = Playthroughs.get_instance_for_edit()
                playthrough.name = self.dirname
                playthrough.directory = self.dirname

                renpy.show_screen("JK_EditPlaythrough", playthrough)
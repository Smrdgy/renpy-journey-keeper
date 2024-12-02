init 1 python in SSSSS:
    _constant = True

    import json
    import time
    import base64
    import re

    class PlaythroughsClass(x52NonPicklable):
        _playthroughs = []
        _activePlaythrough = None

        def __init__(self):
            # For some reason the __init__ is called twice in Ren'Py 7.0.0.196.
            # When that happens the playthroughs are loaded twice which led to a buildup of playthroughs when saved. This if should mitigate that.
            if hasattr(renpy.config, "SSSSS_playthroughs_initialized"): return
            renpy.config.SSSSS_playthroughs_initialized = True

            hasNative = False
            hasMemories = False

            userdir_playthroughs = UserDir.loadPlaythroughs()
            persistent_playthroughs = self.loadFromPersistent()

            userdir_mtime = UserDir.playthroughsMtime()
            persistent_mtime = renpy.store.persistent.SSSSS_playthroughsMtime or 0

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

            if(not hasNative):
                self._playthroughs.insert(0, self.PlaythroughClass(id=1, directory="", name="Native", autosaveOnChoices=False, useChoiceLabelAsSaveName=False))#MODIFY HERE

            if not hasMemories and Settings.memoriesEnabled:
                self._playthroughs.insert(1, self.PlaythroughClass(id=2, directory="_memories", name="Memories", autosaveOnChoices=False, useChoiceLabelAsSaveName=False))#MODIFY HERE

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
            if renpy.store.persistent.SSSSS_playthroughs:
                return json.loads(renpy.store.persistent.SSSSS_playthroughs)

            return []

        def createPlaythroughFromSerialization(self, data):
            return PlaythroughsClass.PlaythroughClass(id=data.get("id"), directory=data.get("directory"), name=data.get("name"), description=data.get("description"), thumbnail=data.get("thumbnail"), storeChoices=data.get("storeChoices"), layout=data.get("layout"), autosaveOnChoices=data.get("autosaveOnChoices"), selectedPage=data.get("selectedPage"), filePageName=data.get("filePageName"), useChoiceLabelAsSaveName=data.get("useChoiceLabelAsSaveName"), enabledSaveLocations=data.get("enabledSaveLocations"))#MODIFY HERE

        class PlaythroughClass(x52NonPicklable):
            def __init__(self, id=None, directory=None, name=None, description=None, thumbnail=None, storeChoices=False, layout="normal", autosaveOnChoices=True, selectedPage=1, filePageName={}, useChoiceLabelAsSaveName=False, enabledSaveLocations=None):#MODIFY HERE
                self.id = id or int(time.time())
                self.directory = directory if (directory != None) else (Utils.name_to_directory_name(name) if name else None)
                self.name = name
                self.description = description
                self.thumbnail = thumbnail
                self.storeChoices = storeChoices
                self.layout = layout
                self.autosaveOnChoices = autosaveOnChoices
                self.selectedPage = selectedPage
                self.filePageName = filePageName
                self.useChoiceLabelAsSaveName = useChoiceLabelAsSaveName
                self.enabledSaveLocations = enabledSaveLocations # Possible values: USER, GAME, string (other full path locations, e.g. C:\\Users\User\Desktop\some saves directory)
                #MODIFY HERE

            def __getstate__(self):
                return None

            def copy(self):
                return PlaythroughsClass.PlaythroughClass(self.id, self.directory, self.name, self.description, self.thumbnail, self.storeChoices, self.layout, self.autosaveOnChoices, self.selectedPage, self.filePageName, self.useChoiceLabelAsSaveName, self.enabledSaveLocations)#MODIFY HERE

            def edit(self, name=None, description=None, thumbnail=None, storeChoices=None, layout=None, autosaveOnChoices=None, selectedPage=None, filePageName=None, useChoiceLabelAsSaveName=None, enabledSaveLocations=None):#MODIFY HERE
                if name != None:
                    self.name = name

                    if(self.directory == None):
                        self.directory = Utils.name_to_directory_name(name)

                if description != None: self.description = description
                if thumbnail != None: self.thumbnail = thumbnail
                if storeChoices != None: self.storeChoices = storeChoices
                if layout != None: self.layout = layout
                if autosaveOnChoices != None: self.autosaveOnChoices = autosaveOnChoices
                if selectedPage != None: self.selectedPage = selectedPage
                if filePageName != None: self.filePageName = filePageName
                if useChoiceLabelAsSaveName != None: self.useChoiceLabelAsSaveName = useChoiceLabelAsSaveName
                if enabledSaveLocations != None: self.enabledSaveLocations = enabledSaveLocations or None #enabledSaveLocations can be False, in that case it needs to be replaced with None
                #MODIFY HERE

                return self

            def editFromPlaythrough(self, playthrough, moveSaveDirectory=False):
                if(self.directory == None or (moveSaveDirectory and playthrough.name != self.name)):
                    self.directory = Utils.name_to_directory_name(playthrough.name)

                self.name = playthrough.name
                self.description = playthrough.description
                self.thumbnail = playthrough.thumbnail
                self.storeChoices = playthrough.storeChoices
                self.layout = playthrough.layout
                self.autosaveOnChoices = playthrough.autosaveOnChoices
                self.selectedPage = playthrough.selectedPage
                self.filePageName = playthrough.filePageName
                self.useChoiceLabelAsSaveName = playthrough.useChoiceLabelAsSaveName
                self.enabledSaveLocations = playthrough.enabledSaveLocations
                #MODIFY HERE

                return self

            def serializable(self):
                return {
                    'id': self.id,
                    'directory': self.directory,
                    'name': self.name,
                    'description': self.description,
                    'thumbnail': self.thumbnail,
                    'storeChoices': self.storeChoices,
                    'layout': self.layout,
                    'autosaveOnChoices': self.autosaveOnChoices,
                    'selectedPage': self.selectedPage,
                    'filePageName': self.filePageName,
                    'useChoiceLabelAsSaveName': self.useChoiceLabelAsSaveName,
                    'enabledSaveLocations': self.enabledSaveLocations,
                    #MODIFY HERE
                }

            def getThumbnail(self, width=None, height=None, maxWidth=None, maxHeight=None):
                defWidth = 150
                defHeight = 150

                if(self.thumbnail == None):
                    return ImagePlaceholder(width or defWidth, height or defHeight)

                import io

                try:
                    # Decode the base64 string to bytes
                    decoded_bytes = base64.b64decode(self.thumbnail)
                    # Create a BytesIO object from the decoded bytes
                    sio = io.BytesIO(decoded_bytes)
                    # Load the image using Ren'Py's load_image function
                    rv = renpy.display.pgrender.load_image(sio, "image.png")

                    # Return the Image object with specified dimensions
                    return Image(rv, width=width or maxWidth or defWidth, height=height or maxHeight or defHeight, fitAfterResize=maxWidth or maxHeight)
                except Exception:
                    return ImagePlaceholder(width or defWidth, height or defHeight)

            def hasThumbnail(self):
                return self.thumbnail != None

            def makeThumbnail(self):
                # Get the screenshot
                screenshot = renpy.game.interface.get_screenshot()
                # Encode it to a base64 string, the important word here is "string" because Python 3 would return b'' from base64.b64encode()...
                self.thumbnail = base64.b64encode(screenshot).decode('utf-8')

            def removeThumbnail(self):
                self.thumbnail = None

            def sequentializeSaves(self):
                current_page = 1
                current_slot = 1
                slots_per_page = Utils.getSlotsPerPage()

                instance = SaveSystem.getPlaythroughSaveInstance(self.id)
                instance.location.scan()

                slots = Utils.getSortedSaves()

                for slot in slots:
                    if(renpy.loadsave.can_load(slot)):
                        newSlot = str(current_page) + '-' + str(current_slot)

                        if(slot != newSlot):
                            renpy.loadsave.rename_save(slot, newSlot)

                        current_slot += 1

                        if(current_slot > slots_per_page):
                            current_slot = 1
                            current_page += 1

            def beforeDeactivation(self):
                self.selectedPage = renpy.store.persistent._file_page
                self.filePageName = renpy.store.persistent._file_page_name

                Playthroughs.save()                        

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
            return self.get(name) or self.add(self.PlaythroughClass(name=name))

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
                if moveSaveDirectory and sourcePlaythrough.name != playthrough.name:
                    result = self.renameSaveDirectory(sourcePlaythrough, Utils.name_to_directory_name(playthrough.name))

                    if result != True:
                        renpy.show_screen("SSSSS_MovePlaythroughDirectoryError", errors=result)
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
                arr.append(playthrough.serializable())

            return json.dumps(arr)

        def saveToUserDir(self):
            UserDir.savePlaythroughs(self.getPlaythroughsAsJson())

        def saveToPersistent(self):
            renpy.store.persistent.SSSSS_playthroughs = self.getPlaythroughsAsJson()
            renpy.store.persistent.SSSSS_playthroughsMtime = int(time.time())

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
            if(self.activePlaythrough != None):
                self.activePlaythrough.beforeDeactivation()

            renpy.store.persistent.SSSSS_lastActivePlaythrough = playthrough.id if playthrough != None else None
            self._activePlaythrough = playthrough

            renpy.store.persistent._file_page = str(playthrough.selectedPage)
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

                renpy.take_screenshot()
                renpy.save(slotString)

                if Settings.pageFollowsQuicksSave:
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
                    message="Sequentialization of a playthrough will rename all your saves, so they start from 1-1 and continue in a sequence without a gap.\nIt may take some time based on the amount of saves and your device.\nThis action {u}{color=[SSSSS.Colors.error]}is irreversible{/c}{/u}. Do you wish to proceed?",
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
                    message="This action will remove {b}{u}all{/u}{/b} your save files for the \"" + name + "\" playthrough.\nThis action {u}{color=[SSSSS.Colors.error]}is irreversible{/c}{/u}. Do you wish to proceed?",
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

                renpy.hide_screen("SSSSS_DuplicatePlaythrough")
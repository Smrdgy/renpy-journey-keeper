init 1 python in SSSSS:
    _constant = True

    import json
    import time

    class PlaythroughsClass():
        _playthroughs = []
        _activePlaythrough = None

        def __init__(self):
            # For some reason the __init__ is called twice in Ren'Py 7.0.0.196.
            # When that happens the playthroughs are loaded twice which led to a buildup of playthroughs when saved. This if should mitigate that.
            if hasattr(renpy.config, "SSSSS_playthroughs_initialized"): return
            renpy.config.SSSSS_playthroughs_initialized = True

            hasNative = False
            if(renpy.store.persistent.SSSSS_playthroughs != None):
                arr = json.loads(renpy.store.persistent.SSSSS_playthroughs)

                for playthrough in arr:
                    if(playthrough.get("id") == 1):
                        hasNative = True

                    self._playthroughs.append(self.createPlaythroughFromSerialization(playthrough))

            if(not hasNative):
                self._playthroughs.insert(0, self.PlaythroughClass(id=1, directory="", name="Native", autosaveOnChoices=False))#MODIFY HERE

        @property
        def playthroughs(self):
            return self._playthroughs

        @property
        def activePlaythrough(self):
            return self._activePlaythrough

        def createPlaythroughFromSerialization(self, data):
            return PlaythroughsClass.PlaythroughClass(id=data.get("id"), directory=data.get("directory"), name=data.get("name"), thumbnail=data.get("thumbnail"), storeChoices=data.get("storeChoices"), layout=data.get("layout"), autosaveOnChoices=data.get("autosaveOnChoices"), selectedPage=data.get("selectedPage"))#MODIFY HERE

        class PlaythroughClass():
            def __init__(self, id=None, directory=None, name=None, thumbnail=None, storeChoices=False, layout="normal", autosaveOnChoices=True, selectedPage=1):#MODIFY HERE
                self.id = id or int(time.time())
                self.directory = directory if (directory != None) else (PlaythroughsClass.name_to_directory_name(name) if name else None)
                self.name = name
                self.thumbnail = thumbnail
                self.storeChoices = storeChoices
                self.layout = layout
                self.autosaveOnChoices = autosaveOnChoices
                self.selectedPage = selectedPage
                #MODIFY HERE

            def copy(self):
                return PlaythroughsClass.PlaythroughClass(self.id, self.directory, self.name, self.thumbnail, self.storeChoices, self.layout, self.autosaveOnChoices, self.selectedPage)#MODIFY HERE

            def edit(self, name=None, thumbnail=None, storeChoices=None, layout=None, autosaveOnChoices=None, selectedPage=None):#MODIFY HERE
                if name != None:
                    self.name = name

                    if(self.directory == None):
                        self.directory = PlaythroughsClass.name_to_directory_name(name)

                if thumbnail != None: self.thumbnail = thumbnail
                if storeChoices != None: self.storeChoices = storeChoices
                if layout != None: self.layout = layout
                if autosaveOnChoices != None: self.autosaveOnChoices = autosaveOnChoices
                if selectedPage != None: self.selectedPage = selectedPage
                #MODIFY HERE

                return self

            def editFromPlaythrough(self, playthrough):
                self.name = playthrough.name

                if(self.directory == None):
                    self.directory = PlaythroughsClass.name_to_directory_name(playthrough.name)

                self.thumbnail = playthrough.thumbnail
                self.storeChoices = playthrough.storeChoices
                self.layout = playthrough.layout
                self.autosaveOnChoices = playthrough.autosaveOnChoices
                self.selectedPage = playthrough.selectedPage

                return self

            def serializable(self):
                return {
                    'id': self.id,
                    'directory': self.directory,
                    'name': self.name,
                    'thumbnail': self.thumbnail,
                    'storeChoices': self.storeChoices,
                    'layout': self.layout,
                    'autosaveOnChoices': self.autosaveOnChoices,
                    'selectedPage': self.selectedPage,
                    #MODIFY HERE
                }

            def getThumbnail(self):
                return None
                # TODO: Complete
                # if(self.thumbnail == None):
                #     return renpy.display.pgrender.surface((2, 2), True)

                # import io

                # try:
                #     # TODO: Fix and uncomment
                #     sio = io.BytesIO(bytes.fromhex(self.thumbnail))
                #     rv = renpy.display.pgrender.load_image(sio, "image.png")
                #     return rv
                # except Exception:
                #     return renpy.display.pgrender.surface((2, 2), True)

            def makeThumbnail(self):
                self.thumbnail = renpy.game.interface.get_screenshot().hex() #TODO: Test, hopefully it won't create a screenshot of the save UI... Also verify the size/speed for let's say 50 or 100 playthroughs


        def add(self, playthrough):
            self._playthroughs.append(playthrough)
            self.activateByInstance(playthrough)

            self.saveToPersistent()
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

        def edit(self, playthrough, originalPlaythrough):
            originalPlaythrough.editFromPlaythrough(playthrough)
                
            self.saveToPersistent()
            renpy.restart_interaction()

            return originalPlaythrough

        def addOrEdit(self, playthrough):
            originalPlaythrough = self.getByID(playthrough.id)
            if(originalPlaythrough != None):
                return self.edit(playthrough, originalPlaythrough)

            return self.add(playthrough)

        def toggleAutosaveOnChoicesOnActive(self):
            self.activePlaythrough.edit(autosaveOnChoices=not self.activePlaythrough.autosaveOnChoices)

            self.saveToPersistent()
            renpy.restart_interaction()

        def activateByName(self, playthroughName):
            self.activateByInstance(self.get(playthroughName))

        def activateByID(self, playthroughID):
            self.activateByInstance(self.getByID(playthroughID))

        def activateByInstance(self, playthrough):
            if(playthrough == None):
                return

            SaveSystem.getOrCreatePlaythroughSaveInstance(playthrough, autoActivate=True)

            self.__setActivePlaythrough(playthrough)

            self.saveToPersistent()
            renpy.restart_interaction()

        def activateNative(self):
            renpy.loadsave.location = SaveSystem.defaultLocation
            renpy.loadsave.clear_cache()

            self.__setActivePlaythrough(None)

            self.saveToPersistent()
            renpy.restart_interaction()

        def activateFirstOrNone(self):
            if(len(self.playthroughs) > 0):
                self.activateByInstance(self.playthroughs[0])
            else:
                self.activateNative()

        @staticmethod
        def name_to_directory_name(title):
            import re

            # Replace spaces and special characters with underscores
            #  Windows does not allow certain characters <>:"/\\|?* in directory names
            directory_name = re.sub(r'[\s<>:"/\\\|\?\*]+', '_', title)
            directory_name = re.sub(r'[^\w.-]', '', directory_name)

            # Make it lowercase
            directory_name = directory_name.lower()

            # Limit the length of the directory name
            max_length = 255  # Maximum file name length for most file systems
            directory_name = directory_name[:max_length]

            # Additional platform-specific adjustments can be added here

            return directory_name

        def saveToPersistent(self):
            arr = []
            for playthrough in self.playthroughs:
                arr.append(playthrough.serializable())

            renpy.store.persistent.SSSSS_playthroughs = json.dumps(arr)

            renpy.save_persistent()

        def getThumbnailFromName(self, playthroughName):
            playthrough = self.get(playthroughName)
        
            if(playthrough != None and playthrough.thumbnail != None):
                return playthrough.getThumbnail()

            return None

        def isValidName(self, name):
            for playthrough in self.playthroughs:
                if(playthrough.name == name):
                    return False

            return True

        def __setActivePlaythrough(self, playthrough=None):
            renpy.store.persistent.SSSSS_lastActivePlaythrough = playthrough.id if playthrough != None else None
            self._activePlaythrough = playthrough

        class ActivateNative(renpy.ui.Action):
            def __call__(self):
                Playthroughs.activateNative()

        class SetThumbnailForActive(renpy.ui.Action):
            def __call__(self):
                playthrough = Playthroughs.activePlaythrough
                playthrough.makeThumbnail()

                Playthroughs.saveToPersistent()
                renpy.restart_interaction()

        class AddOrEdit(renpy.ui.Action):
            def __init__(self, playthrough, name, storeChoices, autosaveOnChoices):#MODIFY HERE
                self.playthrough = playthrough
                self.name = name
                self.storeChoices = storeChoices
                self.autosaveOnChoices = autosaveOnChoices
                #MODIFY HERE

            def __call__(self):
                playthrough = self.playthrough if not callable(self.playthrough) else self.playthrough()
                name = self.name if not callable(self.name) else self.name()
                storeChoices = self.storeChoices if not callable(self.storeChoices) else self.storeChoices()
                autosaveOnChoices = self.autosaveOnChoices if not callable(self.autosaveOnChoices) else self.autosaveOnChoices()
                #MODIFY HERE

                playthrough = playthrough.copy().edit(name=name, storeChoices=storeChoices, autosaveOnChoices=autosaveOnChoices)#MODIFY HERE

                Playthroughs.addOrEdit(playthrough)
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
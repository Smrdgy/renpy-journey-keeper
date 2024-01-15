init 1 python in SSSSS:
    _constant = True

    from collections import OrderedDict
    import json

    class PlaythroughsClass():
        _playthroughs = OrderedDict()
        _activePlaythrough = None

        def __init__(self):
            if(renpy.store.persistent.SSSSS_playthroughs != None):
                print(renpy.store.persistent.SSSSS_playthroughs)
                arr = json.loads(renpy.store.persistent.SSSSS_playthroughs)

                for playthrough in arr:
                    self._playthroughs[playthrough["name"]] = playthrough

        @property
        def playthroughs(self):
            return self._playthroughs

        @property
        def activePlaythrough(self):
            return self._activePlaythrough

        def add(self, directory, name, thumbnail=None, storeChoices=False, layout="normal", autosaveOnChoices=True, selectedPage=1):#MODIFY HERE
            self._playthroughs[name] = self.constructPlaythroughData(directory, name, thumbnail, storeChoices, layout, autosaveOnChoices, selectedPage)#MODIFY HERE
            self.activateByName(name)

            self.saveToPersistent()
            renpy.restart_interaction()

            return self.playthroughs.get(name)

        def get(self, name, substitueIfNotFound=False):
            if(name in self.playthroughs):
                playthrough = self.playthroughs.get(name)

                return self.constructPlaythroughData(playthrough.get("directory"), playthrough.get("name"), playthrough.get("thumbnail"), playthrough.get("storeChoices"), playthrough.get("layout"), playthrough.get("autosaveOnChoices"), playthrough.get("selectedPage"))#MODIFY HERE

            return None

        def getOrAdd(self, name):
            return self.get(name) or self.add(None, name)

        def remove(self, name, removeSaveFiles=False, keepActive=False):
            if(name in self.playthroughs):
                del self.playthroughs[name]

                #TODO: Delete save files if removeSaveFiles is true

                if(keepActive == False):
                    self.activateFirstOrNone()

                return True

            return False

        def edit(self, directory, name, originalName, thumbnail, storeChoices, layout, autosaveOnChoices, selectedPage):
            if(originalName == name and name in self.playthroughs):
                self.playthroughs[name] = self.constructPlaythroughData(directory, name, thumbnail, storeChoices, layout, autosaveOnChoices, selectedPage)#MODIFY HERE
            else:
                self._activePlaythrough = self.add(directory, name, thumbnail, storeChoices, layout, autosaveOnChoices, selectedPage)#MODIFY HERE
                self.remove(originalName, keepActive=True)

                renpy.store.persistent.SSSSS_lastActivePlaythrough = name
                
            self.saveToPersistent()
            renpy.restart_interaction()

            return self.playthroughs.get(name)

        def addOrEdit(self, directory, name, originalName, thumbnail, storeChoices, layout, autosaveOnChoices, selectedPage):#MODIFY HERE
            print("{name} ({originalname}) save", autosaveOnChoices)#TODO: Remove
            if(originalName and self.get(originalName)):
                return self.edit(directory, name, originalName, thumbnail, storeChoices, layout, autosaveOnChoices, selectedPage)#MODIFY HERE

            return self.add(None, name, thumbnail, storeChoices, layout, autosaveOnChoices, selectedPage)#MODIFY HERE

        def toggleAutosaveOnChoicesOnActive(self):
            self.activePlaythrough["autosaveOnChoices"] = not self.activePlaythrough["autosaveOnChoices"]

            self.saveToPersistent()
            renpy.restart_interaction()

        def activateByName(self, playthroughName):
            if(playthroughName in self.playthroughs):
                self.activateByInstance(self.playthroughs.get(playthroughName))

        def activateByInstance(self, playthrough):
            SaveSystem.getOrCreatePlaythroughSaveInstance(playthrough, autoActivate=True)

            renpy.store.persistent.SSSSS_lastActivePlaythrough = playthrough.get("name")
            self._activePlaythrough = playthrough

            self.saveToPersistent()
            renpy.restart_interaction()

        def activateNative(self):
            renpy.loadsave.location = SaveSystem.defaultLocation
            renpy.loadsave.clear_cache()

            renpy.store.persistent.SSSSS_lastActivePlaythrough = None
            self._activePlaythrough = None

            self.saveToPersistent()
            renpy.restart_interaction()

        def activateFirstOrNone(self):
            if(len(self.playthroughs) > 0):
                self.activateByName(next(iter(self.playthroughs)))
            else:
                renpy.store.persistent.SSSSS_lastActivePlaythrough = None
                self._activePlaythrough = None

                self.saveToPersistent()
                renpy.restart_interaction()

        def constructPlaythroughData(self, directory, name, thumbnail=None, storeChoices=False, layout="normal", autosaveOnChoices=True, selectedPage=1):#MODIFY HERE
            print("const", autosaveOnChoices)#TODO: Remove
            return {
                'directory': directory or self.name_to_directory_name(name),
                'name': name,
                'thumbnail': thumbnail,
                'storeChoices': storeChoices,
                'layout': layout, # "normal" -> Grid of thumbnails, "choices" -> list of choices in order
                'autosaveOnChoices': autosaveOnChoices,
                'selectedPage': selectedPage,
                #MODIFY HERE
            }

        def name_to_directory_name(self, title):
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
            for (_, playthrough) in self._playthroughs.items():
                arr.append(playthrough)

            renpy.store.persistent.SSSSS_playthroughs = json.dumps(arr)

            renpy.save_persistent()

        def getThumbnailFromName(self, playthroughName):
            playthrough = self.get(playthroughName)
        
            if(playthrough != None and playthrough.get("thumbnail") != None):
                import io

                # TODO: Fix and uncomment
                # sio = io.BytesIO(playthrough.get("thumbnail"))
                # rv = renpy.display.pgrender.load_image(sio, "image.png")
                # return rv

            return None

        class ActivateNative(renpy.ui.Action):
            def __call__(self):
                Playthroughs.activateNative()

        class SetThumbnailForActive(renpy.ui.Action):
            def __call__(self):
                playthrough = Playthroughs.activePlaythrough
                playthrough["thumbnail"] = renpy.game.interface.get_screenshot() #TODO: Test, hopefully it won't create a screenshot of the save UI... Also verify the size/speed for let's say 50 or 100 playthroughs

                Playthroughs.saveToPersistent()
                renpy.restart_interaction()

        class AddOrEdit(renpy.ui.Action):
            def __init__(self, directory, name, originalName, thumbnail, storeChoices, layout, autosaveOnChoices, selectedPage):#MODIFY HERE
                self.directory = directory
                self.name = name
                self.originalName = originalName
                self.thumbnail = thumbnail
                self.storeChoices = storeChoices
                self.layout = layout
                self.autosaveOnChoices = autosaveOnChoices
                self.selectedPage = selectedPage
                #MODIFY HERE

            def __call__(self):
                directory = self.directory if not callable(self.directory) else self.directory()
                name = self.name if not callable(self.name) else self.name()
                originalName = self.originalName if not callable(self.originalName) else self.originalName()
                thumbnail = self.thumbnail if not callable(self.thumbnail) else self.thumbnail()
                storeChoices = self.storeChoices if not callable(self.storeChoices) else self.storeChoices()
                layout = self.layout if not callable(self.layout) else self.layout()
                autosaveOnChoices = self.autosaveOnChoices if not callable(self.autosaveOnChoices) else self.autosaveOnChoices()
                selectedPage = self.selectedPage if not callable(self.selectedPage) else self.selectedPage()
                #MODIFY HERE

                Playthroughs.addOrEdit(directory, name, originalName, thumbnail, storeChoices, layout, autosaveOnChoices, selectedPage)#MODIFY HERE
                renpy.restart_interaction()

        class ActivatePlaythrough(renpy.ui.Action):
            def __init__(self, playthroughName):
                self.playthroughName = playthroughName

            def __call__(self):
                Playthroughs.activateByName(self.playthroughName)
                renpy.restart_interaction()

        class Remove(renpy.ui.Action):
            def __init__(self, playthroughName, deleteSaves):
                self.playthroughName = playthroughName
                self.deleteSaves = deleteSaves

            def __call__(self):
                Playthroughs.remove(self.playthroughName)
                renpy.restart_interaction()

        class ToggleAutosaveOnChoicesOnActive(renpy.ui.Action):
            def __call__(self):
                Playthroughs.toggleAutosaveOnChoicesOnActive()
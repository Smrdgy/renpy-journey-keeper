init python in JK:
    _constant = True

    import os
    from collections import OrderedDict

    class SaveSystemClass(x52NonPicklable):
        def __init__(self):
            self._playthroughSaves = OrderedDict()
            self.multilocation = MultiLocation()

            renpy.loadsave.location = self.multilocation

        def getPlaythroughSaveInstance(self, playthroughID):
            return self._playthroughSaves.get(playthroughID)

        def getOrCreatePlaythroughSaveInstanceByID(self, playthroughID, autoActivate=False):
            playthrough = Playthroughs.getByID(playthroughID)
            if playthrough:
                return self.getOrCreatePlaythroughSaveInstance(playthrough, autoActivate=autoActivate)

            return None

        def overrideNativeLocation(self):
            renpy.loadsave.location = self.multilocation

        def getAllNativeSaveLocations(self):
            return self.multilocation.nativeLocations

        def getAllNativeSaveLocationsForOptions(self):
            options = []

            # 1. User savedir.
            options.append("USER")

            # 2. Game-local savedir.
            if (not renpy.mobile) and (not renpy.macapp):
                options.append("GAME")

            # 3. Extra savedirs.
            if hasattr(renpy.config, "extra_savedirs"):
                for fullPath in renpy.config.extra_savedirs:
                    options.append(fullPath)

            return options

        class PlaythroughSaveClass(x52NonPicklable):
            def __init__(self, playthrough, noScan=False):
                self.location = MultiLocation()
                self.playthrough = playthrough

                # 1. User savedir.
                if playthrough.enabledSaveLocations == None or "USER" in playthrough.enabledSaveLocations:
                    self._addLocation(FileLocation(os.path.join(renpy.config.savedir, playthrough.directory)))

                # 2. Game-local savedir.
                if (not renpy.mobile) and (not renpy.macapp) and (playthrough.enabledSaveLocations == None or "GAME" in playthrough.enabledSaveLocations):
                    path = os.path.join(renpy.config.gamedir, "saves", playthrough.directory)
                    self._addLocation(FileLocation(path))

                if(hasattr(renpy.config, "extra_savedirs")):
                    # 3. Extra savedirs.
                    for extra_savedir in renpy.config.extra_savedirs:
                        if playthrough.enabledSaveLocations == None or extra_savedir in playthrough.enabledSaveLocations:
                            self._addLocation(FileLocation(os.path.join(extra_savedir, playthrough.directory)))

                if not noScan:
                    # Scan the location.
                    SaveSystem.multilocation.scan()

            # Makes this playthrough locations active for load/save
            def activate(self):
                # For some reason Exciting Games running on RenPy v7.7.1.24030407 retains native location.
                # This will fix the location every time a playthrough is activated, just in case...
                SaveSystem.overrideNativeLocation()
                SaveSystem.multilocation.deactivateLocations()

                self.location.activateLocations()

                renpy.loadsave.clear_cache()
                SaveSystem.multilocation.scan()

            def deactivate(self):
                self.location.deactivateLocations()

            def deleteFiles(self):
                import shutil

                for location in self.location.locations:
                    shutil.rmtree(location.directory)

            def deleteSaveFiles(self, scan=True):
                self.location.unlink_all(scan=False)

                if scan:
                    SaveSystem.multilocation.scan()

            def _addLocation(self, fileLocation):
                fileLocation.active = False
                SaveSystem.multilocation.add(fileLocation)
                self.location.add(fileLocation)

            def listAllSaves(self):
                return self.location.list_including_inactive()

        def createPlaythroughSaveInstance(self, playthrough, noScan=False):
            self._playthroughSaves[playthrough.id] = SaveSystemClass.PlaythroughSaveClass(playthrough, noScan)
            
            return self._playthroughSaves.get(playthrough.id)

        def getOrCreatePlaythroughSaveInstance(self, playthrough, autoActivate=False):
            instance = self.getPlaythroughSaveInstance(playthrough.id)

            if instance == None:
                instance = self.createPlaythroughSaveInstance(playthrough)

            if instance.playthrough.enabledSaveLocations != playthrough.enabledSaveLocations:
                instance = self.createPlaythroughSaveInstance(playthrough)

            if autoActivate:
                instance.activate()

            return instance

        def removeSaveFilesForPlaythrough(self, playthrough, remove_dir=False):
            instance = self.getOrCreatePlaythroughSaveInstance(playthrough)
            if instance == None:
                return False

            instance.deleteSaveFiles(scan=False)

            if remove_dir:
                instance.location.remove_dir()

                self.removeInstance(instance)
            else:
                instance.scan()

            return True

        def removePlaythroughSaveInstance(self, playthrough):
            oldInstance = self.getPlaythroughSaveInstance(playthrough.id)
            if oldInstance != None:
                self.removeInstance(oldInstance)

        def removeInstance(self, instance):
            for location in instance.location.locations:
                SaveSystem.multilocation.remove(location)

            for playthrough_id in self._playthroughSaves:
                if self._playthroughSaves[playthrough_id] == instance:
                    del self._playthroughSaves[playthrough_id]
                    break

        def regeneratePlaythroughSaveInstance(self, playthrough, noScan=False, autoActivate=True):
            self.removePlaythroughSaveInstance(playthrough)

            instance = self.createPlaythroughSaveInstance(playthrough, noScan)

            if autoActivate:
                instance.activate()

        def listAllSavesForPlaythrough(self, playthrough):
            instance = self.getPlaythroughSaveInstance(playthrough.id)
            if instance:
                return instance.listAllSaves()

            return Set()
            
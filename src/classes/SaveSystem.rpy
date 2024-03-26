init 1 python in SSSSS:
    _constant = True

    import os
    from collections import OrderedDict

    class MultiLocation(renpy.savelocation.MultiLocation):
        def __init__(self):
            super(MultiLocation, self).__init__()

            self.nativeLocations = renpy.loadsave.location.locations

        def add(self, location):
            self.locations.append(location)

        def activateLocations(self):
            for location in self.locations:
                location.active = True

        def deactivateLocations(self):
            for location in self.locations:
                location.active = False

        def load_persistent(self):
            rv = []

            for l in self.nativeLocations:
                rv.extend(l.load_persistent())

            return rv

        def save_persistent(self, data):
            for l in self.nativeLocations:
                l.save_persistent(data)

    class SaveSystemClass():
        multilocation = MultiLocation()

        _playthroughSaves = OrderedDict()
        _activePlaythroughSave = None

        def __init__(self):
            renpy.loadsave.location = self.multilocation

        def setupLocations(self):
            playthroughs = Playthroughs.playthroughs

            for playthrough in playthroughs:
                self.createPlaythroughSaveInstance(playthrough, noScan=True)

            SaveSystem.multilocation.scan()

        def getPlaythroughSaveInstance(self, playthroughID):
            return self._playthroughSaves.get(playthroughID)

        class PlaythroughSaveClass():
            def __init__(self, playthrough, noScan=False):
                self.location = MultiLocation()
                self.playthrough = playthrough

                # 1. User savedir.
                self._addLocation(renpy.savelocation.FileLocation(os.path.join(renpy.config.savedir, playthrough.directory)))

                # 2. Game-local savedir.
                if (not renpy.mobile) and (not renpy.macapp):
                    path = os.path.join(renpy.config.gamedir, "saves", playthrough.directory)
                    self._addLocation(renpy.savelocation.FileLocation(path))

                if(hasattr(renpy.config, "extra_savedirs")):
                    # 3. Extra savedirs.
                    for extra_savedir in renpy.config.extra_savedirs:
                        self._addLocation(renpy.savelocation.FileLocation(os.path.join(extra_savedir, playthrough.directory)))

                if not noScan:
                    # Scan the location.
                    SaveSystem.multilocation.scan()

            # Makes this playthrough locations active for load/save
            def activate(self):
                SaveSystem.multilocation.deactivateLocations()

                for location in self.location.locations:
                    location.active = True

                renpy.loadsave.clear_cache()
                SaveSystem.multilocation.scan()
                renpy.store.persistent.SSSSS_lastActivePlaythrough = self.playthrough.id
                SaveSystem._activePlaythroughSave = self

            def deactivate(self):
                for location in self.location.locations:
                    location.active = False

            def deleteFiles(self):
                import shutil

                for location in self.location.locations:
                    shutil.rmtree(location.directory)

            def _addLocation(self, fileLocation):
                fileLocation.active = False
                SaveSystem.multilocation.add(fileLocation)
                self.location.add(fileLocation)

        def createPlaythroughSaveInstance(self, playthrough, noScan=False):
            self._playthroughSaves[playthrough.id] = SaveSystemClass.PlaythroughSaveClass(playthrough, noScan)
            
            return self._playthroughSaves.get(playthrough.id)

        def getOrCreatePlaythroughSaveInstance(self, playthrough, autoActivate=True):
            instance = self.getPlaythroughSaveInstance(playthrough.id)

            if(instance == None):
                instance = self.createPlaythroughSaveInstance(playthrough)

            if(autoActivate):
                instance.activate()

        def removeFilesForPlaythrough(self, playthrough):
            instance = self.getPlaythroughSaveInstance(playthrough.id)

            if(instance == None):
                return False

            instance.deleteFiles()

            return True
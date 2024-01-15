init 1 python in SSSSS:
    _constant = True

    import os
    from collections import OrderedDict

    class SaveSystemClass():
        _playthroughSaves = OrderedDict()

        # Default location for the game
        _defaultLocation = renpy.loadsave.location

        def __init__(self):
            self.setupLocations()

        @property
        def defaultLocation(self):
            return self._defaultLocation

        def setupLocations(self):
            playthroughs = Playthroughs.playthroughs.items()

            for (_, playthrough) in playthroughs:
                self.createPlaythroughSaveInstance(playthrough)

        def useDefault(self):
            renpy.loadsave.location = self._defaultLocation

        def getPlaythroughSaveInstance(self, playthroughName):
            return self._playthroughSaves.get(playthroughName)

        class PlaythroughSaveClass():
            def __init__(self, playthrough):
                self.playthrough = playthrough

                location = renpy.savelocation.MultiLocation()

                # 1. User savedir.
                location.add(renpy.savelocation.FileLocation(os.path.join(renpy.config.savedir, playthrough.get("directory"))))

                # 2. Game-local savedir.
                if (not renpy.mobile) and (not renpy.macapp):
                    path = os.path.join(renpy.config.gamedir, "saves", playthrough.get("directory"))
                    location.add(renpy.savelocation.FileLocation(path))

                # 3. Extra savedirs.
                for extra_savedir in renpy.config.extra_savedirs:
                    location.add(renpy.savelocation.FileLocation(os.path.join(extra_savedir, playthrough.get("directory"))))

                # Scan the location once.
                location.scan()

                self.location = location

            def save(self, slotname, record):
                self.location.save(slotname, record)
            
            def load(self):
                self.location.save(slotname)

            # Makes this playthrough location active for load/save
            def activate(self):
                renpy.loadsave.location = self.location
                renpy.loadsave.clear_cache()
                renpy.store.persistent.SSSSS_lastActivePlaythrough = self.playthrough.get("name")

        def createPlaythroughSaveInstance(self, playthrough):
            self._playthroughSaves[playthrough.get("name")] = SaveSystemClass.PlaythroughSaveClass(playthrough)
            
            return self._playthroughSaves.get(playthrough.get("name"))

        def getOrCreatePlaythroughSaveInstance(self, playthrough, autoActivate=True):
            instance = self.getPlaythroughSaveInstance(playthrough.get("name"))

            if(instance == None):
                instance = self.createPlaythroughSaveInstance(playthrough)

            if(autoActivate):
                instance.activate()

        
            
            
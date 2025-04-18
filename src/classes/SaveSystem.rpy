init python in JK:
    _constant = True

    import os
    from collections import OrderedDict

    class SaveSystemClass(x52NonPicklable):
        def __init__(self):
            self._playthrough_save_class_dict = OrderedDict()
            self.multilocation = MultiLocation()

            renpy.loadsave.location = self.multilocation

        def get_playthrough_save_instance(self, playthroughID):
            return self._playthrough_save_class_dict.get(playthroughID)

        def get_or_create_playthrough_save_instance_by_id(self, playthroughID, autoActivate=False):
            playthrough = Playthroughs.get_by_id(playthroughID)
            if playthrough:
                return self.get_or_create_playthrough_save_instance(playthrough, autoActivate=autoActivate)

            return None

        def override_native_location(self):
            renpy.loadsave.location = self.multilocation

        def get_all_native_save_locations(self):
            return self.multilocation.nativeLocations

        def get_all_native_save_locations_for_options(self):
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

        def create_playthrough_save_instance(self, playthrough, noScan=False):
            self._playthrough_save_class_dict[playthrough.id] = SaveSystemClass.PlaythroughSaveClass(playthrough, noScan)
            
            return self._playthrough_save_class_dict.get(playthrough.id)

        def get_or_create_playthrough_save_instance(self, playthrough, autoActivate=False):
            instance = self.get_playthrough_save_instance(playthrough.id)

            if instance == None:
                instance = self.create_playthrough_save_instance(playthrough)

            if instance.playthrough.enabledSaveLocations != playthrough.enabledSaveLocations:
                instance = self.create_playthrough_save_instance(playthrough)

            if autoActivate:
                instance.activate()

            return instance

        def remove_save_files_for_playthrough(self, playthrough, remove_dir=False):
            instance = self.get_or_create_playthrough_save_instance(playthrough)
            if instance == None:
                return False

            instance.delete_save_files(scan=False)

            if remove_dir:
                instance.location.remove_dir()

                self.remove_instance(instance)
            else:
                instance.location.scan()

            return True

        def removePlaythroughSaveInstance(self, playthrough):
            oldInstance = self.get_playthrough_save_instance(playthrough.id)
            if oldInstance != None:
                self.remove_instance(oldInstance)

        def remove_instance(self, instance):
            for location in instance.location.locations:
                SaveSystem.multilocation.remove(location)

            for playthrough_id in self._playthrough_save_class_dict:
                if self._playthrough_save_class_dict[playthrough_id] == instance:
                    del self._playthrough_save_class_dict[playthrough_id]
                    break

        def regenerate_playthrough_save_instance(self, playthrough, noScan=False, autoActivate=True):
            self.removePlaythroughSaveInstance(playthrough)

            instance = self.create_playthrough_save_instance(playthrough, noScan)

            if autoActivate:
                instance.activate()

        def list_all_saves_for_playthrough(self, playthrough):
            instance = self.get_playthrough_save_instance(playthrough.id)
            if instance:
                return instance.listAllSaves()

            return []

        def get_last_page(self):
            if self.multilocation.last_page_cache:
                return self.multilocation.last_page_cache

            savename = Utils.get_sorted_saves()[-1]
            if savename:
                page, _ = Utils.split_slotname(savename)
                self.multilocation.last_page_cache = page
                return page
            
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
                SaveSystem.override_native_location()
                SaveSystem.multilocation.deactivate_locations()

                self.location.activate_locations()

                renpy.loadsave.clear_cache()
                SaveSystem.multilocation.scan()

            def deactivate(self):
                self.location.deactivate_locations()

            def deleteFiles(self):
                import shutil

                for location in self.location.locations:
                    shutil.rmtree(location.directory)

            def delete_save_files(self, scan=True):
                self.location.unlink_all(scan=False)

                if scan:
                    SaveSystem.multilocation.scan()

            def _addLocation(self, fileLocation):
                fileLocation.active = False
                SaveSystem.multilocation.add(fileLocation)
                self.location.add(fileLocation)

            def listAllSaves(self):
                return self.location.list_including_inactive()
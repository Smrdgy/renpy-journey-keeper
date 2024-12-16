init 1 python in URPS:
    _constant = True

    class PlaythroughClass(x52NonPicklable):
        def __init__(self, id=None, directory=None, name=None, description=None, thumbnail=None, storeChoices=False, autosaveOnChoices=True, selectedPage=1, filePageName={}, useChoiceLabelAsSaveName=False, enabledSaveLocations=None):#MODIFY HERE
            self.id = id or int(time.time())
            self.directory = directory if (directory != None) else (Utils.name_to_directory_name(name) if name else None)
            self.name = name
            self.description = description
            self.thumbnail = thumbnail
            self.storeChoices = storeChoices
            self.autosaveOnChoices = autosaveOnChoices
            self.selectedPage = selectedPage
            self.filePageName = filePageName
            self.useChoiceLabelAsSaveName = useChoiceLabelAsSaveName
            self.enabledSaveLocations = enabledSaveLocations # Possible values: USER, GAME, string (other full path locations, e.g. C:\\Users\User\Desktop\some saves directory)
            #MODIFY HERE

        def __getstate__(self):
            return None

        def copy(self):
            return PlaythroughClass(self.id, self.directory, self.name, self.description, self.thumbnail, self.storeChoices, self.autosaveOnChoices, self.selectedPage, self.filePageName, self.useChoiceLabelAsSaveName, self.enabledSaveLocations)#MODIFY HERE

        def edit(self, name=None, description=None, thumbnail=None, storeChoices=None, autosaveOnChoices=None, selectedPage=None, filePageName=None, useChoiceLabelAsSaveName=None, enabledSaveLocations=None):#MODIFY HERE
            if name != None:
                self.name = name

                if(self.directory == None):
                    self.directory = Utils.name_to_directory_name(name)

            if description != None: self.description = description
            if thumbnail != None: self.thumbnail = thumbnail
            if storeChoices != None: self.storeChoices = storeChoices
            if autosaveOnChoices != None: self.autosaveOnChoices = autosaveOnChoices
            if selectedPage != None: self.selectedPage = selectedPage
            if filePageName != None: self.filePageName = filePageName
            if useChoiceLabelAsSaveName != None: self.useChoiceLabelAsSaveName = useChoiceLabelAsSaveName
            if enabledSaveLocations != None: self.enabledSaveLocations = enabledSaveLocations or None #enabledSaveLocations can be False, in that case it needs to be replaced with None
            #MODIFY HERE

            return self

        def editFromPlaythrough(self, playthrough, moveSaveDirectory=False):
            if(self.directory == None or (moveSaveDirectory and playthrough.name != self.name and playthrough.id != 1)):
                self.directory = Utils.name_to_directory_name(playthrough.name)

            self.name = playthrough.name
            self.description = playthrough.description
            self.thumbnail = playthrough.thumbnail
            self.storeChoices = playthrough.storeChoices
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
                'autosaveOnChoices': self.autosaveOnChoices,
                'selectedPage': self.selectedPage,
                'filePageName': self.filePageName,
                'useChoiceLabelAsSaveName': self.useChoiceLabelAsSaveName,
                'enabledSaveLocations': self.enabledSaveLocations,
                #MODIFY HERE
            }

        def serializable_for_template(self):
            return {
                'name': self.name,
                'description': self.description,
                'storeChoices': self.storeChoices,
                'autosaveOnChoices': self.autosaveOnChoices,
                'useChoiceLabelAsSaveName': self.useChoiceLabelAsSaveName,
                'enabledSaveLocations': self.enabledSaveLocations,
                #MODIFY HERE
            }

        def getThumbnail(self, width=None, height=None, maxWidth=None, maxHeight=None):
            return SmrdgyLib.image.get_b64_thumbnail_displayable(self.thumbnail, width, height, maxWidth or 150, maxHeight or 150)

        def hasThumbnail(self):
            return self.thumbnail != None

        def makeThumbnail(self):
            self.thumbnail = SmrdgyLib.image.make_b64_thumbnail()

        def removeThumbnail(self):
            self.thumbnail = None

        def sequentializeSaves(self):
            current_page = 1
            current_slot = 1
            slots_per_page = Utils.getSlotsPerPage()

            instance = SaveSystem.getPlaythroughSaveInstance(self.id)
            instance.location.scan()

            slots = SmrdgyLib.save.sorted_saves()

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
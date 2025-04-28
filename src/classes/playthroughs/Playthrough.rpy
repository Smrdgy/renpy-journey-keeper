init python in JK:
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

        def regenerate_unique_data(self):
            self.id = int(time.time())
            self.directory = Utils.name_to_directory_name(self.name)

            return self

        def copy(self):
            return PlaythroughClass.from_json_string(self.serialize_to_json_string())

        def remove_unique_data(self):
            self.id = int(time.time())
            self.directory = None

            return self

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

        def edit_from_playthrough(self, playthrough, moveSaveDirectory=False):
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

        def serialize_for_json(self):
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

        def serialize_template_for_json(self):
            return {
                'name': self.name,
                'description': self.description,
                'storeChoices': self.storeChoices,
                'autosaveOnChoices': self.autosaveOnChoices,
                'useChoiceLabelAsSaveName': self.useChoiceLabelAsSaveName,
                'enabledSaveLocations': self.enabledSaveLocations,
                #MODIFY HERE
            }

        def serialize_to_json_string(self):
            return json.dumps(self.serialize_for_json())

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

        def make_thumbnail(self):
            # Get the screenshot
            screenshot = renpy.game.interface.get_screenshot()
            # Encode it to a base64 string, the important word here is "string" because Python 3 would return b'' from base64.b64encode()...
            self.thumbnail = base64.b64encode(screenshot).decode('utf-8')

            return self

        def removeThumbnail(self):
            self.thumbnail = None

        def sequentializeSaves(self):
            current_page = 1
            current_slot = 1
            slots_per_page = Utils.get_slots_per_page()

            instance = SaveSystem.get_playthrough_save_instance(self.id)
            instance.location.scan()

            slots = Utils.get_sorted_saves()

            for slot in slots:
                if(renpy.loadsave.can_load(slot)):
                    newSlot = str(current_page) + '-' + str(current_slot)

                    if(slot != newSlot):
                        renpy.loadsave.rename_save(slot, newSlot)

                    current_slot += 1

                    if(current_slot > slots_per_page):
                        current_slot = 1
                        current_page += 1

        def before_deactivation(self):
            self.selectedPage = renpy.store.persistent._file_page
            self.filePageName = renpy.store.persistent._file_page_name

            Playthroughs.save()

        @staticmethod
        def from_dict(data):
            return PlaythroughClass(id=data.get("id"), directory=data.get("directory"), name=data.get("name"), description=data.get("description"), thumbnail=data.get("thumbnail"), storeChoices=data.get("storeChoices"), autosaveOnChoices=data.get("autosaveOnChoices"), selectedPage=data.get("selectedPage"), filePageName=data.get("filePageName"), useChoiceLabelAsSaveName=data.get("useChoiceLabelAsSaveName"), enabledSaveLocations=data.get("enabledSaveLocations"))#MODIFY HERE

        @staticmethod
        def from_json_string(json_string):
            return PlaythroughClass.from_dict(json.loads(json_string))

        @staticmethod
        def create_native():
            return PlaythroughClass(id=1, directory="", name="Native", autosaveOnChoices=False, useChoiceLabelAsSaveName=False)#MODIFY HERE

        @staticmethod
        def create_memories():
            return PlaythroughClass(id=2, directory="_memories", name="Memories", autosaveOnChoices=False, useChoiceLabelAsSaveName=False)#MODIFY HERE
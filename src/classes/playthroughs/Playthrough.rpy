init python in JK:
    _constant = True

    new_playthrough_instance_callbacks = []

    class PlaythroughClass(x52NonPicklable):
        DEFAULTS = {
            "id": None,
            "directory": None,
            "name": None,
            "description": None,
            "thumbnail": None,
            "storeChoices": False,
            "autosaveOnChoices": True,
            "selectedPage": 1,
            "filePageName": {},
            "useChoiceLabelAsSaveName": False,
            "enabledSaveLocations": None, # Possible values: USER, GAME, string (other full path locations, e.g. C:\\Users\User\Desktop\some saves directory)
            "meta": None,
            "native": False,
            "directory_immovable": False,
            "hidden": False,
            "serializable": True,
            "deletable": True,
            #MODIFY HERE
        }

        def __init__(self, **kwargs):
            # Start with a copy of the defaults
            opts = self.DEFAULTS.copy()
            opts.update((k, v) for k, v in kwargs.items() if v is not None)

            # Special handling
            opts["id"] = opts["id"] or int(time.time())
            if opts.get("directory") is None and opts.get("name"):
                opts["directory"] = Utils.name_to_directory_name(opts["name"])

            # Avoid shared mutable default
            opts["filePageName"] = opts.get("filePageName") or {}

            # Set all attributes to the instance
            for key in self.DEFAULTS:
                setattr(self, key, opts[key])

            for cb in new_playthrough_instance_callbacks:
                if callable(cb):
                    cb(self)

        def __getstate__(self):
            return None

        def regenerate_unique_data(self):
            self.id = int(time.time())
            self.directory = Utils.name_to_directory_name(self.name)

            return self

        def copy(self):
            return PlaythroughClass.from_json_string(self.serialize_to_json_string(ignore_serializable=True))

        def remove_unique_data(self):
            self.id = int(time.time())
            self.directory = None

            return self

        def edit(self, **kwargs):
            for key, value in kwargs.items():
                if key not in self.DEFAULTS:
                    if Settings.debugEnabled:
                        print("Playthrough \"{}\" tried to set an unknown key: {}".format(self.name, key))
                        renpy.notify("Playthrough tried to set an unknown key: {}".format(key))
                    continue

                if key == "name" and value is not None:
                    self.name = value
                    if self.directory is None:
                        self.directory = Utils.name_to_directory_name(value)

                elif key == "enabledSaveLocations":
                    #enabledSaveLocations can be False, in that case it needs to be replaced with None
                    self.enabledSaveLocations = value or None

                elif value is not None:
                    setattr(self, key, value)

            return self

        def edit_from_playthrough(self, playthrough, moveSaveDirectory=False):
            if self.directory is None or (moveSaveDirectory and playthrough.name != self.name and not playthrough.directory_immovable):
                self.directory = Utils.name_to_directory_name(playthrough.name)

            for key in self.DEFAULTS:
                setattr(self, key, getattr(playthrough, key))

            return self

        def serialize_for_json(self, ignore_serializable=False):
            if not self.serializable and not ignore_serializable:
                if Settings.debugEnabled:
                    raise Exception("Playthrough \"{}\" was set as NOT serializable but still got to the serialization!".format(self.name))

                return None

            return { key: getattr(self, key) for key in self.DEFAULTS }

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

        def serialize_to_json_string(self, ignore_serializable=False):
            return json.dumps(self.serialize_for_json(ignore_serializable=ignore_serializable))

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
            return PlaythroughClass(**{
                k: v for k, v in data.items()
                if k in PlaythroughClass.DEFAULTS
            })

        @staticmethod
        def from_json_string(json_string):
            return PlaythroughClass.from_dict(json.loads(json_string))

        @staticmethod
        def create_native():
            return PlaythroughClass(id=1, directory="", name="Native", native=True, directory_immovable=True, deletable=False)#MODIFY HERE

        @staticmethod
        def create_memories():
            return PlaythroughClass(id=2, directory="_memories", name="Memories", directory_immovable=True, hidden=True, serializable=True, deletable=False)#MODIFY HERE
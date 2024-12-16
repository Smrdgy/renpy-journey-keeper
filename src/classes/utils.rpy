init -2000 python in URPS:
    _constant = True

    import re
    import shutil
    import os
    import threading
    disk_lock = threading.RLock()
    import unicodedata
    import sys

    class x52NonPicklable(python_object):
        def __setstate__(self, d):
            pass
        def __getstate__(self):
            return {}
        def __getnewargs__(self):
            return ()
        def __iter__(self):
            return None
        def itervalues(self):
            return None

    class Utils(x52NonPicklable):
        @staticmethod
        def name_to_directory_name(title):
            import re

            # Define invalid characters and their replacements
            replacements = {
                ':': '；',  # full-width semicolon
                '/': '／',  # full-width solidus
                '\\': '／',  # full-width solidus
                '<': '‹',   # single left-pointing angle quotation mark
                '>': '›',   # single right-pointing angle quotation mark
                '*': '＊',  # full-width asterisk
                '?': '？',  # full-width question mark
                '"': '＂',  # full-width quotation mark
                '|': 'ǀ'    # Latin letter dental click
            }

            # Create a regex pattern to match any invalid character
            pattern = re.compile('|'.join(re.escape(char) for char in replacements.keys()))
            
            # Function to replace invalid characters
            def replace_invalid_char(match):
                return replacements[match.group(0)]

            directory_name = pattern.sub(replace_invalid_char, title)

            # Limit the length of the directory name
            max_length = 255  # Maximum file name length for most file systems
            directory_name = directory_name[:max_length]

            # Additional platform-specific adjustments can be added here

            return directory_name

        @staticmethod
        def createSaveRecord(extra_info=None):
            roots = renpy.game.log.freeze(None)

            extra_info = extra_info or ""

            if renpy.config.save_dump:
                renpy.loadsave.save_dump(roots, renpy.game.log)

            logf = io.BytesIO()

            try:
                renpy.loadsave.dump((roots, renpy.game.log), logf)
            except:
                t, e, tb = sys.exc_info()

                try:
                    bad = renpy.loadsave.find_bad_reduction(roots, renpy.game.log)
                except:
                    print("Autosave failure: ", t, e, tb)
                    renpy.notify("Autosave failed. Check log.txt for more info.")
                    return

                if bad is None:
                    print("Autosave failure: ", t, e, tb)
                    renpy.notify("Autosave failed. Check log.txt for more info.")
                    return

                if e.args:
                    e.args = (e.args[0] + ' (perhaps {})'.format(bad),) + e.args[1:]

                print("Autosave failure: ", t, e, tb)
                renpy.notify("Autosave failed. Check log.txt for more info.")
                return

            json = { "_save_name" : extra_info, "_renpy_version" : list(renpy.version_tuple), "_version" : renpy.config.version }

            for i in renpy.config.save_json_callbacks:
                i(json)

            json = json_dumps(json)

            return renpy.loadsave.SaveRecord(None, extra_info, json, logf.getvalue())

        @staticmethod
        def getSlotsPerPage():
            if Settings.customGridEnabled:
                return Settings.customGridX * Settings.customGridY

            if Utils.hasColsAndRowsConfiguration():
                return renpy.store.gui.file_slot_cols * renpy.store.gui.file_slot_rows

            return 4

        @staticmethod
        def hasColsAndRowsConfiguration():
            if Settings.customGridEnabled:
                return True

            return hasattr(renpy.store.gui, "file_slot_cols") and hasattr(renpy.store.gui, "file_slot_rows")

        @staticmethod
        def isDisplayingChoices():
            try:
                current = renpy.game.context().current
                script = renpy.game.script.lookup(current)
                return isinstance(script, renpy.ast.Menu)
            except:
                return False

        @staticmethod
        def isDisplayingMultipleChoices():
            try:
                current = renpy.game.context().current
                script = renpy.game.script.lookup(current)
                if isinstance(script, renpy.ast.Menu):
                    available_count = 0
                    for item in script.items:
                        if len(item) > 2 and item[2]:
                            if eval(item[1], renpy.store.__dict__):
                                available_count += 1

                            if available_count > 1:
                                return True

                    return False
            except:
                return False

        @staticmethod
        def isDisplayingChoicesInAnyContext():
            try:
                for context in renpy.game.contexts:
                    script = renpy.game.script.lookup(context.current)
                    if isinstance(script, renpy.ast.Menu):
                        return True
            except Exception as e:
                print(e)

            return False

        @staticmethod
        def filter_timeline(timeline, search):
            if search is None or search == "":
                return timeline

            # Normalize strings to remove accents
            def normalize(text):
                if isinstance(text, str):
                    text = text.decode('utf-8') if sys.version_info[0] < 3 else text
                return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')

            normalized_search = normalize(search).lower()

            filtered = []
            for entry in timeline:
                if not isinstance(entry, tuple) or len(entry) < 2:
                    continue  # Skip invalid entries
                text = entry[1]
                if text is None:
                    continue  # Skip entries with None in index 1
                if normalized_search in normalize(text).lower():
                    filtered.append(entry)

            return filtered

        @staticmethod
        def is_save_load_screen():
            for screen in ["save", "load"] + Settings.saveScreenName + Settings.loadScreenName:
                if renpy.get_screen(screen) != None:
                    return True
            
            return False

        @staticmethod
        def list_save_directories():
            dir_names = set()
            directories = set()

            for location in renpy.loadsave.location.nativeLocations:
                for item_name in os.listdir(location.directory):
                    if item_name not in dir_names:
                        path = os.path.join(location.directory, item_name)

                        if os.path.isdir(path):
                            directories.add((item_name, path))
                            dir_names.add(item_name)

            return directories

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
        
        def remove(self, location):
            self.locations.remove(location)

        def newest_including_inactive(self, slotname):
            """
            Same logic as newest(), but this one includes locations with active=False.
            """

            mtime = -1
            location = None

            for l in self.locations:
                slot_mtime = l.mtime(slotname)

                if slot_mtime > mtime:
                    mtime = slot_mtime
                    location = l

            return location

        def has_save(self, slotname, check_inactive=True):
            if check_inactive:
                return self.newest_including_inactive(slotname) != None

            return self.newest(slotname) != None

        def screenshot_including_inactive(self, slotname):
            l = self.newest_including_inactive(slotname)

            if l is None:
                return None

            return l.screenshot(slotname)

        def unlink_save(self, slotname, include_inactive=True, scan=True):
            for l in (self.locations if include_inactive else self.active_locations()):
                l.unlink_save(slotname, scan)

        def list_including_inactive(self):
            self.scan()

            rv = set()

            for l in self.locations:
                original_active = l.active
                l.active = True
                l.scan()

                rv.update(l.list())

                l.active = original_active

            return list(rv)

        def copy_save_into_other_multilocation(self, save, multilocation, scan=True):
            for l in multilocation.locations:
                self.copy_save_into_other_location(save, l, scan)

            if scan:
                self.scan()

        def copy_save_into_other_location(self, save, location, scan=True):
            for l in self.locations:
                l.copy_into_other_directory(save, save, location.directory, scan=False)
            
            if scan:
                self.scan()

        def unlink_all(self, scan=True):
            for l in self.active_locations():
                for save in l.list():
                    l.unlink_save(save, scan=False)
            
            if scan:
                self.scan()

        def copy_all_saves_into_other_multilocation(self, multilocation, include_inactive=True, scan=True):
            target_locations = multilocation.locations if include_inactive else multilocation.active_locations()
            source_locations = self.locations if include_inactive else self.active_locations()

            with disk_lock:
                for i in range(0, len(target_locations)):
                    source_location = source_locations[i]
                    if not source_location:
                        raise Exception("Source location not found")

                    target_location = target_locations[i]
                    if not target_location:
                        raise Exception("Target location not found")

                    shutil.rmtree(target_location.directory) # Clear anything that is already there and also remove the root directory, otherwise shutil.copytree would throw an exception...

                    try:
                        shutil.copytree(source_location.directory, target_location.directory)
                    except Exception as e:
                        print(e)
                        return False

                if scan:
                    multilocation.scan()

                return True

    class FileLocation(renpy.savelocation.FileLocation):
        def copy_into_other_directory(self, old, new, destination, scan=True):
            with disk_lock:
                old = self.filename(old)

                if not os.path.exists(old):
                    return

                new = os.path.join(destination, renpy.exports.fsencode(new + renpy.savegame_suffix))

                shutil.copyfile(old, new)

                if scan:
                    self.scan()

        def unlink_save(self, slotname, scan=True):
            with disk_lock:
                filename = self.filename(slotname)
                if os.path.exists(filename):
                    os.unlink(filename)

                if scan:
                    self.scan()

        def name(self):
            if renpy.config.savedir in self.directory:
                return "User data"

            if renpy.config.gamedir in self.directory:
                return "Game"

            return self.directory
    
    class SetKey(renpy.ui.Action):
        def __init__(self, key, shift=False, ctrl=False, alt=False):
            self.key = key
            self.shift = shift
            self.ctrl = ctrl
            self.alt = alt

        def resolveKey(self):
            if self.key == None:
                return None

            parts = []

            if self.shift:
                if not "shift_" in self.key:
                    parts.append("shift")
            elif "shift_" in self.key:
                parts.append("shift")

            if self.ctrl:
                if not "ctrl_" in self.key:
                    parts.append("ctrl")
            elif "ctrl" in self.key:
                parts.append("ctrl")

            if self.alt:
                if not "alt_" in self.key:
                    parts.append("alt")
            elif "alt_" in self.key:
                parts.append("alt")

            parts.append(re.sub(r"(alt_)|(ctrl_)|(shift_)", "", self.key))

            return "_".join(parts)

    class OpenTooltipAction(renpy.ui.Action):
        def __init__(self, title=None, icon=None, message=None, interactive=False, side="top", pos=None):
            self.title = title
            self.icon = icon
            self.message = message
            self.interactive = interactive
            self.side = side
            self.pos = pos

        def __call__(self):
            if self.message:
                renpy.show_screen("URPS_TooltipDialog", title=self.title, icon=self.icon, message=self.message, pos=self.pos, interactive=self.interactive, side=self.side)
                renpy.restart_interaction()

    def adjustable(value, minValue=5): 
        # if URPS.Settings.sizeAdjustment == 0:
    #     return value

        # Helper function to apply adjustment only to integers
        def adjust_number(value):
            return int(value * (renpy.config.screen_height / 1080.0)) + Settings.sizeAdjustment
        
        # If the value is a tuple, apply adjustment to each element
        if isinstance(value, tuple):
            return tuple(adjust_number(v) for v in value)
        
        # If it's a single number, apply adjustment conditionally
        return adjust_number(value)


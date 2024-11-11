init -2000 python in SSSSS:
    _constant = True

    import re
    import shutil
    import os
    import threading
    disk_lock = threading.RLock()

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

    class ImagePlaceholder(renpy.display.core.Displayable):
        def __init__(self, width=0, height=0, **properties):
            super(ImagePlaceholder, self).__init__(**properties)

            self.width = width
            self.height = height

        def render(self, width, height, st, at):
            return renpy.display.render.Render(self.width, self.height)

    class Image(renpy.display.core.Displayable):
        def __init__(self, surface, width, height, fitAfterResize=False, **properties):
            super(Image, self).__init__(**properties)
            self.width = width
            self.height = height
            self.surface = surface
            self.fitAfterResize = fitAfterResize # Fits the bounds to the new size instead of using provided width and height

        def render(self, width, height, st, at):
            surface = self.surface

            sw, sh = surface.get_size()
            w, h = self.scale(surface, (self.width, self.height))

            # Render the image in its original size
            rv = renpy.display.render.Render(sw, sh)
            rv.blit(surface, (0, 0))
 
            # Scale it down to the desired size based on width and height arguments
            try:
                renpy.display.render.blit_lock.acquire()
                surface = renpy.display.scale.smoothscale(surface, (w, h))
            finally:
                renpy.display.render.blit_lock.release()

            cw, ch = surface.get_size()

            if self.fitAfterResize:
                self.width = cw
                self.height = ch

            # Create a new render for the scaled down image and return that
            nrv = renpy.display.render.Render(self.width, self.height)
            nrv.blit(surface, (0, 0))

            return nrv

        def scale(self, image, desired_size):
            return Utils.resizeDimensionsToLimits(image.get_size(), desired_size)

    class GetScreenVariable(x52NonPicklable):
        def __init__(self, name, key=None):
            self.name = name
            self.key = key
        
        def __call__(self):
            Utils.getScreenVariable(self.name, self.key)

    class Utils(x52NonPicklable):
        @staticmethod
        def splitSavename(save_name):
            try:
                page, slot = save_name.split('-')

                if page.isdigit() and slot.isdigit():
                    return int(page), int(slot)
                
                if renpy.config.developer:
                    print("Can't resolve save name ", save_name)
                return 0, 0
            except:
                if renpy.config.developer:
                    print("Can't resolve save name ", save_name)
                return 0, 0

        @staticmethod
        def getSortedSaves():
            regexp = r'\d+' + '-' + r'\d+'
            return Utils.sortSaves(renpy.list_slots(regexp=regexp))

        @staticmethod
        def sortSaves(saves_list):
            return sorted(saves_list, key=Utils.__custom_saves_sort)
        
        @staticmethod
        def __custom_saves_sort(save_name):
            page, slot = Utils.splitSavename(save_name)
            return page, slot

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

        # In built games `[ some text ]` it's not a problem, but if there ever is game with these and config.developer = True, it will throw an exception
        @staticmethod
        def replaceReservedCharacters(text):
            result = []
            length = len(text)
            i = 0

            while i < length:
                char = text[i]
                # Check if this `[` is not part of a `[[` pattern.
                if char == '[' and i < length - 1:
                    # Escape single '['
                    result.append('[')

                    # If [ is following, skip futher
                    if text[i+1] == '[':
                        i += 1

                result.append(char)
                i += 1
            
            # Join list back into a string
            print(''.join(result))
            return ''.join(result)

        @staticmethod
        def getScreenVariable(variableName, dictionaryKey=None):
            cs = renpy.current_screen()
            
            if not cs or not variableName in cs.scope:
                return
            
            if(dictionaryKey):
                key = dictionaryKey if not callable(dictionaryKey) else dictionaryKey()
                return cs.scope[variableName][key]
            else:
                return cs.scope[variableName]

        @staticmethod
        def resizeDimensionsToLimits(original_size, desired_size):
            # Extract dimensions
            desired_width, desired_height = desired_size
            original_width, original_height = original_size

            # Calculate scaling factors for width and height
            width_scaling = float(desired_width) / float(original_width)
            height_scaling = float(desired_height) / float(original_height)

            # Choose the minimum scaling factor to fit the entire image
            scaling_factor = min(width_scaling, height_scaling)

            # Calculate adjusted image size
            new_width = original_width * scaling_factor
            new_height = original_height * scaling_factor

            return int(new_width), int(new_height)

        @staticmethod
        def getLimitedImageSizeWithAspectRatio(desired_width, desired_height):
            # Get the aspect ratio from Ren'Py's screen configuration
            original_width = renpy.config.thumbnail_width or 1 if hasattr(renpy.config, "thumbnail_width") else 1
            original_height = renpy.config.thumbnail_height or 1 if hasattr(renpy.config, "thumbnail_height") else 1

            return Utils.resizeDimensionsToLimits((original_width, original_height), (desired_width, desired_height))

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
    
    class OpenDirectoryAction(renpy.ui.Action):
        def __init__(self, path, cwd=None):
            self.path = path
            self.cwd = cwd

        def __call__(self):
            import os
            import platform
            import subprocess

            directory_path = os.path.join(self.cwd, self.path) if self.cwd else self.path

            # Normalize the path
            directory_path = os.path.normpath(directory_path)
            
            if not os.path.exists(directory_path):
                print "Directory not found: {}".format(directory_path)
                return

            if not os.path.isdir(directory_path):
                print "The path is not a directory: {}".format(directory_path)
                return

            system = platform.system()
            
            try:
                if system == "Windows":
                    # Use explorer to open the directory
                    subprocess.Popen(["explorer", directory_path])
                elif system == "Darwin":
                    # Use Finder to open the directory
                    subprocess.Popen(["open", directory_path])
                elif system == "Linux":
                    # Use xdg-open to open the directory
                    subprocess.Popen(["xdg-open", directory_path])
                elif system == "Android":
                    # Use am start to open the directory (highlighting might not be supported)
                    subprocess.Popen(["am", "start", "-a", "android.intent.action.VIEW", "-d", "file://{}".format(directory_path)])
                else:
                    print "Unsupported OS: {}".format(system)
            except Exception as e:
                print "An error occurred: {}".format(e)

    # class DecrementScreenValue(renpy.ui.Action):
    #     def __init__(self, variableName, amount = 1, min = None):
    #         self.variableName = variableName
    #         self.amount = amount
    #         self.min = min

    #     def __call__(self):
    #         cs = renpy.current_screen()

    #         if cs is None:
    #             return

    #         newValue = cs.scope[self.variableName] - self.amount

    #         if self.min:
    #             cs.scope[self.variableName] = max(self.min, newValue)
    #         else:
    #             cs.scope[self.variableName] = newValue

    #         renpy.restart_interaction()

    # class IncrementScreenValue(renpy.ui.Action):
    #     def __init__(self, variableName, amount = 1, max = None):
    #         self.variableName = variableName
    #         self.amount = amount
    #         self.max = max

    #     def __call__(self):
    #         cs = renpy.current_screen()

    #         if cs is None:
    #             return

    #         newValue = cs.scope[self.variableName] + self.amount

    #         if self.max:
    #             cs.scope[self.variableName] = min(self.max, newValue)
    #         else:
    #             cs.scope[self.variableName] = newValue

    #         renpy.restart_interaction()
    
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

init -1000 python:
    def adjustable(value, minValue=5): 
        if SSSSS.Settings.sizeAdjustment == 0:
            return value

        # Helper function to apply adjustment only to integers
        def adjust_number(value):
            if isinstance(value, int):
                size_adjustment = SSSSS.Settings.sizeAdjustment
                min_value = minValue
                max_value = 1080

                # Base value is bounded by min and max
                value = max(min_value, min(value, max_value))
                
                # Calculate scaled value based on positive or negative size_adjustment
                if size_adjustment > 0:
                    # Increase the value proportionally based on the size_adjustment
                    scaled_value = value + size_adjustment
                else:
                    #TODO: This doesn't work at all... Fix it.
                    # Decrease the value with damping to avoid going too low
                    damping_factor = 1 + abs(size_adjustment) / 10
                    scaled_value = max(min_value, value - int(value / damping_factor))
                
                # Ensure the scaled value stays within the min and max bounds
                return max(min_value, min(scaled_value, max_value))
            return value  # Return the number as is if it's a float
        
        # If the value is a tuple, apply adjustment to each element
        if isinstance(value, tuple):
            return tuple(adjust_number(v) for v in value)
        
        # If it's a single number, apply adjustment conditionally
        return adjust_number(value)


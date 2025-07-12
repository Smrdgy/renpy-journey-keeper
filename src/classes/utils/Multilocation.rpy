init -9999 python in JK:
    _constant = True

    import shutil
    import os
    import threading
    disk_lock = threading.RLock()

    class MultiLocation(renpy.savelocation.MultiLocation):
        def __init__(self):
            super(MultiLocation, self).__init__()

            self.last_page_cache = None
            self.nativeLocations = renpy.loadsave.location.nativeLocations if hasattr(renpy.loadsave, "nativeLocations") else renpy.loadsave.location.locations

        def add(self, location):
            self.locations.append(location)

        def activate_locations(self):
            for location in self.locations:
                location.active = True

        def deactivate_locations(self):
            for location in self.locations:
                location.active = False

        def load_persistent(self, *args, **kwargs):
            rv = []

            for l in self.nativeLocations:
                rv.extend(l.load_persistent(*args, **kwargs))

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
                slot_mtime = l.mtime(slotname) or -1

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

        def unlink_all(self, scan=True, include_inactive=False):
            for l in (self.locations if include_inactive else self.active_locations()):
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
                    if target_location and os.path.exists(target_location.directory):
                        shutil.rmtree(target_location.directory) # Clear anything that is already there and also remove the root directory, otherwise shutil.copytree would throw an exception...

                    try:
                        shutil.copytree(source_location.directory, target_location.directory)
                    except Exception as e:
                        print(e)
                        return False

                if scan:
                    multilocation.scan()

                return True

        def save_json(self, slotname, include_inactive=True):
            if include_inactive:
                l = self.newest_including_inactive(slotname)

                if l is None:
                    return None

                return l.json(slotname)

            return self.json(slotname)

        def save_name(self, slotname, include_inactive=True):
            save_json = self.save_json(slotname, include_inactive=include_inactive)
            if save_json:
                return save_json.get("_save_name", None)

            return None

        def change_locations_directory_name(self, name, force=False):
            for location in self.locations:
                location.change_directory_name(name, force)

        def validate_locations_for_change_of_directory_name(self, name):
            error_locations = []
            for location in self.locations:
                if not location.can_change_directory_name(name):
                    error_locations.append((os.path.abspath(os.path.join(location.directory, "..", name)), "LOCATION_EXISTS"))
            
            return error_locations

        def remove_dir(self):
            for location in self.locations:
                location.remove_dir()

        def edit_json(self, slotname, json, include_inactive=False, scan=True):
            for location in (self.locations if include_inactive else self.active_locations()):
                location.edit_json(slotname, json)
            
            if scan:
                self.scan()

        def scan(self):
            self.last_page_cache = None
            return super(MultiLocation, self).scan()
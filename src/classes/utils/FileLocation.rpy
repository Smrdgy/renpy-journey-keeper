init -9999 python in JK:
    _constant = True

    import shutil
    import os
    import threading
    disk_lock = threading.RLock()
    import time
    import locale
    from json import dumps as json_dumps

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

        def mtime_as_date(self, slotname):
            # Set locale to the user's default settings
            locale.setlocale(locale.LC_TIME, '')

            mtime = self.mtime(slotname)
            if mtime:
                return time.strftime('%c', time.localtime(mtime))

            return None

        def change_directory_name(self, name, force=False):
            self.change_directory(os.path.join(self.directory, "..", name), force)

        def change_directory(self, new_directory, force=False):
            if not force and not self.can_change_directory(new_directory):
                raise Exception("LOCATION_EXISTS")

            if os.path.exists(new_directory):
                shutil.rmtree(new_directory)

            shutil.move(self.directory, new_directory)

            self.directory = new_directory

        def can_change_directory_name(self, name):
            return self.can_change_directory(os.path.join(self.directory, "..", name))

        def can_change_directory(self, new_directory):
            if os.path.exists(new_directory):
                return len(os.listdir(new_directory)) == 0

            return True

        def remove_dir(self):
            if os.path.exists(self.directory):
                os.rmdir(self.directory)

        def edit_json(self, slotname, json):
            with disk_lock:
                try:
                    filename = self.filename(slotname)
                    filename_new = filename + ".new"
                    with zipfile.ZipFile(filename, 'r') as zin:
                        with zipfile.ZipFile(filename_new, 'w') as zout:
                            for item in zin.infolist():
                                if item.filename != "json":
                                    zout.writestr(item, zin.read(item.filename))

                            zout.writestr("json", json_dumps(json))

                    os.remove(filename)
                    os.rename(filename_new, filename)
                except Exception as e:
                    print(e)
                    return False
                finally:
                    if zin:
                        zin.close()
                    if zout:
                        zout.close()
init -2 python in JK:
    _constant = True

    import io
    import os
    import __main__

    savedir = "JK"

    class UserDir(x52NonPicklable):
        @staticmethod
        def is_available():
            return renpy.config.save_directory != None

        @staticmethod
        def root_path():
            return __main__.path_to_saves(renpy.config.gamedir, savedir)

        @staticmethod
        def game_path():
            return os.path.join(UserDir.root_path(), renpy.config.save_directory or "")

        @staticmethod
        def settings_path():
            return os.path.join(UserDir.game_path(), "settings.json")

        @staticmethod
        def global_settings_path():
            return os.path.join(UserDir.root_path(), "settings.json")

        @staticmethod
        def playthroughs_path():
            return os.path.join(UserDir.game_path(), "playthroughs.json")

        @staticmethod
        def loadSettings():
            return UserDir.loadJson(UserDir.settings_path()) or {}

        @staticmethod
        def saveSettings(data):
            return UserDir.saveJson(UserDir.settings_path(), data)

        @staticmethod
        def removeSettings():
            os.unlink(UserDir.settings_path())

        @staticmethod
        def loadGlobalSettings():
            return UserDir.loadJson(UserDir.global_settings_path()) or {}

        @staticmethod
        def saveGlobalSettings(data):
            return UserDir.saveJson(UserDir.global_settings_path(), data)

        @staticmethod
        def removeGlobalSettings():
            os.unlink(UserDir.global_settings_path())

        @staticmethod
        def loadPlaythroughs():
            return UserDir.loadJson(UserDir.playthroughs_path())

        @staticmethod
        def savePlaythroughs(data):
            return UserDir.saveJson(UserDir.playthroughs_path(), data)

        @staticmethod
        def hasPlaythroughs():
            return UserDir.playthroughsMtime() > 0

        @staticmethod
        def playthroughsMtime():
            path = UserDir.playthroughs_path()

            if not os.path.exists(path):
                return 0

            return os.path.getmtime(path)

        @staticmethod
        def loadJson(path):
            if not renpy.config.save_directory:
                return None

            if os.path.isfile(path):
                try:
                    with io.open(path, "r", encoding="utf-8") as file:
                        return json.loads(file.read())
                except Exception as e:
                    print(e)
                    return None

        @staticmethod
        def saveJson(file_path, data):
            if not renpy.config.save_directory:
                return False

            if renpy.config.save_directory in file_path:
                dir_path = UserDir.game_path()

                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)

            try:
                with io.open(file_path, "w", encoding="utf-8") as file:
                    file.write(unicode(data))
            except Exception as e:
                print(e)
                return False

            return True
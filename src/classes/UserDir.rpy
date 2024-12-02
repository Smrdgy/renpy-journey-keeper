init -1001 python in SSSSS:
    import io
    import os
    import __main__

    savedir = "SSSSS"

    class UserDir(x52NonPicklable):
        @staticmethod
        def root_path():
            return __main__.path_to_saves(renpy.config.gamedir, savedir)

        @staticmethod
        def game_path():
            return os.path.join(UserDir.root_path(), renpy.config.save_directory)

        @staticmethod
        def settings_path():
            return os.path.join(UserDir.game_path(), "settings.json")

        @staticmethod
        def playthroughs_path():
            return os.path.join(UserDir.game_path(), "playthroughs.json")

        @staticmethod
        def loadSettings():
            return UserDir.loadJson("settings") or {}

        @staticmethod
        def saveSettings(data):
            return UserDir.saveJson("settings", data)

        @staticmethod
        def removeSettings():
            os.unlink(UserDir.settings_path())

        @staticmethod
        def loadPlaythroughs():
            return UserDir.loadJson("playthroughs")

        @staticmethod
        def savePlaythroughs(data):
            return UserDir.saveJson("playthroughs", data)

        @staticmethod
        def playthroughsMtime():
            path = UserDir.playthroughs_path()

            if not os.path.exists(path):
                return 0

            return os.path.getmtime(path)

        @staticmethod
        def loadJson(filename):
            path = os.path.join(UserDir.game_path(), filename + ".json")

            if os.path.isfile(path):
                try:
                    with io.open(path, "r", encoding="utf-8") as file:
                        return json.loads(file.read())
                except Exception as e:
                    print(e)
                    return None

        @staticmethod
        def saveJson(filename, data):
            dir_path = UserDir.game_path()
            file_path = os.path.join(dir_path, filename + ".json")

            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            try:
                with io.open(file_path, "w", encoding="utf-8") as file:
                    file.write(unicode(data))
            except Exception as e:
                print(e)
                return False

            return True
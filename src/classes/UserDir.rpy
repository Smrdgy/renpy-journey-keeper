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
        def load_settings():
            return UserDir.load_json(UserDir.settings_path()) or {}

        @staticmethod
        def save_settings(data):
            return UserDir.save_json(UserDir.settings_path(), data)

        @staticmethod
        def remove_settings():
            os.unlink(UserDir.settings_path())

        @staticmethod
        def load_global_settings():
            return UserDir.load_json(UserDir.global_settings_path()) or {}

        @staticmethod
        def save_global_settings(data):
            return UserDir.save_json(UserDir.global_settings_path(), data)

        @staticmethod
        def remove_global_settings():
            os.unlink(UserDir.global_settings_path())

        @staticmethod
        def load_playthroughs():
            return UserDir.load_json(UserDir.playthroughs_path())

        @staticmethod
        def save_playthroughs(data):
            return UserDir.save_json(UserDir.playthroughs_path(), data)

        @staticmethod
        def has_playthroughs():
            return UserDir.playthroughs_mtime() > 0

        @staticmethod
        def playthroughs_mtime():
            path = UserDir.playthroughs_path()

            if not os.path.exists(path):
                return 0

            return os.path.getmtime(path)

        @staticmethod
        def load_json(path):
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
        def save_json(file_path, data):
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
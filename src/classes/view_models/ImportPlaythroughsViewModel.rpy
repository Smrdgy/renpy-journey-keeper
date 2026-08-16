init python in JK:
    _constant = True

    import os
    import shutil

    class ImportPlaythroughsViewModel(x52NonPicklable):
        def __init__(self):
            self.loading = True
            self.error_message = None

            self.games = []
            self.selected_game = None

            self.playthroughs = []
            self.selection = SelectionState()

            self.success = False
            self.conflicts = []

            self.copySaves = False
            self.playthroughs_to_copy_saves = []
            self.saves_view_model = None

            renpy.invoke_in_thread(self.find_all_games)
            
        def find_all_games(self):
            self.loading = True
            self.games = []
            renpy.restart_interaction()

            root_path = os.path.normpath(os.path.join(UserDir.root_path(), ".."))
            try:
                if os.path.exists(root_path):
                    for game_name in os.listdir(root_path):
                        if game_name in ["JK", "0x52-URM", renpy.config.save_directory]:
                            continue

                        path = os.path.join(root_path, game_name)

                        if os.path.isdir(path):
                            json_path = os.path.join(UserDir.root_path(), game_name, "playthroughs.json")

                            if os.path.exists(json_path):
                                self.games.append((game_name, json_path))
                else:
                    self.error_message = "User directory does not exist"
            except Exception as e:
                self.error_message = "Failed to load games"
                print(e)

            self.loading = False
            renpy.restart_interaction()

        def set_game(self, game):
            self.selected_game = game

            if game:
                renpy.invoke_in_thread(self.find_all_playthroughs)

        def find_all_playthroughs(self):
            self.loading = True
            self.playthroughs = []
            renpy.restart_interaction()

            playthroughs = UserDir.load_json(self.selected_game[1])
            if playthroughs:
                for playthrough_data in playthroughs:
                    if playthrough_data.get("directory") not in ["_memories"]:
                        self.playthroughs.append(PlaythroughClass.from_dict(playthrough_data))
            else:
                self.error_message = "Failed to load playthroughs"

            self.loading = False
            renpy.restart_interaction()

        def import_selected_playthroughs(self, copySaves=False):
            self.success = False
            self.copySaves = copySaves
            self.playthroughs_to_copy_saves = []
            self.saves_view_model = None

            conflicts = []
            for p in self.selection.items:
                conflicting = self.__find_conflicting_playthrough(p)
                if conflicting:
                    conflicts.append((conflicting, p))
                else:
                    Playthroughs.add(p, activate=False, save=False, restart_interaction=False)

                    if copySaves:
                        self.playthroughs_to_copy_saves.append((p.directory, p))

            Playthroughs.save()

            self.conflicts = conflicts

            if len(conflicts) == 0:
                self.success = True
                self._start_saves_copy_if_needed()

            renpy.restart_interaction()

        def __find_conflicting_playthrough(self, playthrough):
            for p in Playthroughs.playthroughs:
                if p.id == playthrough.id or p.name == playthrough.name or p.directory == playthrough.directory:
                    return p

            return None

        def _start_saves_copy_if_needed(self):
            if not self.copySaves or not self.playthroughs_to_copy_saves:
                return

            self.saves_view_model = ImportPlaythroughsSavesViewModel(self.selected_game[0], self.playthroughs_to_copy_saves)
            renpy.invoke_in_thread(self.saves_view_model.process_start)

        def conflict_overwrite(self):
            current, new = self.conflicts.pop(0)

            if self.copySaves:
                self.playthroughs_to_copy_saves.append((new.directory, current))

            current.edit_from_playthrough(new)

            Playthroughs.save()

            self.conflicts_resolution_continue()

        def conflict_keep_both(self):
            old, new = self.conflicts.pop(0)
            source_directory = new.directory
            new = new.copy()
            new.regenerate_unique_data()

            name_parts = new.name.split(" ")
            possible_number = None
            remaining_name = None

            # Append a unique number to the name to avoid conflict
            while self.__find_conflicting_playthrough(new):
                if possible_number is None:
                    try:
                        possible_number = int(name_parts[-1]) + 1
                        remaining_name = name_parts[:-1]
                    except:
                        possible_number = 1
                        remaining_name = [new.name]
                else:
                    possible_number += 1

                new.name = " ".join(remaining_name + [str(possible_number)])
                new.regenerate_unique_data()

            Playthroughs.add(new, activate=False, save=True, restart_interaction=True)

            if self.copySaves:
                self.playthroughs_to_copy_saves.append((source_directory, new))

            self.conflicts_resolution_continue()

        def conflict_skip(self):
            self.conflicts.pop(0)

            self.conflicts_resolution_continue()

        def conflicts_resolution_continue(self):
            if len(self.conflicts) == 0:
                self.success = True
                self._start_saves_copy_if_needed()

            renpy.restart_interaction()

        def conflict_abort(self):
            self.conflicts = []
            renpy.restart_interaction()

        class SetGameAction(renpy.ui.Action):
            def __init__(self, view_model, game):
                self.view_model = view_model
                self.game = game

            def __call__(self):
                self.view_model.set_game(self.game)
                renpy.restart_interaction()

        class SelectionAction(renpy.ui.Action):
            def __init__(self, view_model, playthrough):
                self.view_model = view_model
                self.playthrough = playthrough

            def __call__(self):
                self.view_model.selection.click(self.playthrough, self.view_model.playthroughs)

        class BackAction(renpy.ui.Action):
            def __init__(self, view_model):
                self.view_model = view_model

            def __call__(self):
                self.view_model.selection.select_none()
                self.view_model.selected_game = None

                renpy.restart_interaction()

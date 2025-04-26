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
            self.selected_playthroughs = []

            self.success = False
            self.conflicts = []

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

        def import_selected_playthroughs(self):
            self.success = False

            conflicts = []
            for p in self.selected_playthroughs:
                conflicting = self.__find_conflicting_playthrough(p)
                if conflicting:
                    conflicts.append((conflicting, p))
                else:
                    Playthroughs.add(p, activate=False, save=False, restart_interaction=False)
            
            Playthroughs.save()

            self.conflicts = conflicts

            if len(conflicts) == 0:
                self.success = True

            renpy.restart_interaction()

        def __find_conflicting_playthrough(self, playthrough):
            for p in Playthroughs.playthroughs:
                if p.id == playthrough.id or p.name == playthrough.name or p.directory == playthrough.directory:
                    return p

            return None

        def conflict_overwrite(self):
            current, new = self.conflicts.pop(0)
            current.edit_from_playthrough(new)

            Playthroughs.save()

            self.conflicts_resolution_continue()

        def conflict_keep_both(self):
            old, new = self.conflicts.pop(0)
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

            self.conflicts_resolution_continue()

        def conflict_skip(self):
            self.conflicts.pop(0)

            self.conflicts_resolution_continue()

        def conflicts_resolution_continue(self):
            if len(self.conflicts) == 0:
                self.success = True

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
            def __init__(self, view_model, playthrough, last_selected_playthrough):
                self.view_model = view_model
                self.playthrough = playthrough
                self.last_selected_playthrough = last_selected_playthrough

            def __call__(self):
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    start_index = self.view_model.playthroughs.index(self.last_selected_playthrough) if self.last_selected_playthrough in self.view_model.playthroughs else -1
                    end_index = self.view_model.playthroughs.index(self.playthrough) if self.playthrough in self.view_model.playthroughs else -1

                    if start_index > -1 and end_index > -1:
                        new_playthroughs = []
                        for playthrough in self.view_model.playthroughs[min(start_index, end_index):max(start_index, end_index) + 1]:
                            if playthrough in new_playthroughs:
                                new_playthroughs.remove(playthrough)
                            else:
                                new_playthroughs.append(playthrough)

                        self.view_model.selected_playthroughs = new_playthroughs
                        renpy.restart_interaction()
                        return
                elif pygame.key.get_mods() & pygame.KMOD_LCTRL:
                    if self.playthrough in self.view_model.selected_playthroughs:
                        self.view_model.selected_playthroughs.remove(self.playthrough)
                    else:
                        self.view_model.selected_playthroughs.append(self.playthrough)
                else:
                    self.view_model.selected_playthroughs = [self.playthrough]
                
                cs = renpy.current_screen()
                if not cs:
                    return

                cs.scope["last_selected_playthrough"] = self.playthrough

                renpy.restart_interaction()

        class ToggleAllAction(renpy.ui.Action):
            def __init__(self, view_model):
                self.view_model = view_model

            def __call__(self):
                if len(self.view_model.selected_playthroughs) < len(self.view_model.playthroughs):
                    self.view_model.selected_playthroughs = [] + self.view_model.playthroughs
                else:
                    self.view_model.selected_playthroughs = []

                renpy.restart_interaction()

        class SelectAllAction(renpy.ui.Action):
            def __init__(self, view_model):
                self.view_model = view_model

            def __call__(self):
                self.view_model.selected_playthroughs = [] + self.view_model.playthroughs
                renpy.restart_interaction()

        class BackAction(renpy.ui.Action):
            def __init__(self, view_model):
                self.view_model = view_model

            def __call__(self):
                self.view_model.selected_playthroughs = []
                self.view_model.selected_game = None

                renpy.restart_interaction()

screen JK_ImportPlaythroughsSelectGame(view_model, search, import_games_vlist):
    default search_input = JK.TextInput("search", auto_focus=True)

    python:
        def get_filtered_games(all_games, search):
            if not search:
                return all_games

            search = search.lower()

            games = []
            for game in all_games:
                if search in game[0].lower():
                    games.append(game)

            return games

        filtered_games = get_filtered_games(view_model.games, search)

        row_pitch = JK.scaled(40)
        viewport_size = import_games_vlist.estimate_viewport_size(renpy.config.screen_height)
        window_start, window_end, top_spacer, bottom_spacer = import_games_vlist.compute(len(filtered_games), row_pitch, viewport_size)
        windowed_games = filtered_games[window_start:window_end]

    hbox:
        button:
            action NullAction()
            key_events True
            xalign 0.5

            vbox:
                add search_input.displayable(placeholder="Search")
                frame style "JK_default" background "#ffffff22" hover_background JK.Colors.hover ysize 2 offset JK.scaled((0, 2))

    text "Found {} game(s)".format(len(filtered_games))

    viewport:
        mousewheel True
        draggable True
        scrollbars "vertical"
        vscrollbar_unscrollable "hide"
        pagekeys True
        yadjustment import_games_vlist.adjustment

        vbox:
            null height top_spacer

            $ i = window_start
            for game in windowed_games:
                python:
                    i += 1
                    game_name, path = game

                button:
                    ysize row_pitch
                    action JK.ImportPlaythroughsViewModel.SetGameAction(view_model, game)
                    style ("JK_row_button" if i % 2 == 0 else "JK_row_odd_button")
                    xsize 1.0

                    text JK.Utils.escape_all_problematic_characters(game_name)

            null height bottom_spacer

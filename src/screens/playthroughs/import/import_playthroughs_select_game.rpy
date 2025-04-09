screen JK_ImportPlaythroughsSelectGame(view_model, search):
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

    hbox:
        button:
            action NullAction()
            key_events True
            xalign 0.5

            vbox:
                add search_input.displayable(placeholder="Search")
                frame style "JK_default" background "#ffffff22" hover_background JK.Colors.hover ysize 2 offset JK.scaled((0, 2))

    viewport:
        mousewheel True
        draggable True
        scrollbars "vertical"
        vscrollbar_unscrollable "hide"
        pagekeys True

        vbox:
            text "Found {} game(s)".format(len(view_model.games))

            $ i = 0
            for game in get_filtered_games(view_model.games, search):
                python:
                    i += 1
                    game_name, path = game

                button:
                    action JK.ImportPlaythroughsViewModel.SetGameAction(view_model, game)
                    style ("JK_row_button" if i % 2 == 0 else "JK_row_odd_button")
                    xsize 1.0

                    text game_name
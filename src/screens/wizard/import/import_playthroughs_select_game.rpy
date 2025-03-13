screen JK_ImportPlaythroughsSelectGame(view_model):
    viewport:
        mousewheel True
        draggable True
        scrollbars "vertical"
        pagekeys True

        vbox:
            text "Found {} game(s)".format(len(view_model.games))

            $ i = 0
            for game in view_model.games:
                python:
                    i += 1
                    game_name, path = game

                button:
                    action JK.ImportPlaythroughsViewModel.SetGameAction(view_model, game)
                    style ("JK_row_button" if i % 2 == 0 else "JK_row_odd_button")
                    xsize 1.0

                    text game_name
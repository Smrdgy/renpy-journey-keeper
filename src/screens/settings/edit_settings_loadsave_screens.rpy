screen SSSSS_SettingsLoadSaveScreens(update_at_runtime=False):
    python:
        def remove_duplicates(lst):
            seen = set()
            result = []
            for item in lst:
                if item not in seen:
                    result.append(item)
                    seen.add(item)
            return result

        def get_active_screens():
            screens = []
            for context in renpy.game.contexts:
                for layer in context.scene_lists.layers:
                    for sle in context.scene_lists.layers[layer]:
                        if sle and sle.name:
                            name = sle.name[0]

                            #TODO: Improve
                            # get_screen() isn't very efficient here since the loops above are doing pretty much the same,
                            # but I'm missing something to check if the screen is valid, or visible, or something and I couldn't be bothered to do it now.
                            if not "SSSSS_" in name and renpy.get_screen(name):
                                screens.append(name)

            return screens

    if update_at_runtime:
        python:
            activeScreens = get_active_screens()
            relevantSaveScreens = remove_duplicates(["save"] + SSSSS.Settings.saveScreenName + activeScreens)
            relevantLoadScreens = remove_duplicates(["load"] + SSSSS.Settings.loadScreenName + activeScreens)
    else:
        default activeScreens = get_active_screens()
        default relevantSaveScreens = remove_duplicates(["save"] + SSSSS.Settings.saveScreenName + activeScreens)
        default relevantLoadScreens = remove_duplicates(["load"] + SSSSS.Settings.loadScreenName + activeScreens)

    vbox:
        use SSSSS_Title("Save page", 3)
        for screen in relevantSaveScreens:
            $ print(screen)
            use SSSSS_Checkbox(checked=screen in SSSSS.Settings.saveScreenName, text=("\"save\" (default)" if screen == "save" else "\"" + screen + "\""), action=SSSSS.Settings.SetSaveScreenName(screen), disabled=screen == "save")

        use SSSSS_YSpacer(2)

        use SSSSS_Title("Load page", 3)
        for screen in relevantLoadScreens:
            use SSSSS_Checkbox(checked=screen in SSSSS.Settings.loadScreenName, text=("\"load\" (default)" if screen == "load" else "\"" + screen + "\""), action=SSSSS.Settings.SetLoadScreenName(screen), disabled=screen == "load")
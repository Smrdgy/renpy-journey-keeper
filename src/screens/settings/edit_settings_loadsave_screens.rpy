screen JK_SettingsLoadSaveScreens(update_at_runtime=False):
    python:
        def remove_duplicates(lst):
            seen = set()
            result = []
            for item in lst:
                if item not in seen:
                    result.append(item)
                    seen.add(item)
            return result

    if update_at_runtime:
        python:
            activeScreens = JK.Utils.get_active_screens()
            relevantSaveScreens = remove_duplicates(["save"] + JK.Settings.saveScreenName + activeScreens)
            relevantLoadScreens = remove_duplicates(["load"] + JK.Settings.loadScreenName + activeScreens)
    else:
        default activeScreens = JK.Utils.get_active_screens()
        default relevantSaveScreens = remove_duplicates(["save"] + JK.Settings.saveScreenName + activeScreens)
        default relevantLoadScreens = remove_duplicates(["load"] + JK.Settings.loadScreenName + activeScreens)

    vbox:
        use JK_Title("Save page", 3)
        for screen in relevantSaveScreens:
            use JK_Checkbox(checked=screen in JK.Settings.saveScreenName, text=("\"save\" (default)" if screen == "save" else "\"" + screen + "\""), action=JK.Settings.SetSaveScreenName(screen), disabled=screen == "save")

        use JK_YSpacer(2)

        use JK_Title("Load page", 3)
        for screen in relevantLoadScreens:
            use JK_Checkbox(checked=screen in JK.Settings.loadScreenName, text=("\"load\" (default)" if screen == "load" else "\"" + screen + "\""), action=JK.Settings.SetLoadScreenName(screen), disabled=screen == "load")
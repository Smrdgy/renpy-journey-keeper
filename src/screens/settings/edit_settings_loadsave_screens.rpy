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
            active_screens = JK.Utils.get_active_screens()
            relevant_save_screens = remove_duplicates(["save"] + JK.Settings.saveScreenName + active_screens)
            relevant_load_screens = remove_duplicates(["load"] + JK.Settings.loadScreenName + active_screens)
    else:
        default active_screens = JK.Utils.get_active_screens()
        default relevant_save_screens = remove_duplicates(["save"] + JK.Settings.saveScreenName + active_screens)
        default relevant_load_screens = remove_duplicates(["load"] + JK.Settings.loadScreenName + active_screens)

    vbox:
        use JK_Title("Save page", 3)
        for screen in relevant_save_screens:
            use JK_Checkbox(checked=screen in JK.Settings.saveScreenName, text=("\"save\" (default)" if screen == "save" else "\"" + screen + "\""), action=JK.Settings.SetSaveScreenNameAction(screen), disabled=screen == "save")

        use JK_YSpacer(2)

        use JK_Title("Load page", 3)
        for screen in relevant_load_screens:
            use JK_Checkbox(checked=screen in JK.Settings.loadScreenName, text=("\"load\" (default)" if screen == "load" else "\"" + screen + "\""), action=JK.Settings.SetLoadScreenNameAction(screen), disabled=screen == "load")
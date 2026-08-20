screen JK_Overlay():
    layer "screens"
    style_prefix "JK"

    if JK.Settings.autosaveKey:
        key JK.Settings.autosaveKey action JK.Playthroughs.ToggleAutosaveOnChoicesForActiveAction()

    if not JK.Memories.memoryInProgress and not renpy.store._in_replay and JK.Settings.quickSaveEnabled and JK.Settings.quickSaveKey:
        key JK.Settings.quickSaveKey action JK.Playthroughs.QuickSaveAction()

    if not renpy.store._in_replay and JK.Settings.memoriesEnabled and JK.Settings.memoriesKey:
        key JK.Settings.memoriesKey action JK.Memories.OpenSaveMemory()

    if JK.Playthroughs.active_playthrough.autosaveOnChoices:
        if JK.Autosaver.after_load_save_position_pending:
            $ JK.Autosaver.process_slot_after_load()

    key "ctrl_alt_shift_K_p" action JK.Settings.ResetSizeAdjustmentAction()

    python:
        isSaveLoadScreen = JK.Utils.is_save_load_screen()

    # Some games clear screen layers on their own way into/out of the save/load screen through
    # paths JK doesn't control. JK_Overlay re-runs on every restart_interaction (far more often
    # than start_interact_callbacks, which only fires at the start of a brand new interact() -
    # too late here, since closing the save screen commonly resumes an already-running one
    # instead of starting a fresh one), so this is the most responsive place to self-heal.
    if JK.Autocomplete.active and not renpy.get_screen('JK_AutocompleteBar'):
        python:
            renpy.show_screen('JK_AutocompleteBar')
            renpy.restart_interaction()

    if isSaveLoadScreen and JK.Memories.memoryInProgress:
        use JK_ExitMemoryConfirm()

    if isSaveLoadScreen and JK.Settings.showPlaythroughNameBanner:
        use JK_ActivePlaythroughBanner()
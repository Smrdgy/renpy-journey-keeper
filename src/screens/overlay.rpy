screen SSSSS_Overlay():
    layer "screens"
    style_prefix "SSSSS"

    if SSSSS.Settings.autosaveKey:
        key SSSSS.Settings.autosaveKey action SSSSS.Playthroughs.ToggleAutosaveOnChoicesOnActive()

    if not SSSSS.Memories.memoryInProgress and not renpy.store._in_replay and SSSSS.Settings.quickSaveEnabled and SSSSS.Settings.quickSaveKey:
        key SSSSS.Settings.quickSaveKey action SSSSS.Playthroughs.QuickSave()

    if not renpy.store._in_replay and SSSSS.Settings.memoriesEnabled and SSSSS.Settings.memoriesKey:
        key SSSSS.Settings.memoriesKey action SSSSS.Memories.OpenSaveMemory()

    if SSSSS.Playthroughs.activePlaythrough.autosaveOnChoices:
        if SSSSS.Autosaver.afterLoadSavePositionPending:
            $ SSSSS.Autosaver.processSlotAfterLoad()

    key "ctrl_alt_shift_K_p" action SSSSS.Settings.ResetSizeAdjustment()

    python:
        isSaveLoadScreen = renpy.get_screen("load") != None or renpy.get_screen("save") != None

    if isSaveLoadScreen and SSSSS.Memories.memoryInProgress:
        use SSSSS_ExitMemoryConfirm()

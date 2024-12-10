screen URPS_Overlay():
    layer "screens"
    style_prefix "URPS"

    if URPS.Settings.autosaveKey:
        key URPS.Settings.autosaveKey action URPS.Playthroughs.ToggleAutosaveOnChoicesOnActive()

    if not URPS.Memories.memoryInProgress and not renpy.store._in_replay and URPS.Settings.quickSaveEnabled and URPS.Settings.quickSaveKey:
        key URPS.Settings.quickSaveKey action URPS.Playthroughs.QuickSave()

    if not renpy.store._in_replay and URPS.Settings.memoriesEnabled and URPS.Settings.memoriesKey:
        key URPS.Settings.memoriesKey action URPS.Memories.OpenSaveMemory()

    if URPS.Playthroughs.activePlaythrough.autosaveOnChoices:
        if URPS.Autosaver.afterLoadSavePositionPending:
            $ URPS.Autosaver.processSlotAfterLoad()

    key "ctrl_alt_shift_K_p" action URPS.Settings.ResetSizeAdjustment()

    python:
        isSaveLoadScreen = URPS.Utils.is_save_load_screen()

    if isSaveLoadScreen and URPS.Memories.memoryInProgress:
        use URPS_ExitMemoryConfirm()

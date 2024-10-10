screen SSSSS_Overlay():
    layer "screens"
    style_prefix "SSSSS"

    key 'alt_K_a' action SSSSS.Playthroughs.ToggleAutosaveOnChoicesOnActive()

    if not SSSSS.Memories.memoryInProgress and not renpy.store._in_replay:
        key "K_F5" action SSSSS.Playthroughs.QuickSave()

    if not renpy.store._in_replay:
        key "K_BACKQUOTE" action SSSSS.Memories.OpenSaveMemory()

    if SSSSS.Playthroughs.activePlaythrough.autosaveOnChoices:
        if SSSSS.Autosaver.afterLoadSavePositionPending:
            $ SSSSS.Autosaver.processSlotAfterLoad()

    python:
        isSaveLoadScreen = renpy.get_screen("load") != None or renpy.get_screen("save") != None

    if isSaveLoadScreen and SSSSS.Memories.memoryInProgress:
        use SSSSS_ExitMemoryConfirm()

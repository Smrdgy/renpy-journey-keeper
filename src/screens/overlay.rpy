screen SSSSS_Overlay():
    layer "screens"
    style_prefix "SSSSS"

    key "K_F5" action SSSSS.Playthroughs.QuickSave()
    key "K_BACKQUOTE" action SSSSS.Memories.OpenSaveMemory()

    if SSSSS.Playthroughs.activePlaythrough.autosaveOnChoices:
        if SSSSS.Autosaver.afterLoadSavePositionPending:
            $ SSSSS.Autosaver.processSlotAfterLoad()

    python:
        isSaveLoadScreen = renpy.get_screen("load") != None or renpy.get_screen("save") != None

    if isSaveLoadScreen and SSSSS.Memories.memoryInProgress:
        use SSSSS_ExitMemoryConfirm()

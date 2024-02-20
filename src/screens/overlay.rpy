screen SSSSS_Overlay():
    layer "screens"

    key "K_F5" action SSSSS.Playthroughs.QuickSave()

    if SSSSS.Playthroughs.activePlaythrough.autosaveOnChoices:
        if SSSSS.Autosaver.afterLoadSavePositionPending:
            $ SSSSS.Autosaver.processSlotAfterLoad()
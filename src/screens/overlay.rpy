screen SSSSS_Overlay():
    layer "screens"

    text "." offset(1910, -20) color '#f00'

    key "K_F5" action SSSSS.Playthroughs.QuickSave()

    if SSSSS.Playthroughs.activePlaythrough != None and SSSSS.Playthroughs.activePlaythrough.autosaveOnChoices:
        if SSSSS.Autosaver.afterLoadSavePositionPending:
            $ SSSSS.Autosaver.processSlotAfterLoad()

        if(not SSSSS.Choices.isDisplayingChoice):
            text "." offset(1910, -20) color '#00ff00'

            if(SSSSS.Autosaver.pendingSave != None and SSSSS.Autosaver.pendingSave.isReady and not SSSSS.Autosaver.confirmDialogOpened):
                $ SSSSS.Autosaver.TrySavePendingSave()()
        else:
            key "mousedown_1" action SSSSS.Autosaver.HandlePress()

            text "." offset(1910, -20) color '#f0f'
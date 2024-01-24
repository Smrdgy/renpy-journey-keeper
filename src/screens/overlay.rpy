screen SSSSS_Overlay():
    layer "SSSSSoverlay"

    if SSSSS.Playthroughs.activePlaythrough.autosaveOnChoices:
        if(not SSSSS.Choices.isDisplayingChoice):
            if(SSSSS.Autosaver.pendingSave != None and SSSSS.Autosaver.pendingSave.isReady and not SSSSS.Autosaver.confirmDialogOpened):
                $ SSSSS.Autosaver.trySavePendingSave()
        else:
            button:
                xfill True
                yfill True

                key "mousedown_1" action SSSSS.Autosaver.HandlePress()
init -9999 python:
    renpy.config.search_prefixes.append("SSSSS/src/assets/") # Provides discoverability for assets that are used in SSSSS

init 51 python in SSSSS:
    _constant = True

    Playthroughs = PlaythroughsClass()
    SaveSystem = SaveSystemClass()
    Choices = ChoicesDetectorClass()
    Autosaver = AutosaverClass()
    Pagination = PaginationClass()

    SaveSystem.setupLocations()

    print(Playthroughs.activePlaythroughOrNone)
    if Playthroughs.activePlaythroughOrNone == None:
        Playthroughs.activateNative()

    def afterLoadCallback():
        Autosaver.afterLoadSavePositionPending = True

    def startInteractCallback():
        if(not renpy.get_screen('SSSSS_SidepanelHolder')):
            renpy.show_screen('SSSSS_SidepanelHolder')

            if(renpy.store.persistent.SSSSS_playthroughs != None and renpy.store.persistent.SSSSS_lastActivePlaythrough != None):
                Playthroughs.activateByID(renpy.store.persistent.SSSSS_lastActivePlaythrough)

        if(not renpy.get_screen('SSSSS_Overlay')):
            renpy.show_screen('SSSSS_Overlay')

    class ToggleSidepanel(renpy.ui.Action):
        def __call__(self):
            if(not hasattr(renpy.config, "SSSSS_show_sidepanel")):
                renpy.config.SSSSS_show_sidepanel = False

            renpy.config.SSSSS_show_sidepanel = not renpy.config.SSSSS_show_sidepanel
            renpy.restart_interaction()

init 999 python:
    if not 'SSSSSsidepanel' in config.layers: config.layers.append('SSSSSsidepanel')

    renpy.config.after_load_callbacks.append(SSSSS.afterLoadCallback)
    renpy.config.start_interact_callbacks.append(SSSSS.startInteractCallback)
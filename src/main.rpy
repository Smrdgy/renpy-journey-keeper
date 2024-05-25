init -9999 python:
    renpy.config.search_prefixes.append("SSSSS/src/assets/") # Provides discoverability for assets that are used in SSSSS

init 51 python in SSSSS:
    _constant = True

    Playthroughs = PlaythroughsClass()
    SaveSystem = SaveSystemClass()
    Choices = ChoicesDetectorClass()
    Autosaver = AutosaverClass()
    Pagination = PaginationClass()
    Memories = MemoriesClass()

    SaveSystem.setupLocations()

    if Playthroughs.activePlaythroughOrNone == None and renpy.store.persistent.SSSSS_lastActivePlaythrough != None:
        Playthroughs.activateByID(renpy.store.persistent.SSSSS_lastActivePlaythrough)
    else:
        Playthroughs.activateNative()

    def afterLoadCallback():
        if(Autosaver.activeSlotPending != None):
            Autosaver.suppressAutosaveConfirm = False
            Autosaver.setActiveSlot(Autosaver.activeSlotPending)
            Autosaver.activeSlotPending = None

        Autosaver.afterLoadSavePositionPending = True

    def startInteractCallback():
        SaveSystem.overrideNativeLocation()

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
    if not 'w_s_e_s_w' in renpy.config.gestures:
        renpy.config.gestures['w_s_e_s_w'] = 'K_SCROLLOCK'

    if not 'SSSSSsidepanel' in config.layers:
        config.layers.insert(config.layers.index("overlay"), 'SSSSSsidepanel')
    
    if not 'SSSSSoverlay' in config.layers:
        config.layers.insert(config.layers.index("overlay"), 'SSSSSoverlay')

    renpy.config.after_load_callbacks.append(SSSSS.afterLoadCallback)
    renpy.config.start_interact_callbacks.append(SSSSS.startInteractCallback)
init -9999 python:
    renpy.config.search_prefixes.append("SSSSS/src/assets/") # Provides discoverability for assets that are used in SSSSS

init 51 python in SSSSS:
    _constant = True

    Playthroughs = PlaythroughsClass()
    SaveSystem = SaveSystemClass()
    Choices = ChoicesDetectorClass()
    Autosaver = AutosaverClass()

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
    if not 'SSSSSoverlay' in config.layers: config.layers.append('SSSSSoverlay')

    renpy.config.start_interact_callbacks.append(SSSSS.startInteractCallback)
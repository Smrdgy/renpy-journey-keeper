init -9999 python:
    renpy.config.search_prefixes.append("SSSSS/src/assets/") # Provides discoverability for assets that are used in SSSSS

init 51 python in SSSSS:
    _constant = True

    Playthroughs = PlaythroughsClass()
    SaveSystem = SaveSystemClass()
    Choices = ChoicesDetectorClass()
    Autosaver = AutosaverClass()

    def afterLoad():
        renpy.show_screen('SSSSS_Overlay')

    def startInteractCallback():
        if(not hasattr(renpy.config, "SSSSS_shows_sidepanel")):
            renpy.show_screen('SSSSS_SidepanelHolder')

            if(renpy.store.persistent.SSSSS_playthroughs != None and renpy.store.persistent.SSSSS_lastActivePlaythrough != None):
                Playthroughs.activateByName(renpy.store.persistent.SSSSS_lastActivePlaythrough)

            renpy.config.SSSSS_shows_sidepanel = True

init 999 python:
    if not 'SSSSSsidepanel' in config.layers: config.layers.append('SSSSSsidepanel')
    if not 'SSSSSoverlay' in config.layers: config.layers.append('SSSSSoverlay')

    renpy.config.after_load_callbacks.append(SSSSS.afterLoad)
    renpy.config.start_interact_callbacks.append(SSSSS.startInteractCallback)
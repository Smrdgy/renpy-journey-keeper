init -1 python in JK:
    _constant = True

    print("Initializing {} v{}".format(MOD_NAME, MOD_VERSION))

    Settings = SettingsClass()

init python in JK:
    _constant = True

    Updater = UpdaterClass()
    SaveSystem = SaveSystemClass()
    Playthroughs = PlaythroughsClass()
    Autosaver = AutosaverClass()
    Pagination = PaginationClass()
    Memories = MemoriesClass()

    renpy.config.search_prefixes.append("JK/src/assets/") # Provides discoverability for assets that are used in JK

init 9999 python in JK:
    _constant = True

    if not 'n_e_s_w' in renpy.config.gestures:
        renpy.config.gestures['n_e_s_w'] = Settings.changeSidepanelVisibilityKey

    if not "JK_Sidepanel" in renpy.config.layers:
        renpy.config.layers.append("JK_Sidepanel")
        renpy.config.context_clear_layers.append("JK_Sidepanel")
    
    if not "JK_Overlay" in renpy.config.layers:
        renpy.add_layer("JK_Overlay", above="JK_Sidepanel")
        renpy.config.context_clear_layers.append("JK_Overlay")

    print("{} is ready".format(MOD_NAME))
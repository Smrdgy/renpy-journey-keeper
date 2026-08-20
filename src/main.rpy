init -1 python in JK:
    _constant = True

    print("Initializing {} v{}".format(MOD_NAME, MOD_VERSION))

    Settings = SettingsClass()

init python in JK:
    _constant = True

    Notifications = NotificationsClass()
    Updater = UpdaterClass()
    SaveSystem = SaveSystemClass()
    Playthroughs = PlaythroughsClass()
    Autosaver = AutosaverClass()
    Pagination = PaginationClass()
    Memories = MemoriesClass()
    ThumbnailCache = ThumbnailCacheClass()
    Autocomplete = AutocompleteClass()

init 999999999999 python in JK: # Delayed by a huge number to ensure that this is not overridden by a game
    _constant = True

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

    # Deliberately not menu_clear and not in context_clear_layers: unlike JK_Overlay (tooltips,
    # confirms, pickers - fine to wipe when entering/leaving the game menu), the autocomplete bar
    # must survive visiting the save/load screen mid-run, since that's the game menu context.
    if not "JK_Autocomplete" in renpy.config.layers:
        renpy.add_layer("JK_Autocomplete", below="JK_Overlay", menu_clear=False)

    print("{} is ready".format(MOD_NAME))
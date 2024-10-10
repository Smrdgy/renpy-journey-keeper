init 51 python in SSSSS:
    _constant = True

    hasColsAndRowsConfiguration = hasattr(renpy.store.gui, "file_slot_cols") and hasattr(renpy.store.gui, "file_slot_rows")

    Playthroughs = PlaythroughsClass()
    SaveSystem = SaveSystemClass()
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
            if(not hasattr(renpy.config, "SSSSS_sidepanelVisibilityMode")):
                renpy.config.SSSSS_sidepanelVisibilityMode = True

            if renpy.config.SSSSS_sidepanelVisibilityMode == True:
                renpy.config.SSSSS_sidepanelVisibilityMode = False
                renpy.notify("Sidepanel is now hidden at all times")
            elif renpy.config.SSSSS_sidepanelVisibilityMode == False:
                renpy.config.SSSSS_sidepanelVisibilityMode = None
                renpy.notify("Sidepanel is now visible only in save/load screen")
            else:
                renpy.config.SSSSS_sidepanelVisibilityMode = True
                renpy.notify("Sidepanel is now visible at all times")

            renpy.restart_interaction()

init 999 python:
    renpy.config.search_prefixes.append("SSSSS/src/assets/") # Provides discoverability for assets that are used in SSSSS

    if not 'w_s_e_s_w' in renpy.config.gestures:
        renpy.config.gestures['w_s_e_s_w'] = 'alt_K_p'

    if not 'SSSSSsidepanel' in config.layers:
        config.layers.insert(config.layers.index("overlay"), 'SSSSSsidepanel')
        config.context_clear_layers.append('SSSSSsidepanel')
    
    if not 'SSSSSoverlay' in config.layers:
        config.layers.insert(config.layers.index("overlay"), 'SSSSSoverlay')
        config.context_clear_layers.append('SSSSSoverlay')

    renpy.config.after_load_callbacks.append(SSSSS.afterLoadCallback)
    renpy.config.start_interact_callbacks.append(SSSSS.startInteractCallback)

    # Input.
    renpy.config.keymap.update({
        'input_backspace': [ 'K_BACKSPACE', 'repeat_K_BACKSPACE' ] if not hasattr(renpy.config.keymap, 'input_backspace') else renpy.config.keymap.input_backspace,
        'input_next_line': [ 'K_RETURN', 'repeat_K_RETURN', 'K_KP_ENTER', 'repeat_K_KP_ENTER' ] if not hasattr(renpy.config.keymap, 'input_next_line') else renpy.config.keymap.input_next_line,
        'input_left': [ 'K_LEFT', 'repeat_K_LEFT' ] if not hasattr(renpy.config.keymap, 'input_left') else renpy.config.keymap.input_left,
        'input_right': [ 'K_RIGHT', 'repeat_K_RIGHT' ] if not hasattr(renpy.config.keymap, 'input_right') else renpy.config.keymap.input_right,
        'input_up': [ 'K_UP', 'repeat_K_UP' ] if not hasattr(renpy.config.keymap, 'input_up') else renpy.config.keymap.input_up,
        'input_down': [ 'K_DOWN', 'repeat_K_DOWN' ] if not hasattr(renpy.config.keymap, 'input_down') else renpy.config.keymap.input_down,
        'input_delete': [ 'K_DELETE', 'repeat_K_DELETE' ] if not hasattr(renpy.config.keymap, 'input_delete') else renpy.config.keymap.input_delete,
        'input_home': [ 'K_HOME', 'meta_K_LEFT' ] if not hasattr(renpy.config.keymap, 'input_home') else renpy.config.keymap.input_home,
        'input_end': [ 'K_END', 'meta_K_RIGHT' ] if not hasattr(renpy.config.keymap, 'input_end') else renpy.config.keymap.input_end,
        'input_copy': [ 'ctrl_noshift_K_INSERT', 'ctrl_noshift_K_c', 'meta_noshift_K_c' ] if not hasattr(renpy.config.keymap, 'input_copy') else renpy.config.keymap.input_copy,
        'input_paste': [ 'shift_K_INSERT', 'ctrl_noshift_K_v', 'meta_noshift_K_v' ] if not hasattr(renpy.config.keymap, 'input_paste') else renpy.config.keymap.input_paste,
        'input_jump_word_left': [ 'ctrl_K_LEFT', 'repeat_ctrl_K_LEFT' ] if not hasattr(renpy.config.keymap, 'input_jump_word_left') else renpy.config.keymap.input_jump_word_left,
        'input_jump_word_right': [ 'ctrl_K_RIGHT', 'repeat_ctrl_K_RIGHT' ] if not hasattr(renpy.config.keymap, 'input_jump_word_right') else renpy.config.keymap.input_jump_word_right,
        'input_delete_word': [ 'repeat_ctrl_K_BACKSPACE' ] if not hasattr(renpy.config.keymap, 'input_delete_word') else renpy.config.keymap.input_delete_word,
        'input_delete_full': [ 'repeat_meta_K_BACKSPACE' ] if not hasattr(renpy.config.keymap, 'input_delete_full') else renpy.config.keymap.input_delete_full,
    })
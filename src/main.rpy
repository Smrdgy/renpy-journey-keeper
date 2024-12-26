init -1000 python in URPS:
    _constant = True

    Settings = SettingsClass()

init 51 python in URPS:
    _constant = True

    Updater = UpdaterClass()
    Playthroughs = PlaythroughsClass()
    SaveSystem = SaveSystemClass()
    Autosaver = AutosaverClass()
    Pagination = PaginationClass()
    Memories = MemoriesClass()

    SaveSystem.setupLocations()

    if Playthroughs.activePlaythroughOrNone == None and renpy.store.persistent.URPS_lastActivePlaythrough != None:
        Playthroughs.activateByID(renpy.store.persistent.URPS_lastActivePlaythrough)
    
    if Playthroughs.activePlaythroughOrNone is None:
        Playthroughs.activateNative()

    def afterLoadCallback():
        if(Autosaver.activeSlotPending != None):
            Autosaver.suppressAutosaveConfirm = False
            Autosaver.setActiveSlot(Autosaver.activeSlotPending)
            Autosaver.activeSlotPending = None

            if Settings.offsetSlotAfterManualSaveIsLoaded:
                Autosaver.setNextSlot()

        Autosaver.afterLoadSavePositionPending = True

    def startInteractCallback():
        SaveSystem.overrideNativeLocation()

        if(not renpy.get_screen('URPS_SidepanelHolder')):
            renpy.show_screen('URPS_SidepanelHolder')

        if(not renpy.get_screen('URPS_Overlay')):
            renpy.show_screen('URPS_Overlay')

        if renpy.store.persistent.URPS_SizeAdjustmentRollbackValue != None and renpy.get_screen("URPS_ConfirmSizeAdjustment") is None:
            renpy.show_screen('URPS_ConfirmSizeAdjustment')

        if Settings.updaterEnabled and not Updater.checked_for_update:
            renpy.invoke_in_thread(Updater.check_for_update)

    def saveJsonCallback(json):
        if Autosaver.pendingSave:
            json["_URPS_choice"] = Autosaver.pendingSave.choice

    class ToggleSidepanel(renpy.ui.Action):
        def __call__(self):
            if not hasattr(renpy.config, "URPS_sidepanelVisibilityMode") or renpy.config.URPS_sidepanelVisibilityMode == None:
                # Visible at all times
                SetSidepanelVisibilityAction(visibility=True)()
            elif renpy.config.URPS_sidepanelVisibilityMode == True:
                # Hidden at all times
                SetSidepanelVisibilityAction(visibility=False)()
            elif renpy.config.URPS_sidepanelVisibilityMode == False:
                # Visible only in save/load screen
                SetSidepanelVisibilityAction(visibility=None)()
            else:
                # Visible at all times
                SetSidepanelVisibilityAction(visibility=True)()

            renpy.restart_interaction()
        
    class SetSidepanelVisibilityAction(renpy.ui.Action):
        def __init__(self, visibility):
            self.visibility = visibility # True/False/None

        def __call__(self):
            renpy.config.URPS_sidepanelVisibilityMode = self.visibility

            if renpy.config.URPS_sidepanelVisibilityMode == True:
                renpy.notify("Sidepanel is now visible at all times")
            elif renpy.config.URPS_sidepanelVisibilityMode == False:
                renpy.notify("Sidepanel is now hidden at all times")
            elif renpy.config.URPS_sidepanelVisibilityMode == None:
                renpy.notify("Sidepanel is now visible only on the save/load screen")
            else:
                renpy.notify("Sidepanel is now visible at all times")

            renpy.restart_interaction()

init 999 python in URPS:
    renpy.config.search_prefixes.append("URPS/src/assets/") # Provides discoverability for assets that are used in URPS

    if not 'n_e_s_w' in renpy.config.gestures:
        renpy.config.gestures['n_e_s_w'] = Settings.changeSidepanelVisibilityKey

    if not "URPS_Sidepanel" in renpy.config.layers:
        renpy.config.layers.append("URPS_Sidepanel")
        renpy.config.context_clear_layers.append("URPS_Sidepanel")
    
    if not "URPS_Overlay" in renpy.config.layers:
        renpy.add_layer("URPS_Overlay", above="URPS_Sidepanel")
        renpy.config.context_clear_layers.append("URPS_Overlay")

    renpy.config.after_load_callbacks.append(afterLoadCallback)
    renpy.config.start_interact_callbacks.append(startInteractCallback)
    renpy.config.save_json_callbacks.append(saveJsonCallback)

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
        'input_content_start': [ 'shift_K_HOME' ],
        'input_content_end': [ 'shift_K_END' ],
        # 'input_next_input': ['noshift_K_TAB'], #TODO: Finish prev/next input via TAB
        # 'input_prev_input': ['shift_K_TAB']
    })
init -1 python in JK:
    _constant = True

    print("Initializing {} v{}".format(MOD_NAME, MOD_VERSION))

    Settings = SettingsClass()

init python in JK:
    _constant = True

    Updater = UpdaterClass()
    Playthroughs = PlaythroughsClass()
    SaveSystem = SaveSystemClass()
    Autosaver = AutosaverClass()
    Pagination = PaginationClass()
    Memories = MemoriesClass()

    if Playthroughs.active_playthrough_or_none == None and renpy.store.persistent.JK_ActivePlaythrough != None:
        Playthroughs.activate_by_id(renpy.store.persistent.JK_ActivePlaythrough)
    
    if Playthroughs.active_playthrough_or_none is None:
        Playthroughs.activate_native()

    def afterLoadCallback():
        Autosaver.prevent_autosaving = False

        if(Autosaver.active_slot_pending != None):
            Autosaver.suppress_autosave_confirm = False
            Autosaver.set_active_slot(Autosaver.active_slot_pending)
            Autosaver.active_slot_pending = None

            if Settings.offsetSlotAfterManualSaveIsLoaded:
                Autosaver.set_next_slot()

        Autosaver.after_load_save_position_pending = True

    def startInteractCallback():
        # Perform utter restart due to pending update, but only once!
        # If something were to break, a user might get stuck in infinite loop and that's obviously not good.
        if Updater.pending_utter_restart and not renpy.store.persistent.JK_TriedUtterRestart:
            renpy.store.persistent.JK_TriedUtterRestart = True
            renpy.utter_restart()
            return

        SaveSystem.override_native_location()
        renpy.loadsave.clear_cache()
        SaveSystem.multilocation.scan()

        if(not renpy.get_screen('JK_SidepanelHolder')):
            renpy.show_screen('JK_SidepanelHolder')

        if(not renpy.get_screen('JK_Overlay')):
            renpy.show_screen('JK_Overlay')

        if renpy.store.persistent.JK_SizeAdjustmentRollbackValue != None and renpy.get_screen("JK_ConfirmSizeAdjustment") is None:
            renpy.show_screen('JK_ConfirmSizeAdjustment')

        if Settings.updaterEnabled and not Updater.checked_for_update:
            renpy.invoke_in_thread(Updater.check_for_update)

    def saveJsonCallback(json):
        if Autosaver.pending_save:
            json["_JK_choice"] = Autosaver.pending_save.choice

    def wait_for_start_label_callback(statement):
        if Autosaver.prevent_autosaving and statement == "label":
            current = renpy.game.context().current
            script = renpy.game.script.lookup(current)

            if script.name == "start":
                Autosaver.prevent_autosaving = False

    class ToggleSidepanel(renpy.ui.Action):
        def __call__(self):
            if not hasattr(renpy.config, "JK_sidepanelVisibilityMode") or renpy.config.JK_sidepanelVisibilityMode == None:
                # Visible at all times
                SetSidepanelVisibilityAction(visibility=True)()
            elif renpy.config.JK_sidepanelVisibilityMode == True:
                # Hidden at all times
                SetSidepanelVisibilityAction(visibility=False)()
            elif renpy.config.JK_sidepanelVisibilityMode == False:
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
            renpy.config.JK_sidepanelVisibilityMode = self.visibility

            if renpy.config.JK_sidepanelVisibilityMode == True:
                renpy.notify("Sidepanel is now visible at all times")
            elif renpy.config.JK_sidepanelVisibilityMode == False:
                renpy.notify("Sidepanel is now hidden at all times")
            elif renpy.config.JK_sidepanelVisibilityMode == None:
                renpy.notify("Sidepanel is now visible only on the save/load screen")
            else:
                renpy.notify("Sidepanel is now visible at all times")

            renpy.restart_interaction()

init 9999 python in JK:
    renpy.config.search_prefixes.append("JK/src/assets/") # Provides discoverability for assets that are used in JK

    if not 'n_e_s_w' in renpy.config.gestures:
        renpy.config.gestures['n_e_s_w'] = Settings.changeSidepanelVisibilityKey

    if not "JK_Sidepanel" in renpy.config.layers:
        renpy.config.layers.append("JK_Sidepanel")
        renpy.config.context_clear_layers.append("JK_Sidepanel")
    
    if not "JK_Overlay" in renpy.config.layers:
        renpy.add_layer("JK_Overlay", above="JK_Sidepanel")
        renpy.config.context_clear_layers.append("JK_Overlay")

    renpy.config.after_load_callbacks.append(afterLoadCallback)
    renpy.config.start_interact_callbacks.append(startInteractCallback)
    renpy.config.save_json_callbacks.append(saveJsonCallback)
    renpy.config.statement_callbacks.append(wait_for_start_label_callback)

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
        'input_select_all': [ 'ctrl_K_a' ],
        # 'input_next_input': ['noshift_K_TAB'], #TODO: Finish prev/next input via TAB
        # 'input_prev_input': ['shift_K_TAB']
    })

    # Link handler to run any action on click: `text "{a=JK_Run:SomeAction()}Some clickable text{/a}"`
    def __run(arg):
        renpy.python.py_exec("renpy.run({})".format(arg))

    renpy.config.hyperlink_handlers["JK_Run"] = __run


    print("{} is ready".format(MOD_NAME))
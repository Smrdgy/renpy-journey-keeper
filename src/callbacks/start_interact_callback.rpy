init 9999 python in JK:
    _constant = True

    def __start_interact_callback():
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

    renpy.config.start_interact_callbacks.append(__start_interact_callback)
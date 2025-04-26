init 9999 python in JK:
    _constant = True

    def __after_load_callback():
        Autosaver.prevent_autosaving = False

        if(Autosaver.active_slot_pending != None):
            Autosaver.suppress_autosave_confirm = False
            Autosaver.set_active_slot(Autosaver.active_slot_pending)
            Autosaver.active_slot_pending = None

            if Settings.offsetSlotAfterManualSaveIsLoaded:
                Autosaver.set_next_slot()

        Autosaver.after_load_save_position_pending = True

    renpy.config.after_load_callbacks.append(__after_load_callback)
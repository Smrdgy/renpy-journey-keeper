init 9999 python in JK:
    _constant = True

    def __after_load_callback():
        Autosaver.prevent_autosaving = False

        if(Autosaver.active_slot_pending != None):
            Autosaver.suppress_autosave_confirm = False
            Autosaver.set_active_slot(Autosaver.active_slot_pending)

            # set_active_slot() just set prev_active_slot from the *current* JK_ActiveSlot,
            # but by this point the load's rollback has already restored JK_ActiveSlot to
            # whatever was pickled inside the loaded slot - i.e. the same slot being loaded,
            # so that comparison is always a no-op right after a load. Overwrite it with the
            # slot that was actually active before this load happened (captured in
            # __before_load), so the overwrite-confirm check can correctly detect "we just
            # loaded a different slot than the one we're about to autosave into."
            Autosaver.prev_active_slot = Autosaver.slot_before_load

            Autosaver.active_slot_pending = None

            if Settings.offsetSlotAfterManualSaveIsLoaded:
                Autosaver.set_next_slot()

        Autosaver.after_load_save_position_pending = True

    renpy.config.after_load_callbacks.append(__after_load_callback)
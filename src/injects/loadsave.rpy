init 9999 python in JK:
    _constant = True
    
    def __before_load(slotname):
        Autosaver.active_slot_pending = slotname
        Autosaver.prevent_confirm_on_large_page_jump = True
        Autosaver.suppress_autosave_confirm = False

        # Captured now, before the rollback restores JK_ActiveSlot to whatever was
        # pickled inside the slot being loaded - after_load_callback needs the
        # genuine pre-load slot to detect "did loading actually move us elsewhere."
        Autosaver.slot_before_load = renpy.store.JK_ActiveSlot
    
    def __before_save(slotname):
        #Ignore temporary saves used to stage autosave/quicksave writes
        if AutosaverClass.PendingSaveClass.temp_save_slotname in slotname or Playthroughs.QuickSaveAction.temp_save_slotname in slotname:
            return

        #Ignore quick and auto saves
        if "quick" in slotname or "auto" in slotname:
            return

        if Settings.offsetSlotAfterManualSave:
            if Settings.offsetSlotBlacklist.strip() != "":
                for pattern in Settings.offsetSlotBlacklist.split(","):
                    pattern = pattern.strip()
                    if pattern and (slotname == pattern or Utils.wildcard_match(slotname, pattern)):
                        return

            Autosaver.set_active_slot(slotname)

            if not Utils.is_displaying_choices_in_any_context():
                Autosaver.set_next_slot()

    def __load_partial(func, *args, **kwargs):
        if hasattr(func, "_original"):
            func = func._original

        def new_funct(*new_args, **new_kwargs):
            new_kwargs.update(kwargs.copy())

            if(new_args and new_args[0]):
                __before_load(new_args[0])

            Memories.memoryInProgress = False

            return func(*(args + new_args), **new_kwargs)

        new_funct._original = func

        return new_funct

    def __save_partial(func, *args, **kwargs):
        if hasattr(func, "_original"):
            func = func._original

        def new_funct(*new_args, **new_kwargs):
            new_kwargs.update(kwargs.copy())

            if(new_args and new_args[0]):
                __before_save(new_args[0])

            return func(*(args + new_args), **new_kwargs)

        new_funct._original = func

        return new_funct


    renpy.load = __load_partial(renpy.load)
    renpy.save = __save_partial(renpy.save)

init 9999 python in JK:
    _constant = True
    
    def __before_load(slotname):
        Autosaver.active_slot_pending = slotname
        Autosaver.prevent_confirm_on_large_page_jump = True
        Autosaver.suppress_autosave_confirm = False
    
    def __before_save(slotname):
        #Ignore temporary save
        if AutosaverClass.PendingSaveClass.temp_save_slotname in slotname:
            return

        if Settings.offsetSlotAfterManualSave:
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

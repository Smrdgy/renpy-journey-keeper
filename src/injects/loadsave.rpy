init -99 python in JK:
    _constant = True
    
    def before_load(slotname):
        Autosaver.activeSlotPending = slotname
        Autosaver.suppressAutosaveConfirm = False
    
    def before_save(slotname):
        #Ignore temporary save
        if AutosaverClass.PendingSaveClass.temp_save_slotname in slotname:
            return

        if Settings.offsetSlotAfterManualSave:
            Autosaver.setActiveSlot(slotname)

            if not Utils.isDisplayingChoicesInAnyContext():
                Autosaver.setNextSlot()

    def load_partial(func, *args, **kwargs):
        def new_funct(*new_args, **new_kwargs):
            new_kwargs.update(kwargs.copy())

            if(new_args and new_args[0]):
                before_load(new_args[0])

            Memories.memoryInProgress = False

            return func(*(args + new_args), **new_kwargs)
        return new_funct

    def save_partial(func, *args, **kwargs):
        def new_funct(*new_args, **new_kwargs):
            new_kwargs.update(kwargs.copy())

            if(new_args and new_args[0]):
                before_save(new_args[0])

            return func(*(args + new_args), **new_kwargs)
        return new_funct


    renpy.load = load_partial(renpy.load)
    renpy.save = save_partial(renpy.save)

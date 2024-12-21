init -99 python in URPS:
    _constant = True
    
    def before_load(slotname):
        Autosaver.activeSlotPending = slotname
        Autosaver.suppressAutosaveConfirm = False
    
    def before_save(slotname):
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

    def write_file_partial(func, *args, **kwargs):#TODO: Remove
        def new_funct(*new_args, **new_kwargs):
            new_kwargs.update(kwargs.copy())

            print(args, new_args, new_kwargs)

            fn = func(*(args + new_args), **new_kwargs)

            return fn
        return new_funct

    renpy.loadsave.SaveRecord.write_file = write_file_partial(renpy.loadsave.SaveRecord.write_file)#TODO: Remove

init -99 python in SSSSS:
    _constant = True
    
    def before_load(slotname):
        Autosaver.lastChoice = None
        Autosaver.activeSlotPending = slotname
        Autosaver.suppressAutosaveConfirm = False
    
    def before_save(slotname):
        Autosaver.lastChoice = None

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

    def write_file_partial(func, *args, **kwargs):
        def new_funct(*new_args, **new_kwargs):
            new_kwargs.update(kwargs.copy())

            fn = func(*(args + new_args), **new_kwargs)

            if(Autosaver.lastChoice != None):
                import zipfile

                filename = new_args[1]

                zf = zipfile.ZipFile(filename, "a", zipfile.ZIP_DEFLATED)
                zf.writestr("choice", Autosaver.lastChoice.encode("utf-8"))
                zf.close()

                Autosaver.lastChoice = None

            return fn
        return new_funct

    renpy.loadsave.SaveRecord.write_file = write_file_partial(renpy.loadsave.SaveRecord.write_file)

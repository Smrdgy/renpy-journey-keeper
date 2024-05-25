init -99 python:
    _constant = True
    
    def bafore_saveload(slotname):
        SSSSS.Autosaver.lastChoice = None
        SSSSS.Autosaver.activeSlotPending = slotname

    def load_partial(func, *args, **kwargs):
        def new_funct(*new_args, **new_kwargs):
            new_kwargs.update(kwargs.copy())

            if(new_args and new_args[0]):
                bafore_saveload(new_args[0])

            SSSSS.Memories.memoryInProgress = False

            return func(*(args + new_args), **new_kwargs)
        return new_funct
    _constant = True

    def save_partial(func, *args, **kwargs):
        def new_funct(*new_args, **new_kwargs):
            new_kwargs.update(kwargs.copy())

            if(new_args and new_args[0]):
                bafore_saveload(new_args[0])

            return func(*(args + new_args), **new_kwargs)
        return new_funct


    renpy.load = load_partial(renpy.load)
    renpy.save = save_partial(renpy.save)

    def write_file_partial(func, *args, **kwargs):
        def new_funct(*new_args, **new_kwargs):
            new_kwargs.update(kwargs.copy())

            fn = func(*(args + new_args), **new_kwargs)

            if(SSSSS.Autosaver.lastChoice != None):
                import zipfile

                filename = new_args[1]

                zf = zipfile.ZipFile(filename, "a", zipfile.ZIP_DEFLATED)
                zf.writestr("choice", SSSSS.Autosaver.lastChoice.encode("utf-8"))
                zf.close()

                SSSSS.Autosaver.lastChoice = None

            return fn
        return new_funct

    renpy.loadsave.SaveRecord.write_file = write_file_partial(renpy.loadsave.SaveRecord.write_file)

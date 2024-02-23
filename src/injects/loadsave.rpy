init -99 python:
    def my_partial(func, *args, **kwargs):
        def new_funct(*new_args, **new_kwargs):
            new_kwargs.update(kwargs.copy())

            if(new_args and new_args[0]):
                SSSSS.Autosaver.lastChoice = None
                SSSSS.Autosaver.setActiveSlot(new_args[0])

            return func(*(args + new_args), **new_kwargs)
        return new_funct


    renpy.load = my_partial(renpy.load)
    renpy.save = my_partial(renpy.save)

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

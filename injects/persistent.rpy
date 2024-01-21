init -99 python:
    def my_partial(func, *args, **kwargs):
        def new_funct(*new_args, **new_kwargs):
            new_kwargs.update(kwargs.copy())
            
            mylocation = renpy.loadsave.location
            renpy.loadsave.location = SSSSS.SaveSystem.defaultLocation
            
            fn = func(*(args + new_args), **new_kwargs)

            renpy.loadsave.location = mylocation

            return fn
        return new_funct

    renpy.persistent.check_update = my_partial(renpy.persistent.check_update)
    renpy.persistent.update = my_partial(renpy.persistent.update)
    renpy.persistent.save = my_partial(renpy.persistent.save)

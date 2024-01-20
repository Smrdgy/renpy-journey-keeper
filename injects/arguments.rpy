init -99 python:
    def my_partial(func, *args, **kwargs):
        def new_funct(*new_args, **new_kwargs):
            new_kwargs.update(kwargs.copy())
            
            mylocation = renpy.loadsave.location
            renpy.loadsave.location = SSSSS.SaveSystem.defaultLocation
            fn = func(*args, *new_args, **kwargs)
            renpy.loadsave.location = mylocation

            return fn
        return new_funct

    renpy.arguments.rmpersistent = my_partial(renpy.arguments.rmpersistent)
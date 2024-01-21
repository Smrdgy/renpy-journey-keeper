init -99 python:
    def my_partial(func, *args, **kwargs):
        def new_funct(*new_args, **new_kwargs):
            new_kwargs.update(kwargs.copy())

            if(new_args and new_args[0]):
                SSSSS.Autosaver.setActiveSlot(new_args[0])

            return func(*(args + new_args), **new_kwargs)
        return new_funct


    renpy.load = my_partial(renpy.load)
    renpy.save = my_partial(renpy.save)

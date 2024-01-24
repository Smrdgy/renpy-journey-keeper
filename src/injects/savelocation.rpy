init -99 python:
    def my_partial(func, *args, **kwargs):
        def new_funct(*new_args, **new_kwargs):
            new_kwargs.update(kwargs.copy())
            
            fn = func(*(args + new_args), **new_kwargs)

            if(renpy.store.persistent.SSSSS_playthroughs != None and renpy.store.persistent.SSSSS_lastActivePlaythrough != None):
                SSSSS.Playthroughs.activateByName(renpy.store.persistent.SSSSS_lastActivePlaythrough)

            return fn
        return new_funct

    renpy.savelocation.init = my_partial(renpy.savelocation.init)
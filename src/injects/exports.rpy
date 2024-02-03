init -99 python:
    def my_partial(func, *args, **kwargs):
        def new_funct(*new_args, **new_kwargs):
            new_kwargs.update(kwargs.copy())
            
            if SSSSS.Playthroughs.activePlaythrough != None and SSSSS.Playthroughs.activePlaythrough.autosaveOnChoices:
                SSSSS.Autosaver.registerChoices()

            return func(*(args + new_args), **new_kwargs)
        return new_funct


    renpy.choice_for_skipping = my_partial(renpy.choice_for_skipping)
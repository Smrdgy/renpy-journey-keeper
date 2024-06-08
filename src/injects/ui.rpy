init -99 python in SSSSS:
    _constant = True

    def my_partial(func, *args, **kwargs):
        def new_funct(*new_args, **new_kwargs):
            new_kwargs.update(kwargs.copy())
        
            # Prevent making any autosave actions when viewing a memory or a replay
            if not Memories.memoryInProgress and not renpy.store._in_replay:
                Autosaver.handleChoiceSelection(new_args[0])

            fn = func(*(args + new_args), **new_kwargs)

            return fn
        return new_funct

    renpy.ui.ChoiceReturn.__call__ = my_partial(renpy.ui.ChoiceReturn.__call__)
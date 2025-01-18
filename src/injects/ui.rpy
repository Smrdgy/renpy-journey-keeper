init 9999 python in JK:
    _constant = True

    def my_partial(func, *args, **kwargs):
        def new_funct(*new_args, **new_kwargs):
            new_kwargs.update(kwargs.copy())
        
            # Prevent making any autosave action when the game is not initialized yet or the player is viewing a memory or a replay
            if not Autosaver.prevent_autosaving and not Memories.memoryInProgress and not renpy.store._in_replay and (Settings.autosaveOnSingletonChoice or Utils.isDisplayingMultipleChoices()):
                Autosaver.handleChoiceSelection(new_args[0])

            fn = func(*(args + new_args), **new_kwargs)

            return fn
        return new_funct

    renpy.ui.ChoiceReturn.__call__ = my_partial(renpy.ui.ChoiceReturn.__call__)
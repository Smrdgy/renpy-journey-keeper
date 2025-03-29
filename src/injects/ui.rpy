init 9999 python in JK:
    _constant = True

    def __can_perform_autosave():
        # Prevent making any autosave action when the game is not initialized yet or the player is viewing a memory or a replay
        return not Autosaver.prevent_autosaving and not Memories.memoryInProgress and not renpy.store._in_replay and (Settings.autosaveOnSingletonChoice or Utils.is_displaying_multiple_choices())

    def __choice_return_call_partial(func, *args, **kwargs):
        if hasattr(func, "_original"):
            func = func._original

        def new_funct(*new_args, **new_kwargs):
            new_kwargs.update(kwargs.copy())
        
            Autosaver.handle_choice_selection(new_args[0])

            fn = func(*(args + new_args), **new_kwargs)

            return fn

        new_funct._original = func

        return new_funct

    def __button_init_partial(func, *args, **kwargs):
        if hasattr(func, "_original"):
            func = func._original

        def new_init_funct(button, *new_args, **new_kwargs):
            new_kwargs.update(kwargs.copy())

            func(button, *(args + new_args), **new_kwargs)

            # Don't overwrite action if the feature is disabled
            if not Settings.autosaveOnNormalButtonsWithJump:
                return

            class Action(renpy.ui.Action):
                def __init__(self, button, action, node):
                    self.button = button
                    self.original_action = action
                    self.node = node
                
                def __call__(self, *args, **kwargs):
                    # In case the button hasn't been reconstructed after disabling the choice, make sure the autosave isn't performed.
                    if Settings.autosaveOnNormalButtonsWithJump:
                        Autosaver.handle_any_button_click(self.button)

                    return renpy.display.behavior.run(self.original_action, *args, **kwargs)

            # Determine node
            node = None

            # **Warning!** renpy.ast.Jump != renpy.store.Jump
            if isinstance(button.action, renpy.ast.Jump) or isinstance(button.action, renpy.store.Jump):
                node = button.action

            elif isinstance(button.action, list) or isinstance(button.action, python_list):
                for n in button.action:
                    if isinstance(n, renpy.ast.Jump) or isinstance(n, renpy.store.Jump):
                        node = n

            # Make sure the button has Jump action, that way, we can tell at least with some degree of confidence that the button is used for as a choice.
            #  Otherwise we would get a lot of false positives from the rest of the buttons, like toggle buttons inside Preferences, confirm dialog, etc.
            if isinstance(node, renpy.ast.Jump) or isinstance(node, renpy.store.Jump):
                button.action = Action(button, button.action, node)

        new_init_funct._original = func

        return new_init_funct

    renpy.ui.ChoiceReturn.__call__ = __choice_return_call_partial(renpy.ui.ChoiceReturn.__call__)
    renpy.display.behavior.Button.__init__ = __button_init_partial(renpy.display.behavior.Button.__init__)
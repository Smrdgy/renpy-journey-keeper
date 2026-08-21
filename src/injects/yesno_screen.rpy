init 9999 python in JK:
    _constant = True

    # Ren'Py's own yes/no prompts (quit, return to main menu, delete/overwrite save, skip -
    # anything using the stock Confirm action or layout.yesno_screen) show on the "screens"
    # layer by default, which sits below JK's own layers. That lets JK's UI cover or steal
    # input from them. Rather than reimplementing layout.yesno_screen (which would drop
    # whatever visuals/transitions the host game customized it with), wrap it: for the
    # duration of its call only, retarget renpy.show_screen to the JK_AboveAll layer, then
    # restore it. This leaves the original prompt logic untouched and only relocates it.
    def __yesno_screen_partial(func):
        original = getattr(func, "_original", func)

        def new_funct(*args, **kwargs):
            native_show_screen = renpy.show_screen

            def __show_screen_on_JK_AboveAll(_screen_name, *a, **kw):
                kw.setdefault("_layer", "JK_AboveAll")
                return native_show_screen(_screen_name, *a, **kw)

            renpy.show_screen = __show_screen_on_JK_AboveAll

            try:
                return original(*args, **kwargs)
            finally:
                renpy.show_screen = native_show_screen

        new_funct._original = original

        return new_funct

    renpy.store.layout.yesno_screen = __yesno_screen_partial(renpy.store.layout.yesno_screen)

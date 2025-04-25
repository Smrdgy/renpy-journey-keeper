init python in JK:
    # Link handler to run any action on click: `text "{a=JK_Run:SomeAction()}Some clickable text{/a}"`
    def __run(arg):
        renpy.python.py_exec("renpy.run({})".format(arg))

    renpy.config.hyperlink_handlers["JK_Run"] = __run
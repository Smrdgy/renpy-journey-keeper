screen JK_PendingUpdateReloadAndUpdate():
    style_prefix "JK"
    modal True

    python:
        class Reload(renpy.ui.Action):
            def __call__(self):
                renpy.utter_restart()

    vbox:
        xfill True
        yfill True

        vbox:
            xalign 0.5
            yalign 0.5

            hbox:
                xalign 0.5

                use JK_Title("Reloading...")

            use JK_YSpacer(2)

            if JK.Updater.rpa_locked_exception:
                text "This might take a minute. The game will need to reload twice—once to release the mod file and again for the update to take effect." xalign 0.5 text_align 0.5
                

    timer 0.1 action Reload()
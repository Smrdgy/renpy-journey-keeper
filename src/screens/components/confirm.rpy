screen SSSSS_Confirm(title=_("Confirm"), message=None, yes=None, no=None, yesText=_("Yes"), noText=_("No")):
    modal True

    zorder 199

    use SSSSS_Dialog(title=title, message=message, closeAction=[no, Hide("SSSSS_Confirm")], background="gui/dialog/confirm_dialog_background.png", size=(922, 378)):
        vbox:
            yfill True

        hbox:
            offset (0, -70)
            xalign 0.5

            button:
                style "SSSSS_textbutton_medium_green"
                action [yes, Hide("SSSSS_Confirm")]
                key_events True
                xalign 0.5

                text "[yesText]" yalign .5 xalign 0.5 size 28 text_align 0.5

            null width 100

            button:
                style "SSSSS_textbutton_medium_red"
                action [no, Hide("SSSSS_Confirm")]
                key_events True
                xalign 0.5

                text "[noText]" yalign .5 xalign 0.5 size 28 text_align 0.5

init python in SSSSS:
    def showConfirm(title="", message=None, yes=None, no=None, yesText="Yes", noText="No"):
        renpy.run(renpy.store.Show("SSSSS_Confirm", title=title, message=message, yes=yes, no=no, yesText=yesText, noText=noText))
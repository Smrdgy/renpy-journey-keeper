screen URPS_Confirm(title=None, message=None, yes=None, no=None, yesText=None, noText=None, yesIcon=None, noIcon=None, yesColor=None, noColor=None):
    layer "URPS_Overlay"
    style_prefix "URPS"

    modal True

    zorder 199

    python:
        yesAction = [yes, Hide("URPS_Confirm")]
        noAction = [no, Hide("URPS_Confirm")]

    key 'K_RETURN' action yesAction
    key 'K_KP_ENTER' action yesAction

    use URPS_Dialog(title=title, message=message, closeAction=noAction):
        hbox:
            xfill True
            yfill True

            style_prefix "URPS_dialog_action_buttons"

            vbox:
                hbox:
                    use URPS_IconButton(icon=yesIcon, text=yesText, action=yesAction, color=yesColor, key="K_y")

                hbox:
                    use URPS_IconButton(icon=noIcon, text=noText, action=noAction, color=noColor, key="K_n")

init python in URPS:
    def showConfirm(title="Confirm", message=None, yes=None, no=None, yesText="Yes", noText="No", yesIcon="\ue876", noIcon="\ue5cd", yesColor=None, noColor=None):
        renpy.show_screen("URPS_Confirm", title, message, yes, no, yesText, noText, yesIcon, noIcon, yesColor, noColor)
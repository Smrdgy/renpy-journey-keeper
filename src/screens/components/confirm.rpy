screen URPS_Confirm(title="Confirm", message=None, yes=None, no=None, yesText="{u}Y{/u}es", noText="{u}N{/u}o", yesIcon=None, noIcon="\ue5cd", yesColor=None, noColor=None):
    layer "URPS_Overlay"
    style_prefix "URPS"

    modal True

    zorder 199

    python:
        yesAction = [yes, Hide("URPS_Confirm")]
        noAction = [no, Hide("URPS_Confirm")]

    key 'K_RETURN' action yesAction
    key 'K_KP_ENTER' action yesAction

    if yesText == "Yes":
        key 'K_y' action yesAction

    if noText == "No":
        key 'K_n' action noAction

    use URPS_Dialog(title=title, message=message, closeAction=noAction):
        hbox:
            xfill True
            yfill True

            style_prefix "URPS_dialog_action_buttons"

            vbox:
                hbox:
                    use URPS_IconButton(icon=yesIcon, text=yesText, action=yesAction, color=yesColor)

                hbox:
                    use URPS_IconButton(icon=noIcon, text=noText, action=noAction, color=noColor)

init python in URPS:
    def showConfirm(title="", message=None, yes=None, no=None, yesText="{u}Y{/u}es", noText="{u}N{/u}o", yesIcon="\ue876", noIcon="\ue5cd", yesColor=None, noColor=None):
        renpy.run(renpy.store.Show("URPS_Confirm", title=title, message=message, yes=yes, no=no, yesText=yesText, noText=noText, yesIcon=yesIcon, noIcon=noIcon, yesColor=yesColor, noColor=noColor))
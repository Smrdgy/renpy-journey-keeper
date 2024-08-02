screen SSSSS_Confirm(title="Confirm", message=None, yes=None, no=None, yesText="{u}Y{/u}es", noText="{u}N{/u}o", yesIcon=None, noIcon="\ue5cd", yesColor=None, noColor=None):
    layer "SSSSSoverlay"
    style_prefix "SSSSS"

    modal True

    zorder 199

    python:
        yesAction = [yes, Hide("SSSSS_Confirm")]
        noAction = [no, Hide("SSSSS_Confirm")]

    key 'K_RETURN' action yesAction
    key 'K_KP_ENTER' action yesAction

    if yesText == "Yes":
        key 'K_y' action yesAction

    if noText == "No":
        key 'K_n' action noAction

    use SSSSS_Dialog(title=title, message=message, closeAction=noAction):
        hbox:
            xfill True
            yfill True

            vbox at right:
                yalign 1.0

                use sssss_iconButton(icon=yesIcon, text=yesText, action=yesAction, color=yesColor)
                use sssss_iconButton(icon=noIcon, text=noText, action=noAction, color=noColor)

init python in SSSSS:
    def showConfirm(title="", message=None, yes=None, no=None, yesText="{u}Y{/u}es", noText="{u}N{/u}o", yesIcon="\ue876", noIcon="\ue5cd", yesColor=None, noColor=None):
        renpy.run(renpy.store.Show("SSSSS_Confirm", title=title, message=message, yes=yes, no=no, yesText=yesText, noText=noText, yesIcon=yesIcon, noIcon=noIcon, yesColor=yesColor, noColor=noColor))
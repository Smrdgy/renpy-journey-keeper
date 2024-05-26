screen SSSSS_Confirm(title="Confirm", message=None, yes=None, no=None, yesText="Yes", noText="No", yesIcon=None, noIcon="\ue5cd", yesColor=None, noColor=None):
    layer "SSSSSoverlay"
    style_prefix "SSSSS"

    modal True

    zorder 199

    use SSSSS_Dialog(title=title, message=message, closeAction=[no, Hide("SSSSS_Confirm")]):
        hbox:
            xfill True
            yfill True

            vbox at right:
                yalign 1.0

                use sssss_iconButton(icon=yesIcon, text=yesText, action=[yes, Hide("SSSSS_Confirm")], color=yesColor)
                use sssss_iconButton(icon=noIcon, text=noText, action=[no, Hide("SSSSS_Confirm")], color=noColor)

init python in SSSSS:
    def showConfirm(title="", message=None, yes=None, no=None, yesText="Yes", noText="No", yesIcon="\ue876", noIcon="\ue5cd", yesColor=None, noColor=None):
        renpy.run(renpy.store.Show("SSSSS_Confirm", title=title, message=message, yes=yes, no=no, yesText=yesText, noText=noText, yesIcon=yesIcon, noIcon=noIcon, yesColor=yesColor, noColor=noColor))
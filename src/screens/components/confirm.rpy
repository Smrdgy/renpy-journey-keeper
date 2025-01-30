screen JK_Confirm(title=None, message=None, yes=None, no=None, yesText=None, noText=None, yesIcon=None, noIcon=None, yesColor=None, noColor=None):
    layer "JK_Overlay"
    style_prefix "JK"

    modal True

    zorder 199

    python:
        yesAction = [yes, Hide("JK_Confirm")]
        noAction = [no, Hide("JK_Confirm")]

    key 'K_RETURN' action yesAction
    key 'K_KP_ENTER' action yesAction

    use JK_Dialog(title=title, message=message, closeAction=noAction):
        hbox:
            xfill True
            yfill True

            style_prefix "JK_dialog_action_buttons"

            vbox:
                hbox:
                    use JK_IconButton(icon=yesIcon, text=yesText, action=yesAction, color=yesColor, key="K_y")

                hbox:
                    use JK_IconButton(icon=noIcon, text=noText, action=noAction, color=noColor, key="K_n")

init python in JK:
    def showConfirm(title="Confirm", message=None, yes=None, no=None, yesText="Yes", noText="No", yesIcon="\ue876", noIcon="\ue5cd", yesColor=None, noColor=None):
        renpy.show_screen("JK_Confirm", title, message, yes, no, yesText, noText, yesIcon, noIcon, yesColor, noColor)
        renpy.restart_interaction()

    class ShowConfirmAction(renpy.ui.Action):
        def __init__(self, title="Confirm", message=None, yes=None, no=None, yesText="Yes", noText="No", yesIcon="\ue876", noIcon="\ue5cd", yesColor=None, noColor=None):
            self.title = title
            self.message = message
            self.yes = yes
            self.no = no
            self.yesText = yesText
            self.noText = noText
            self.yesIcon = yesIcon
            self.noIcon = noIcon
            self.yesColor = yesColor
            self.noColor = noColor

        def __call__(self):
            renpy.show_screen("JK_Confirm", self.title, self.message, self.yes, self.no, self.yesText, self.noText, self.yesIcon, self.noIcon, self.yesColor, self.noColor)
            renpy.restart_interaction()
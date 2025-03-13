screen JK_Confirm(title=None, message=None, yes=None, yes_text=None, yes_icon=None, yes_color=None, no=None, no_text=None, no_icon=None, no_color=None):
    layer "JK_Overlay"
    style_prefix "JK"

    modal True

    zorder 199

    python:
        yesAction = [yes, Hide("JK_Confirm")]
        noAction = [no, Hide("JK_Confirm")]

    key 'K_RETURN' action yesAction
    key 'K_KP_ENTER' action yesAction

    use JK_Dialog(title=title, message=message, close_action=noAction):
        hbox:
            xfill True
            yfill True

            style_prefix "JK_dialog_action_buttons"

            vbox:
                hbox:
                    use JK_IconButton(icon=yes_icon, text=yes_text, action=yesAction, color=yes_color, key="K_y")

                hbox:
                    use JK_IconButton(icon=no_icon, text=no_text, action=noAction, color=no_color, key="K_n")

init python in JK:
    def showConfirm(title="Confirm", message=None, yes=None, no=None, yes_text="Yes", no_text="No", yes_icon="\ue876", no_icon="\ue5cd", yes_color=None, no_color=None):
        renpy.show_screen("JK_Confirm", title=title, message=message, yes=yes, no=no, yes_text=yes_text, no_text=no_text, yes_icon=yes_icon, no_icon=no_icon, yes_color=yes_color, no_color=no_color)
        renpy.restart_interaction()

    class ShowConfirmAction(renpy.ui.Action):
        def __init__(self, title="Confirm", message=None, yes=None, no=None, yes_text="Yes", no_text="No", yes_icon="\ue876", no_icon="\ue5cd", yes_color=None, no_color=None):
            self.title = title
            self.message = message
            self.yes = yes
            self.no = no
            self.yes_text = yes_text
            self.no_text = no_text
            self.yes_icon = yes_icon
            self.no_icon = no_icon
            self.yes_color = yes_color
            self.no_color = no_color

        def __call__(self):
            renpy.show_screen("JK_Confirm", title=self.title, message=self.message, yes=self.yes, no=self.no, yes_text=self.yes_text, no_text=self.no_text, yes_icon=self.yes_icon, no_icon=self.no_icon, yes_color=self.yes_color, no_color=self.no_color)
            renpy.restart_interaction()
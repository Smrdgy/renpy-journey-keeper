screen SSSSS_MoveCopySavesError(viewModel):
    python:
        class ClearErrorAction(renpy.ui.Action):
            def __init__(self, viewModel):
                self.viewModel = viewModel
            
            def __call__(self):
                self.viewModel.error = None
                renpy.restart_interaction()

    vbox:
        xfill True
        yfill True
        ymaximum 0.85

        vbox align (0.5, 0.5):
            hbox xalign 0.5:
                use SSSSS_Title("Error", color="#f00")

            use SSSSS_YSpacer(offset=2)

            hbox xalign 0.5:
                text viewModel.error

    # Dialog footer
    hbox:
        xfill True
        yfill True

        style_prefix "SSSSS_dialog_action_buttons"

        vbox:
            # OK
            hbox:
                use sssss_iconButton(icon="", text="OK", action=ClearErrorAction(viewModel))

            # Close
            hbox:
                use sssss_iconButton(icon="\ue5cd", text="Close", action=Hide("SSSSS_MoveCopySaves"))
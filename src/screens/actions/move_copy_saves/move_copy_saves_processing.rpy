screen SSSSS_MoveCopySavesProcessing(viewModel):
    python:
        processed = viewModel.processed
        to_process = len(viewModel.saves_to_process)

        class StopAction(renpy.ui.Action):
            def __init__(self, viewModel):
                self.viewModel = viewModel

            def __call__(self):
                self.viewModel.process_stop()

    vbox:
        xfill True
        yfill True
        ymaximum 0.85

        vbox align(0.5, 0.5):
            xfill True
            xmaximum 0.85

            hbox xalign 0.5:
                use SSSSS_Title("Copying saves..." if viewModel.stage == "COPY" else "Removing old saves...")

            use SSSSS_YSpacer()

            text "[processed]/[to_process]" xalign 0.5
            bar value processed range to_process

    # Dialog footer
    hbox:
        xfill True
        yfill True

        style_prefix "SSSSS_dialog_action_buttons"

        vbox:
            hbox:
                use sssss_iconButton(icon="\ue99a", text="Stop", action=StopAction(viewModel), color=SSSSS.Colors.danger)

            # Close
            hbox:
                use sssss_iconButton(icon="\ue5cd", text="Close", action=Hide("SSSSS_MoveCopySaves"))
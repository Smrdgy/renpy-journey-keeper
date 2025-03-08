screen JK_SavesListProcessing(view_model):
    style_prefix 'JK'
    modal True

    python:
        processed = view_model.processed
        to_process = len(view_model.selection)

        class StopAction(renpy.ui.Action):
            def __init__(self, view_model):
                self.view_model = view_model

            def __call__(self):
                self.view_model.process_stop()

    vbox:
        xfill True
        yfill True
        ymaximum 0.85

        vbox align(0.5, 0.5):
            xfill True
            xmaximum 0.85

            hbox xalign 0.5:
                use JK_Title("Removing saves...")

            use JK_YSpacer()

            text "[processed]/[to_process]" xalign 0.5
            bar value processed range to_process

    # Dialog footer
    hbox:
        xfill True
        yfill True

        style_prefix "JK_dialog_action_buttons"

        vbox:
            hbox:
                use JK_IconButton(icon="\ue99a", text="Stop", action=StopAction(view_model), color=JK.Colors.danger)

            # Close
            hbox:
                use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_SavesList"))
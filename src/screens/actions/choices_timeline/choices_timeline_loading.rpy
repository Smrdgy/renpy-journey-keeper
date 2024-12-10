screen URPS_ChoicesTimelineLoading(viewModel):
    style_prefix 'URPS'
    modal True

    python:
        loaded = viewModel.loaded
        to_load = viewModel.to_load

        # class StopAction(renpy.ui.Action):
        #     def __init__(self, viewModel):
        #         self.viewModel = viewModel

        #     def __call__(self):
        #         self.viewModel.process_stop()

    vbox:
        xfill True
        yfill True
        ymaximum 0.85

        vbox align(0.5, 0.5):
            xfill True
            xmaximum 0.85

            hbox xalign 0.5:
                use URPS_Title("Reading saves...")

            use URPS_YSpacer()

            text "[loaded]/[to_load]" xalign 0.5
            bar value loaded range to_load

    # Dialog footer
    hbox:
        xfill True
        yfill True

        style_prefix "URPS_dialog_action_buttons"

        vbox:
            # hbox:
            #     use URPS_IconButton(icon="\ue99a", text="Stop", action=StopAction(viewModel), color=URPS.Colors.danger)

            # Close
            hbox:
                use URPS_IconButton(icon="\ue5cd", text="Close", action=Hide("URPS_ChoicesTimeline"))
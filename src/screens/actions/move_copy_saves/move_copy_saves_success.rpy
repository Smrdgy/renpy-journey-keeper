screen SSSSS_MoveCopySavesSuccess(viewModel):
    vbox:
        xfill True
        yfill True
        ymaximum 0.85

        vbox align (0.5, 0.5):
            use SSSSS_Title("Done", color="#0f0")

    # Dialog footer
    hbox:
        xfill True
        yfill True

        style_prefix "SSSSS_dialog_action_buttons"

        vbox:
            # Close
            hbox:
                use sssss_iconButton(icon="", text="OK", action=Hide("SSSSS_MoveCopySaves"))
screen JK_MoveCopySavesSuccess():
    style_prefix 'JK'
    modal True

    vbox:
        xfill True
        yfill True
        ymaximum 0.85

        vbox align (0.5, 0.5):
            use JK_Title("Done", color=JK.Colors.success)

    # Dialog footer
    hbox:
        xfill True
        yfill True

        style_prefix "JK_dialog_action_buttons"

        vbox:
            # Close
            hbox:
                use JK_IconButton(icon="", text="OK", action=Hide("JK_MoveCopySaves"))
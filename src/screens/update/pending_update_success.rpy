screen SSSSS_PendingUpdateSuccess():
    style_prefix 'SSSSS'
    modal True

    vbox:
        xfill True
        yfill True
        ymaximum 0.85

        vbox align (0.5, 0.5):
            use SSSSS_Title("Update installed successfully.", color=SSSSS.Colors.success)
            use SSSSS_InfoBox("Restart the game to see the changes.")

    # Dialog footer
    hbox:
        xfill True
        yfill True

        style_prefix "SSSSS_dialog_action_buttons"

        vbox:
            # Quit game
            hbox:
                use sssss_iconButton(icon="\ue9ba", text="Quit game", action=Quit())

            # Close
            hbox:
                use sssss_iconButton(icon="", text="OK", action=Hide("SSSSS_PendingUpdate"))
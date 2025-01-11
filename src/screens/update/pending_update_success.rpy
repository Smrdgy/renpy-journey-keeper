screen URPS_PendingUpdateSuccess():
    style_prefix 'URPS'
    modal True

    vbox:
        xfill True
        yfill True
        ymaximum 0.85

        vbox align (0.5, 0.5):
            use URPS_Title("Update installed successfully.", color=URPS.Colors.success)
            use URPS_InfoBox("Restart the game to see the changes.")

    # Dialog footer
    hbox:
        xfill True
        yfill True

        style_prefix "URPS_dialog_action_buttons"

        vbox:
            # Restart game
            hbox:
                use URPS_IconButton(icon="\ue9ba", text="Restart the game", action=URPS.Updater.RestartGame())

            # Close
            hbox:
                use URPS_IconButton(icon="", text="OK", action=Hide("URPS_PendingUpdate"))
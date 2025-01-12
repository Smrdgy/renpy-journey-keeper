screen JK_PendingUpdateSuccess():
    style_prefix 'JK'
    modal True

    vbox:
        xfill True
        yfill True
        ymaximum 0.85

        vbox align (0.5, 0.5):
            use JK_Title("Update installed successfully.", color=JK.Colors.success)
            use JK_InfoBox("Restart the game to see the changes.")

    # Dialog footer
    hbox:
        xfill True
        yfill True

        style_prefix "JK_dialog_action_buttons"

        vbox:
            # Restart game
            hbox:
                use JK_IconButton(icon="\ue9ba", text="Restart the game", action=JK.Updater.RestartGame())

            # Close
            hbox:
                use JK_IconButton(icon="", text="OK", action=Hide("JK_PendingUpdate"))
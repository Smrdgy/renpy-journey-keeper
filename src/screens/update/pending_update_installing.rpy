screen URPS_PendingUpdateInstalling():
    style_prefix 'URPS'
    modal True

    vbox:
        xfill True
        yfill True
        ymaximum 0.85

        vbox align (0.5, 0.5):
            use URPS_Title("Downloading...")

    # Dialog footer
    hbox:
        xfill True
        yfill True

        style_prefix "URPS_dialog_action_buttons"

        vbox:
            # Close
            hbox:
                use URPS_IconButton(icon="\ue5cd", text="Close", action=Hide("URPS_PendingUpdate"))
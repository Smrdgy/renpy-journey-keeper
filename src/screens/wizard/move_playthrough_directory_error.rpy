screen URPS_MovePlaythroughDirectoryError(errors=[]):
    layer "URPS_Overlay"
    style_prefix "URPS"
    modal True

    $ errorsLen = len(errors)

    use URPS_Dialog(title="Failed to rename directories", closeAction=Hide("URPS_MovePlaythroughDirectoryError")):
        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            pagekeys True
            ymaximum 0.85

            vbox:
                text "{b}{color=[URPS.Colors.theme]}[errorsLen]{/c}{/b} directory(s) failed to move:"

                use URPS_YSpacer(offset=3)

                for error in errors:
                    python:
                        errorText = ""

                        if error[1] == "LOCATION_EXISTS":
                            errorText = "Directory already exists"
                        else:
                            errorText = error[1]

                    hbox:
                        textbutton error[0]:
                            action SmrdgyLib.path.OpenDirectoryAction(path=error[0])

                        use URPS_IconButton(icon="\ue2c8", action=SmrdgyLib.path.OpenDirectoryAction(path=error[0]))

                        textbutton " - "
                        textbutton errorText:
                            text_color URPS.Colors.error

        hbox:
            xfill True
            yfill True

            style_prefix "URPS_dialog_action_buttons"

            vbox:
                # Close
                hbox:
                    use URPS_IconButton(icon="\ue5cd", text="Close", action=Hide("URPS_MovePlaythroughDirectoryError"))

        

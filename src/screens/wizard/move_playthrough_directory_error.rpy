screen SSSSS_MovePlaythroughDirectoryError(errors=[]):
    layer "SSSSSoverlay"
    style_prefix "SSSSS"
    modal True

    $ errorsLen = len(errors)

    use SSSSS_Dialog(title="Failed to rename directories", closeAction=Hide("SSSSS_MovePlaythroughDirectoryError")):
        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            pagekeys True
            ymaximum 0.85

            vbox:
                text "{b}{color=[SSSSS.Colors.theme]}[errorsLen]{/c}{/b} directory(s) failed to move:"

                use SSSSS_YSpacer(offset=3)

                for error in errors:
                    python:
                        errorText = ""

                        if error[1] == "LOCATION_EXISTS":
                            errorText = "Directory already exists"
                        else:
                            errorText = error[1]

                    hbox:
                        textbutton error[0]:
                            action SSSSS.OpenDirectoryAction(path=error[0])

                        use sssss_iconButton(icon="\ue2c8", action=SSSSS.OpenDirectoryAction(path=error[0]))

                        textbutton " - "
                        textbutton errorText:
                            text_color SSSSS.Colors.error

        hbox:
            xfill True
            yfill True

            style_prefix "SSSSS_dialog_action_buttons"

            vbox:
                # Close
                hbox:
                    use sssss_iconButton(icon="\ue5cd", text="Close", action=Hide("SSSSS_MovePlaythroughDirectoryError"))

        

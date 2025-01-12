screen JK_MovePlaythroughDirectoryError(errors=[]):
    layer "JK_Overlay"
    style_prefix "JK"
    modal True

    $ errorsLen = len(errors)

    use JK_Dialog(title="Failed to rename directories", closeAction=Hide("JK_MovePlaythroughDirectoryError")):
        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            pagekeys True
            ymaximum 0.85

            vbox:
                text "{b}{color=[JK.Colors.theme]}[errorsLen]{/c}{/b} directory(s) failed to move:"

                use JK_YSpacer(offset=3)

                for error in errors:
                    python:
                        errorText = ""

                        if error[1] == "LOCATION_EXISTS":
                            errorText = "Directory already exists"
                        else:
                            errorText = error[1]

                    hbox:
                        textbutton error[0]:
                            action JK.OpenDirectoryAction(path=error[0])

                        use JK_IconButton(icon="\ue2c8", action=JK.OpenDirectoryAction(path=error[0]))

                        textbutton " - "
                        textbutton errorText:
                            text_color JK.Colors.error

        hbox:
            xfill True
            yfill True

            style_prefix "JK_dialog_action_buttons"

            vbox:
                # Close
                hbox:
                    use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_MovePlaythroughDirectoryError"))

        

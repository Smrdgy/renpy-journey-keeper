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

            vbox:
                text "{b}{color=#70bde6}[errorsLen]{/c}{/b} directory(s) failed to move:"

                hbox ysize 10

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
                            text_color "#ff4c4c"

        

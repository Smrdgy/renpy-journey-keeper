screen JK_MovePlaythroughDirectoryError(playthrough, errors=[]):
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
                        button:
                            action JK.OpenDirectoryAction(path=error[0])

                            hbox yalign 0.5:
                                text error[0] yalign 0.5

                                text "  "

                                use JK_Icon(icon="\ue2c8")

                        text " - " + errorText color JK.Colors.error yalign 0.5

        hbox:
            xfill True
            yfill True

            style_prefix "JK_dialog_action_buttons"

            vbox:
                # Overwrite
                hbox:
                    use JK_IconButton(icon="\ue15a", text="Overwrite", action=JK.ShowConfirmAction(title="Overwrite conflicting directories", message="Are you sure? This will delete any data stored in those directories.\n\nThis action {u}{color=[JK.Colors.error]}is irreversible{/c}{/u}.", yes=[Hide("JK_MovePlaythroughDirectoryError"), JK.Playthroughs.ForceRenamePlaythrough(playthrough)], yesColor=JK.Colors.danger), color=JK.Colors.danger, spacing=JK.scaled(5))

                # Close
                hbox:
                    use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_MovePlaythroughDirectoryError"))

        

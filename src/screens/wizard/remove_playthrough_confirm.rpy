screen SSSSS_RemovePlaythroughConfirm(playthrough):
    layer "SSSSSoverlay"
    style_prefix 'SSSSS'
    modal True

    default deleteFiles = False

    $ deleteAction = [SSSSS.Playthroughs.Remove(playthrough.id, deleteFiles), Hide("SSSSS_RemovePlaythroughConfirm"), Hide("SSSSS_EditPlaythrough")]

    key 'K_RETURN' action deleteAction #TODO: Doesn't work not sure why...
    key 'K_KP_ENTER' action deleteAction

    use SSSSS_Dialog(title="Delete playthrough", closeAction=Hide("SSSSS_RemovePlaythroughConfirm")):
        text "Are you sure you want to remove \"[playthrough.name]\"?" xalign .5

        frame:
            background None
            xalign 0.5
            padding (0, 10, 0, 0)

            use SSSSS_Checkbox(checked=deleteFiles, text="Delete files", action=ToggleScreenVariable('deleteFiles', True, False))

        frame:
            background None
            padding (0, 0, 10, 0)
            xalign 0.5

            hbox:
                button:
                    action None
                    use sssss_icon('\ue88e', color = "#8cb8ed")
                hbox xsize 10
                text "If you choose to delete the files, you won't be able to recover the playthrough." yalign .5 color "#8cb8ed"

        python:
            removeText = "Remove & delete files" if deleteFiles else "Remove"

        hbox:
            xfill True
            yfill True

            style_prefix "SSSSS_dialog_action_buttons"

            vbox:
                # Remove
                hbox:
                    use sssss_iconButton(icon="\ue92b", text=removeText, action=deleteAction, color="#ff0000")

                # Close
                hbox:
                    use sssss_iconButton(icon="\ue5cd", text="Close", action=Hide("SSSSS_RemovePlaythroughConfirm"))
screen URPS_RemovePlaythroughConfirm(playthrough):
    layer "URPS_Overlay"
    style_prefix 'URPS'
    modal True

    default deleteFiles = False

    $ deleteAction = [URPS.Playthroughs.Remove(playthrough.id, deleteFiles), Hide("URPS_RemovePlaythroughConfirm"), Hide("URPS_EditPlaythrough")]

    use URPS_Dialog(title="Delete playthrough", closeAction=Hide("URPS_RemovePlaythroughConfirm")):
        key 'K_RETURN' action deleteAction
        key 'K_KP_ENTER' action deleteAction

        text "Are you sure you want to remove \"[playthrough.name]\"?" xalign .5

        frame:
            background None
            xalign 0.5
            padding (0, 10, 0, 0)

            use URPS_Checkbox(checked=deleteFiles, text="Delete files", action=ToggleScreenVariable('deleteFiles', True, False))

        frame:
            background None
            padding (0, 0, 10, 0)
            xalign 0.5

            hbox yalign .5:
                use URPS_InfoBox("If you choose to delete the files, you won't be able to recover the playthrough.")

        python:
            removeText = "Remove & delete files" if deleteFiles else "Remove"

        hbox:
            xfill True
            yfill True

            style_prefix "URPS_dialog_action_buttons"

            vbox:
                # Remove
                hbox:
                    use URPS_IconButton(icon="\ue92b", text=removeText, action=deleteAction, color=URPS.Colors.danger)

                # Close
                hbox:
                    use URPS_IconButton(icon="\ue5cd", text="Close", action=Hide("URPS_RemovePlaythroughConfirm"))
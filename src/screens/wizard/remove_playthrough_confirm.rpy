screen JK_RemovePlaythroughConfirm(playthrough):
    layer "JK_Overlay"
    style_prefix 'JK'
    modal True

    default deleteFiles = False

    $ deleteAction = [JK.Playthroughs.Remove(playthrough.id, deleteFiles), Hide("JK_RemovePlaythroughConfirm"), Hide("JK_EditPlaythrough")]

    use JK_Dialog(title="Delete playthrough", closeAction=Hide("JK_RemovePlaythroughConfirm")):
        key 'K_RETURN' action deleteAction
        key 'K_KP_ENTER' action deleteAction

        text "Are you sure you want to remove \"[playthrough.name]\"?" xalign .5

        frame:
            background None
            xalign 0.5
            padding (0, 10, 0, 0)

            use JK_Checkbox(checked=deleteFiles, text="Delete files", action=ToggleScreenVariable('deleteFiles', True, False))

        frame:
            background None
            padding (0, 0, 10, 0)
            xalign 0.5

            hbox yalign .5:
                use JK_InfoBox("If you choose to delete the files, you won't be able to recover the playthrough.")

        python:
            removeText = "Remove & delete files" if deleteFiles else "Remove"

        hbox:
            xfill True
            yfill True

            style_prefix "JK_dialog_action_buttons"

            vbox:
                # Remove
                hbox:
                    use JK_IconButton(icon="\ue92b", text=removeText, action=deleteAction, color=JK.Colors.danger)

                # Close
                hbox:
                    use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_RemovePlaythroughConfirm"))
screen SSSSS_RemovePlaythroughConfirm(playthrough):
    style_prefix 'SSSSS'
    default deleteFiles = False

    use SSSSS_Dialog(title="Delete playthrough", closeAction=Hide("SSSSS_RemovePlaythroughConfirm"), background="gui/dialog/confirm_dialog_background.png", size=(x52URM.scalePxInt(922), x52URM.scalePxInt(400))):
        style_prefix "SSSSS"

        text "Are you sure you want to remove \"[playthrough.name]\"?" xalign .5

        frame:
            style "SSSSS_frame"
            background None
            xalign 0.5
            padding (0, 10, 0, 0)

            use SSSSS_Checkbox(checked=deleteFiles, text="Delete files", action=ToggleScreenVariable('deleteFiles', True, False))

        frame:
            style "SSSSS_frame"
            background None
            padding (0, 0, 10, 0)
            xalign 0.5

            hbox:
                button:
                    action None
                    use sssss_icon('\ue88e')
                hbox xsize 10
                text "If you choose to delete the files, you won't be able to recover the playthrough." yalign .5

        hbox:
            xfill True

            python:
                removeText = "Remove & delete files" if deleteFiles else "Remove"

            button:
                style "SSSSS_textbutton_medium_red"
                action [SSSSS.Playthroughs.Remove(playthrough.id, deleteFiles), Hide("SSSSS_RemovePlaythroughConfirm"), Hide("SSSSS_EditPlaythrough")]
                key_events True # We need this to still trigger key events defined inside of this button
                xalign 0.5

                text "[removeText]" yalign .5 xalign 0.5 size (20 if deleteFiles else 28)

            button:
                style "SSSSS_textbutton_medium_gray"
                action Hide("SSSSS_RemovePlaythroughConfirm")
                key_events True # We need this to still trigger key events defined inside of this button
                xalign 0.5
                
                text "Close" yalign .5 xalign 0.5 size 28
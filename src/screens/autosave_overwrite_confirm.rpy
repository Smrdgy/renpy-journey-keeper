screen SSSSS_AutosaveOverwriteConfirm():
    default title = "Are you sure you want to overwrite your save?"
    default message = "By choosing \"No\", the autosave feature will disable itself until you re-enable it again."

    use SSSSS_Dialog(title=title, message=message, closeAction=[SSSSS.Autosaver.ConfirmDialogClose(), Hide("SSSSS_AutosaveOverwriteConfirm")], background="gui/edit_playthrough_dialog_background.png", size=(x52URM.scalePxInt(1000), x52URM.scalePxInt(600))):
        vbox:
            yfill True
            xfill True

            vbox:
                align (0.5, 0.5)

                python:
                    page, slot, _ = SSSSS.Autosaver.getCurrentSlot()

                add FileScreenshot(name=slot, page=page) xalign 0.5

                text "[renpy.store.SSSSS_ActiveSlot]" style "SSSSS_text" xalign 0.5

        hbox:
            xfill True
            offset (0, -50)

            button:
                style "SSSSS_textbutton_medium_red"
                key_events True
                xalign 0.5
                action [SSSSS.Autosaver.ConfirmDialogSave(), SSSSS.Autosaver.ConfirmDialogClose(), Hide("SSSSS_AutosaveOverwriteConfirm")]

                text "Overwrite" yalign .5 xalign 0.5 size 28

            button:
                style "SSSSS_textbutton_medium_gray"
                key_events True
                xalign 0.5

                action [SSSSS.Autosaver.MoveOneSlotOver(), Hide("SSSSS_AutosaveOverwriteConfirm"), SSSSS.Autosaver.TrySavePendingSave()]
                
                text "Save one over" yalign .5 xalign 0.5 size 28

            button:
                style "SSSSS_textbutton_medium_gray"
                key_events True
                xalign 0.5

                action [SSSSS.Playthroughs.ToggleAutosaveOnChoicesOnActive(), SSSSS.Autosaver.ConfirmDialogClose(), Hide("SSSSS_AutosaveOverwriteConfirm")]
                
                text "No" yalign .5 xalign 0.5 size 28
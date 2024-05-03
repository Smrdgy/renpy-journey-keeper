screen SSSSS_AutosaveOverwriteConfirm():    
    default title = "Are you sure you want to overwrite your save?"
    default message = "By choosing \"No\", the autosave feature will disable itself until you re-enable it again."

    layer "SSSSSoverlay"
    style_prefix 'SSSSS'

    use SSSSS_Dialog(title=title, message=message, closeAction=[SSSSS.Autosaver.ConfirmDialogClose(), Hide("SSSSS_AutosaveOverwriteConfirm")]):
        vbox:
            xfill True

            python:
                page, slot, _ = SSSSS.Autosaver.getCurrentSlot()

            add FileScreenshot(name=slot, page=page) xalign 0.5

            text "[renpy.store.SSSSS_ActiveSlot]"  xalign 0.5 text_align 0.5
        
        hbox:
            xfill True
            yfill True

            vbox at right:
                yalign 1.0

                # Overwrite
                hbox at right:
                    use sssss_iconButton(icon="\ue161", text="Overwrite", action=[SSSSS.Autosaver.ConfirmDialogSave(), SSSSS.Autosaver.ConfirmDialogClose(), Hide("SSSSS_AutosaveOverwriteConfirm")], textColor="#f00")

                # Move one over
                hbox at right:
                    use sssss_iconButton(icon="\ue941", text="Save one over", action=[SSSSS.Autosaver.MoveOneSlotOver(), Hide("SSSSS_AutosaveOverwriteConfirm"), SSSSS.Autosaver.TrySavePendingSave()])

                # No
                hbox at right:
                    use sssss_iconButton(icon="\ue5cd", text="No", action=[SSSSS.Playthroughs.ToggleAutosaveOnChoicesOnActive(), SSSSS.Autosaver.ConfirmDialogClose(), Hide("SSSSS_AutosaveOverwriteConfirm")])
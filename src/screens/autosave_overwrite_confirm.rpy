screen SSSSS_AutosaveOverwriteConfirm():    
    default title = "Are you sure you want to overwrite your save?"
    default message = "By choosing \"No & disable autosave\", the autosave feature will disabled until you re-enable it again."

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

            style_prefix "SSSSS_dialog_action_buttons"

            vbox:
                # Overwrite
                hbox:
                    use sssss_iconButton(icon="\ue161", text="Overwrite", action=[SSSSS.Autosaver.ConfirmDialogSave(), SSSSS.Autosaver.ConfirmDialogClose(), Hide("SSSSS_AutosaveOverwriteConfirm")], color="#f00")

                # Move one over
                hbox:
                    use sssss_iconButton(icon="\ue3cd", text="Save one over", action=[SSSSS.Autosaver.MoveOneSlotOver(), Hide("SSSSS_AutosaveOverwriteConfirm"), SSSSS.Autosaver.TrySavePendingSave()])

                # Skip once
                hbox:
                    use sssss_iconButton(icon="\ue044", text="Skip this time", action=[SSSSS.Autosaver.ConfirmDialogClose(), Hide("SSSSS_AutosaveOverwriteConfirm")])

                # No
                hbox:
                    use sssss_iconButton(icon="\ue5cd", text="No & disable autosave", action=[SSSSS.Playthroughs.ToggleAutosaveOnChoicesOnActive(), SSSSS.Autosaver.ConfirmDialogClose(), Hide("SSSSS_AutosaveOverwriteConfirm")])
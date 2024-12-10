screen URPS_AutosaveOverwriteConfirm():    
    default title = "Are you sure you want to overwrite your save?"
    default message = "By choosing \"No & disable autosave\", the autosave feature will disabled until you re-enable it again."

    layer "URPS_Overlay"
    style_prefix 'URPS'

    use URPS_Dialog(title=title, message=message, closeAction=[URPS.Autosaver.ConfirmDialogClose(), Hide("URPS_AutosaveOverwriteConfirm")]):
        vbox:
            xfill True

            python:
                page, slot, _ = URPS.Autosaver.getCurrentSlot()

            add FileScreenshot(name=slot, page=page) xalign 0.5

            text "[renpy.store.URPS_ActiveSlot]"  xalign 0.5 text_align 0.5
        
        hbox:
            xfill True
            yfill True

            style_prefix "URPS_dialog_action_buttons"

            vbox:
                # Overwrite
                hbox:
                    use URPS_IconButton(icon="\ue161", text="Overwrite", action=[URPS.Autosaver.ConfirmDialogSave(), URPS.Autosaver.ConfirmDialogClose(), Hide("URPS_AutosaveOverwriteConfirm")], color=URPS.Colors.danger)

                # Move one over
                hbox:
                    use URPS_IconButton(icon="\ue3cd", text="Save one over", action=[URPS.Autosaver.MoveOneSlotOver(), Hide("URPS_AutosaveOverwriteConfirm"), URPS.Autosaver.TrySavePendingSave()])

                # Skip once
                hbox:
                    use URPS_IconButton(icon="\ue044", text="Skip this time", action=[URPS.Autosaver.ConfirmDialogClose(), Hide("URPS_AutosaveOverwriteConfirm")])

                # No
                hbox:
                    use URPS_IconButton(icon="\ue5cd", text="No & disable autosave", action=[URPS.Playthroughs.ToggleAutosaveOnChoicesOnActive(), URPS.Autosaver.ConfirmDialogClose(), Hide("URPS_AutosaveOverwriteConfirm")])
screen JK_AutosaveOverwriteConfirm():    
    default title = "Are you sure you want to overwrite your save?"
    default message = "By choosing \"No & disable autosave\", the autosave feature will disabled until you re-enable it again."

    layer "JK_Overlay"
    style_prefix 'JK'

    use JK_Dialog(title=title, message=message, close_action=[JK.Autosaver.ConfirmDialogCloseAction(), Hide("JK_AutosaveOverwriteConfirm")]):
        vbox:
            xfill True

            python:
                page, slot, _ = JK.Autosaver.get_current_slot()

            add FileScreenshot(name=slot, page=page) xalign 0.5

            text "[renpy.store.JK_ActiveSlot]"  xalign 0.5 text_align 0.5
        
        hbox:
            xfill True
            yfill True

            style_prefix "JK_dialog_action_buttons"

            vbox:
                # Overwrite
                hbox:
                    use JK_IconButton(icon="\ue161", text="Overwrite", action=[JK.Autosaver.ConfirmDialogSaveAction(), JK.Autosaver.ConfirmDialogCloseAction(), Hide("JK_AutosaveOverwriteConfirm")], color=JK.Colors.danger)

                # Move one over
                hbox:
                    use JK_IconButton(icon="\ue3cd", text="Save one over", action=[JK.Autosaver.MoveOneSlotOverAction(), Hide("JK_AutosaveOverwriteConfirm"), JK.Autosaver.TrySavePendingSaveAction()])

                # Skip once
                hbox:
                    use JK_IconButton(icon="\ue044", text="Skip this time", action=[JK.Autosaver.ConfirmDialogCloseAction(), Hide("JK_AutosaveOverwriteConfirm")])

                # No
                hbox:
                    use JK_IconButton(icon="\ue5cd", text="No & disable autosave", action=[JK.Playthroughs.ToggleAutosaveOnChoicesForActiveAction(), JK.Autosaver.ConfirmDialogCloseAction(), Hide("JK_AutosaveOverwriteConfirm")])
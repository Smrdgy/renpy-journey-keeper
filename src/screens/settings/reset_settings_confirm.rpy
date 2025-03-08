screen JK_ResetSettingsConfirm():
    layer "JK_Overlay"
    style_prefix 'JK'
    modal True

    default include_global = False

    use JK_Dialog(title="Reset settings", close_action=Hide("JK_ResetSettingsConfirm")):
        style_prefix "JK"

        vbox xalign 0.5 yalign 0.5:
            if include_global:
                text "Do you really wish to reset all settings, including global, into their default configuration?"
            else:
                text "Do you really wish to reset all local settings into their default configuration?"

            use JK_YSpacer(offset=2)

            hbox xalign 0.5:
                use JK_Checkbox(checked=include_global, text="Include global settings", action=ToggleScreenVariable('include_global', True, False))

        hbox:
            xfill True
            yfill True

            style_prefix "JK_dialog_action_buttons"

            vbox:
                # Reset
                hbox:
                    use JK_IconButton(icon="\ue8ba", text="Reset all" if include_global else "Perform reset", action=[JK.Settings.ResetAction(include_global), Hide("JK_ResetSettingsConfirm")], color=JK.Colors.danger)

                # Close
                hbox:
                    use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_ResetSettingsConfirm"))
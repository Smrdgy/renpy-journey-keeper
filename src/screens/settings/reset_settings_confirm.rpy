screen SSSSS_ResetSettingsConfirm():
    layer "SSSSSoverlay"
    style_prefix 'SSSSS'
    modal True

    default include_global = False

    use SSSSS_Dialog(title="Reset settings", closeAction=Hide("SSSSS_Settings")):
        style_prefix "SSSSS"

        vbox xalign 0.5 yalign 0.5:
            if include_global:
                text "Do you really wish to reset all settings, including global, into their default configuration?"
            else:
                text "Do you really wish to reset all local settings into their default configuration?"

            use SSSSS_YSpacer(offset=2)

            hbox xalign 0.5:
                use SSSSS_Checkbox(checked=include_global, text="Include global settings", action=ToggleScreenVariable('include_global', True, False))

        hbox:
            xfill True
            yfill True

            style_prefix "SSSSS_dialog_action_buttons"

            vbox:
                # Reset
                hbox:
                    use sssss_iconButton(icon="\ue8ba", text="Reset all" if include_global else "Reset", action=[SSSSS.Settings.Reset(include_global), Hide("SSSSS_ResetSettingsConfirm")], color=SSSSS.Colors.danger)

                # Close
                hbox:
                    use sssss_iconButton(icon="\ue5cd", text="Close", action=Hide("SSSSS_ResetSettingsConfirm"))
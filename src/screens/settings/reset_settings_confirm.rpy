screen URPS_ResetSettingsConfirm():
    layer "URPS_Overlay"
    style_prefix 'URPS'
    modal True

    default include_global = False

    use URPS_Dialog(title="Reset settings", closeAction=Hide("URPS_Settings")):
        style_prefix "URPS"

        vbox xalign 0.5 yalign 0.5:
            if include_global:
                text "Do you really wish to reset all settings, including global, into their default configuration?"
            else:
                text "Do you really wish to reset all local settings into their default configuration?"

            use URPS_YSpacer(offset=2)

            hbox xalign 0.5:
                use SmrdgyLib_Checkbox(checked=include_global, text="Include global settings", action=ToggleScreenVariable('include_global', True, False))

        hbox:
            xfill True
            yfill True

            style_prefix "URPS_dialog_action_buttons"

            vbox:
                # Reset
                hbox:
                    use URPS_IconButton(icon="\ue8ba", text="Reset all" if include_global else "Reset", action=[URPS.Settings.Reset(include_global), Hide("URPS_ResetSettingsConfirm")], color=URPS.Colors.danger)

                # Close
                hbox:
                    use URPS_IconButton(icon="\ue5cd", text="Close", action=Hide("URPS_ResetSettingsConfirm"))
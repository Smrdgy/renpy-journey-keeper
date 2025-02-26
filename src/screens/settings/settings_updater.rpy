screen JK_Settings_Updater():
    vbox:
        hbox:
            text "These settings are always global." color JK.Colors.status_enabled_disabled yalign 0.5

            use JK_ToggleSettingGlobalizationButton("", disabled=True, force_enabled=True)

        use JK_YSpacer()

        hbox:
            hbox yalign 0.5:
                if JK.Updater.latest:
                    text "Latest version: {a=[JK.Updater.latest_html_url]}[JK.Updater.latest_version]"
                elif JK.Updater.loading:
                    text "Latest version: {color=[JK.Colors.info]}Loading...{/color}"
                else:
                    text "Latest version: {color=[JK.Colors.na]}N/A{/color}"

            use JK_IconButton("\ue5d5", text="Refresh", action=JK.Updater.CheckForUpdateAction())

        use JK_Checkbox(checked=JK.Settings.updaterEnabled, text="Check for an update every time the game launches", action=JK.Settings.ToggleEnabled("updaterEnabled"))

        if JK.Settings.updaterEnabled:
            hbox:
                use JK_XSpacer()

                vbox:
                    use JK_Checkbox(checked=JK.Settings.autoUpdateWithoutPrompt, text="Perform automatic update without prompting", action=JK.Settings.ToggleEnabled("autoUpdateWithoutPrompt"))
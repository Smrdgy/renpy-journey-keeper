screen JK_Settings_Updater():
    default releases_view_model = JK.ReleasesViewModel()
    
    vbox:
        hbox:
            text "These settings are always global." color JK.Colors.status_enabled_disabled yalign 0.5

            use JK_ToggleSettingGlobalizationButton("", disabled=True, force_enabled=True)

        use JK_YSpacer()

        hbox:
            hbox yalign 0.5:
                python:
                    if JK.Updater.latest:
                        state = "{a=[JK.Updater.latest.url]}[JK.Updater.latest.version]"
                    elif JK.Updater.loading:
                        state = "{color=[JK.Colors.info]}Loading...{/color}"
                    else:
                        state = "{color=[JK.Colors.na]}N/A{/color}"

                text "Latest version: {}".format(state)

                if JK.Updater.latest and JK.Updater.latest.version == JK.MOD_VERSION:
                    text "{size=-5} (You have the latest version.){/size}" color JK.Colors.success yalign 0.5

            use JK_IconButton("\ue5d5", text="Refresh", action=JK.Updater.CheckForUpdateAction())

            if not JK.Updater.installed and JK.Updater.latest and JK.Updater.latest.version:
                use JK_IconButton(icon="\ue8d7", text="Download & install {}".format(JK.Updater.latest.version), action=JK.Updater.InstallUpdateAction(JK.Updater.latest))

        if JK.Updater.installed:
            hbox:
                button yalign 0.5:
                    action NullAction()
                    use JK_Icon("\uf05a", size=JK.scaled(20), color=JK.Colors.warning)

                text "You have a pending update ready to be applied." color JK.Colors.warning yalign 0.5

                use JK_IconButton(text="Click here to reload the game", action=JK.Updater.RestartGameAction())
        elif JK.Updater.error:
            text JK.Updater.error color JK.Colors.error

        use JK_Checkbox(checked=JK.Settings.updaterEnabled, text="Check for an update every time the game launches", action=JK.Settings.ToggleEnabledAction("updaterEnabled"))

        hbox:
            use JK_XSpacer()

            vbox:
                use JK_Checkbox(checked=JK.Settings.noUpdatePrompt, text="Don't show update prompt", action=JK.Settings.ToggleEnabledAction("noUpdatePrompt"), disabled=not JK.Settings.updaterEnabled)

                hbox:
                    use JK_XSpacer()

                    vbox:
                        use JK_Checkbox(checked=JK.Settings.autoUpdateWithoutPrompt, text="Automatically install the update", action=JK.Settings.ToggleEnabledAction("autoUpdateWithoutPrompt"), disabled=not JK.Settings.noUpdatePrompt)

        use JK_Title("Changelog")

        if releases_view_model.releases:
            for release in releases_view_model.releases:
                vbox:
                    hbox:
                        use JK_Title(release.version, 2, color=JK.Colors.warning)

                        hbox yalign 0.5:
                            use JK_IconButton(icon="\ue895", action=OpenURL(release.url), tt="Open in browser", size=JK.scaled(20))
                            $ confirm_action = JK.ShowConfirmAction(title="Install {{color=[JK.Colors.theme]}}{}{{/color}}?".format(release.version), message="{color=[JK.Colors.warning]}Caution! Using older versions may cause crashes, corrupt your playthroughs, or reset your settings.{/color}", yes=JK.Updater.InstallUpdateAction(release), yes_text="Download and install", yes_icon="\uf090", yes_color=JK.Colors.danger)
                            use JK_IconButton(icon="\uf090", action=confirm_action, tt="Download and install {}".format(release.version), size=JK.scaled(20))

                    if release.changelog:
                        text release.changelog
                    else:
                        text "(No description)" color JK.Colors.na

                    use JK_YSpacer(2)
        else:
            use JK_IconButton(icon="\uf090", text="Loading..." if releases_view_model.loading else "Load releases", action=JK.Call(releases_view_model.fetch_all_releases))
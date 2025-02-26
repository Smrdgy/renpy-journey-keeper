screen JK_Settings_QuickSave():
    vbox:
        hbox:
            use JK_Checkbox(checked=JK.Settings.quickSaveEnabled, text="Enabled", action=JK.Settings.ToggleEnabled("quickSaveEnabled"))
            use JK_ToggleSettingGlobalizationButton("quickSaveEnabled")

        if JK.Settings.quickSaveEnabled:
            hbox:
                use JK_XSpacer()

                vbox:
                    hbox:
                        use JK_Checkbox(checked=JK.Settings.quickSaveNotificationEnabled, text="Show notification when quick save is performed", action=JK.Settings.ToggleEnabled("quickSaveNotificationEnabled"), disabled=not JK.Settings.quickSaveEnabled)
                        use JK_ToggleSettingGlobalizationButton("quickSaveNotificationEnabled")

                    hbox:
                        use JK_Checkbox(checked=JK.Settings.pageFollowsQuickSave, text="Change page based on the quick-saved slot", action=JK.Settings.ToggleEnabled("pageFollowsQuickSave"))
                        use JK_ToggleSettingGlobalizationButton("pageFollowsQuickSave")

                    use JK_YSpacer(2)

                    hbox:
                        text "Perform quick save key" yalign 0.5
                        use JK_ToggleSettingGlobalizationButton("quickSaveKey")

                    use JK_KeyInput(assignment=JK.Settings.quickSaveKey, action=JK.Settings.SetQuickSaveKey, disabled=not JK.Settings.quickSaveEnabled)
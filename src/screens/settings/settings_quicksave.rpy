screen JK_Settings_QuickSave():
    vbox:
        hbox:
            use JK_Checkbox(checked=JK.Settings.quickSaveEnabled, text="Enabled", action=JK.Settings.ToggleEnabledAction("quickSaveEnabled"))
            use JK_ToggleSettingGlobalizationButton("quickSaveEnabled")

        hbox:
            use JK_XSpacer()

            vbox:
                hbox:
                    use JK_Checkbox(checked=JK.Settings.quickSaveNotificationEnabled, text="Show notification when quick save is performed", action=JK.Settings.ToggleEnabledAction("quickSaveNotificationEnabled"), disabled=not JK.Settings.quickSaveEnabled)
                    use JK_ToggleSettingGlobalizationButton("quickSaveNotificationEnabled", disabled=not JK.Settings.quickSaveEnabled)

                hbox:
                    use JK_Checkbox(checked=JK.Settings.offsetSlotAfterQuickSave, text="Offset slot after quick save", action=JK.Settings.ToggleEnabledAction("offsetSlotAfterQuickSave"), disabled=not JK.Settings.quickSaveEnabled)
                    use JK_Helper("If enabled, creating a quick save will shift the save slot by 1, preventing the next autosave or quicksave from overwriting it.", disabled=not JK.Settings.quickSaveEnabled)
                    use JK_ToggleSettingGlobalizationButton("offsetSlotAfterQuickSave", disabled=not JK.Settings.quickSaveEnabled)

                hbox:
                    use JK_Checkbox(checked=JK.Settings.pageFollowsQuickSave, text="Change page based on the quick-saved slot", action=JK.Settings.ToggleEnabledAction("pageFollowsQuickSave"), disabled=not JK.Settings.quickSaveEnabled)
                    use JK_ToggleSettingGlobalizationButton("pageFollowsQuickSave", disabled=not JK.Settings.quickSaveEnabled)

                use JK_YSpacer(2)

                hbox:
                    text "Perform quick save key" yalign 0.5:
                        if not JK.Settings.quickSaveEnabled:
                            color JK.Colors.disabled
                    use JK_ToggleSettingGlobalizationButton("quickSaveKey", disabled=not JK.Settings.quickSaveEnabled)

                use JK_KeyInput(assignment=JK.Settings.quickSaveKey, action=JK.Settings.get_set_key_action("quickSaveKey"), disabled=not JK.Settings.quickSaveEnabled)
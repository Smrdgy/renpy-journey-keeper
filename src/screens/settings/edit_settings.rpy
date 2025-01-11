screen URPS_Settings():
    layer "URPS_Overlay"
    style_prefix 'URPS'
    modal True

    default originalSizeAdjustment = URPS.Settings.sizeAdjustment

    use URPS_Dialog(title="Settings", closeAction=Hide("URPS_Settings")):
        style_prefix "URPS"

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            pagekeys True
            ymaximum 0.85

            vbox:
                # Accessibility
                vbox:
                    use URPS_Title("Accessibility")
                    vbox:
                        use URPS_Title("Size adjustment", 2)

                        hbox:
                            hbox:
                                yalign 0.0

                                use URPS_IconButton(icon="\ue15b", action=URPS.Settings.DecrementSizeAdjustment())

                                hbox xminimum 40 yalign 0.5:
                                    text ("+" if URPS.Settings.sizeAdjustment > 0 else "") + str(URPS.Settings.sizeAdjustment) xalign 0.5

                                use URPS_IconButton(icon="\ue145", action=URPS.Settings.IncrementSizeAdjustment())

                                use URPS_IconButton(icon="\ue8ba", action=URPS.Settings.ResetSizeAdjustment(), color=URPS.Colors.reset, disabled=URPS.Settings.sizeAdjustment == 0)

                                use URPS_XSpacer()

                            hbox:
                                text "T" size 30 yalign 1.0

                                hbox xsize 5

                                text "T" size URPS.adjustable(30) yalign 1.0

                    if originalSizeAdjustment != URPS.Settings.sizeAdjustment:
                        use URPS_InfoBox("If anything goes wrong, you can revert the value via confirm dialog / waiting for 60 seconds / manually, by simultaneously pressing {b}CTRL + SHIFT + ALT + P{/b}.")

                        use URPS_IconButton(icon="\ue86c", text="Click here to apply the new size\n{size=-7}{color=[URPS.Colors.warning]}This will rebuild all the styles of the game, so don't be scared if it takes a few seconds.{/color}{/size}", action=[URPS.Settings.ApplySizeAdjustment(), SetScreenVariable("originalSizeAdjustment", URPS.Settings.sizeAdjustment)])

                use URPS_YSpacer()

                # Autosave
                vbox:
                    use URPS_Title("Autosave")
                    vbox:
                        hbox:
                            use URPS_Checkbox(checked=URPS.Settings.autosaveNotificationEnabled, text="Show notification when autosave is performed", action=URPS.Settings.ToggleAutosaveNotificationEnabled())
                            use URPS_ToggleSettingGlobalizationButton("autosaveNotificationEnabled")

                        hbox:
                            use URPS_Checkbox(checked=URPS.Settings.pageFollowsAutoSave, text="Change page based on the auto-saved slot", action=URPS.Settings.TogglePageFollowsAutoSaveEnabled())
                            use URPS_ToggleSettingGlobalizationButton("pageFollowsAutoSave")
                        
                        hbox:
                            use URPS_Checkbox(checked=URPS.Settings.autosaveOnSingletonChoice, text="Perform autosave even when only one choice is available.", action=URPS.Settings.ToggleAutosaveOnSingletonChoiceEnabled())
                            use URPS_Helper("When enabled, an autosave will be created even when there is only one choice is displayed.")
                            use URPS_ToggleSettingGlobalizationButton("autosaveOnSingletonChoice")

                        use URPS_YSpacer(2)

                        hbox:
                            text "Toggle autosave key" yalign 0.5
                            use URPS_ToggleSettingGlobalizationButton("autosaveKey")
                        use URPS_KeyInput(assignment=URPS.Settings.autosaveKey, action=URPS.Settings.SetAutosaveToggleKey)

                        use URPS_YSpacer(2)

                        use URPS_Title("Advanced", size=3, color=URPS.Colors.warning)

                        hbox:
                            use URPS_Checkbox(checked=URPS.Settings.preventAutosavingWhileNotInGame, text="Restict autosave to in-game only", action=URPS.Settings.TogglePreventAutosavingWhileNotInGameEnabled())
                            use URPS_Helper("Some games might not properly indicate when the game starts, which could prevent autosave on choices from working. Disabling this setting {b}may{/b} allow autosave to function as intended.\n\nFor technically apt users: The mod waits for the {u}start{/u} label to allow autosaving to function.\n\n{color=[URPS.Colors.warning]}Warning! Disabling this might cause save(s) loss. For example, an 18+ age check might overwrite the 1-1 save slot, if it shows up before the main menu.{/color}")

                use URPS_YSpacer()

                # Quick save
                vbox:
                    use URPS_Title("Quick save")
                    vbox:
                        hbox:
                            use URPS_Checkbox(checked=URPS.Settings.quickSaveEnabled, text="Enabled", action=URPS.Settings.ToggleQuickSaveEnabled())
                            use URPS_ToggleSettingGlobalizationButton("quickSaveEnabled")

                        if URPS.Settings.quickSaveEnabled:
                            hbox:
                                use URPS_XSpacer()

                                vbox:
                                    hbox:
                                        use URPS_Checkbox(checked=URPS.Settings.quickSaveNotificationEnabled, text="Show notification when quick save is performed", action=URPS.Settings.ToggleQuickSaveNotificationEnabled(), disabled=not URPS.Settings.quickSaveEnabled)
                                        use URPS_ToggleSettingGlobalizationButton("quickSaveNotificationEnabled")

                                    hbox:
                                        use URPS_Checkbox(checked=URPS.Settings.pageFollowsQuickSave, text="Change page based on the quick-saved slot", action=URPS.Settings.TogglePageFollowsQuickSaveEnabled())
                                        use URPS_ToggleSettingGlobalizationButton("pageFollowsQuickSave")

                                    use URPS_YSpacer(2)

                                    hbox:
                                        text "Perform quick save key" yalign 0.5
                                        use URPS_ToggleSettingGlobalizationButton("quickSaveKey")

                                    use URPS_KeyInput(assignment=URPS.Settings.quickSaveKey, action=URPS.Settings.SetQuickSaveKey, disabled=not URPS.Settings.quickSaveEnabled)

                use URPS_YSpacer()

                # Sidepanel
                vbox:
                    use URPS_Title("Sidepanel")
                    vbox:
                        hbox:
                            text "Toggle visibility mode key" yalign 0.5
                            use URPS_ToggleSettingGlobalizationButton("changeSidepanelVisibilityKey")

                        use URPS_KeyInput(assignment=URPS.Settings.changeSidepanelVisibilityKey, action=URPS.Settings.SetChangeSidepanelVisibilityKey)

                use URPS_YSpacer()

                # Memories
                vbox:
                    use URPS_Title("Memories")
                    vbox:
                        use URPS_Checkbox(checked=URPS.Settings.memoriesEnabled, text="Enabled", action=URPS.Settings.ToggleMemoriesEnabled())

                        if URPS.Settings.memoriesEnabled:
                            use URPS_YSpacer(2)

                            hbox:
                                use URPS_XSpacer()

                                vbox:
                                    hbox:
                                        text "Create memory key" yalign 0.5
                                        use URPS_ToggleSettingGlobalizationButton("memoriesKey")

                                    use URPS_KeyInput(assignment=URPS.Settings.memoriesKey, action=URPS.Settings.SetCreateMemoryKey, disabled=not URPS.Settings.memoriesEnabled)

                use URPS_YSpacer()

                # Save/Load
                vbox:
                    use URPS_Title("Save/Load")
                    vbox:
                        hbox:
                            use URPS_Checkbox(checked=URPS.Settings.customGridEnabled, text="Custom slots grid", action=URPS.Settings.ToggleCustomGridEnabled())
                            use URPS_Helper("When enabled, two new options will appear where you can enter the number of columns and rows for the save slots in the game's save/load menu. This is needed because some games use custom save systems that the mod's autosave/quicksave system can't handle automatically.")

                        if URPS.Settings.customGridEnabled:
                            use URPS_YSpacer(2)

                            hbox:
                                use URPS_XSpacer()

                                hbox:
                                    vbox:
                                        text "Columns" xalign 0.5
                                        hbox:
                                            use URPS_IconButton(icon="\ue15b", action=URPS.Settings.DecrementCustomGridX())

                                            text str(URPS.Settings.customGridX) yalign 0.5

                                            use URPS_IconButton(icon="\ue145", action=URPS.Settings.IncrementCustomGridX())

                                    use URPS_XSpacer(2)

                                    vbox:
                                        text "Rows" xalign 0.5
                                        hbox:
                                            use URPS_IconButton(icon="\ue15b", action=URPS.Settings.DecrementCustomGridY())

                                            text str(URPS.Settings.customGridY) yalign 0.5

                                            use URPS_IconButton(icon="\ue145", action=URPS.Settings.IncrementCustomGridY())

                                grid URPS.Settings.customGridX URPS.Settings.customGridY spacing URPS.adjustable(5, minValue=1) offset (100, 0) yalign 0.5:
                                    for x in range(0, URPS.Settings.customGridX):
                                        for y in range(0, URPS.Settings.customGridY):
                                            frame style "URPS_default" xysize (10, 10) background URPS.Colors.theme

                            use URPS_YSpacer(2)

                        hbox:
                            use URPS_Checkbox(checked=URPS.Settings.offsetSlotAfterManualSaveIsLoaded, text="Always offset the slot after loading a manual save", action=URPS.Settings.ToggleOffsetSlotAfterManualSaveIsLoadedEnabled())
                            use URPS_Helper("If enabled, loading a save will shift the save slot by 1, ensuring the next autosave or quicksave does not overwrite the manual save.")
                            use URPS_ToggleSettingGlobalizationButton("offsetSlotAfterManualSaveIsLoaded")

                        hbox:
                            use URPS_Checkbox(checked=URPS.Settings.offsetSlotAfterManualSave, text="Offset the slot after a manual save is performed", action=URPS.Settings.ToggleOffsetSlotAfterManualSaveEnabled())
                            use URPS_Helper("If enabled, creating a manual save will shift the save slot by 1, preventing the next autosave or quicksave from overwriting it.")
                            use URPS_ToggleSettingGlobalizationButton("offsetSlotAfterManualSave")

                        use URPS_YSpacer(2)

                        hbox:
                            use URPS_XSpacer()

                            vbox:
                                use URPS_Title("Screens", 2)
                                
                                hbox:
                                    use URPS_XSpacer()

                                    vbox:
                                        use URPS_SettingsLoadSaveScreens()

                                        hbox:
                                            use URPS_IconButton("\ue8fb", text="Detach from settings", action=[Show("URPS_SettingsLoadSaveScreensStandalone"), URPS.SetSidepanelVisibilityAction(None), Hide("URPS_Settings")])
                                            use URPS_Helper("Click to isolate the 'Screens' section, hiding other settings for a focused view. Monitor real-time updates on currently displayed screens to easily choose the correct screen names, with immediate visual feedback on changes.")

                # Updates
                if not URPS.Updater.unavailable:
                    use URPS_YSpacer()

                    vbox:
                        hbox:
                            use URPS_Title("Updates")

                            use URPS_ToggleSettingGlobalizationButton("updaterEnabled", disabled=True, force_enabled=True)

                        vbox:
                            hbox:
                                hbox yalign 0.5:
                                    if URPS.Updater.latest:
                                        text "Latest version: {a=[URPS.Updater.latest_html_url]}[URPS.Updater.latest_version]"
                                    elif URPS.Updater.loading:
                                        text "Latest version: {color=[URPS.Colors.info]}Loading...{/color}"
                                    else:
                                        text "Latest version: {color=[URPS.Colors.na]}N/A{/color}"

                                use URPS_IconButton("\ue5d5", text="Refresh", action=URPS.Updater.CheckForUpdateAction())

                            use URPS_Checkbox(checked=URPS.Settings.updaterEnabled, text="Check for an update every time the game launches", action=URPS.Settings.ToggleUpdaterEnabled())

                            if URPS.Settings.updaterEnabled:
                                hbox:
                                    use URPS_XSpacer()

                                    vbox:
                                        use URPS_Checkbox(checked=URPS.Settings.autoUpdateWithoutPrompt, text="Perform automatic update without prompting", action=URPS.Settings.ToggleAutoUpdatesWithoutPromptEnabled())

                if renpy.config.developer:
                    use URPS_YSpacer()

                    vbox:
                        use URPS_Title("Debug", color=URPS.Colors.danger)
                        vbox:
                            use URPS_Checkbox(checked=URPS.Settings.debugEnabled, text="Debug mode", action=URPS.Settings.ToggleDebugEnabled())

                use URPS_YSpacer()

                hbox:
                    xfill True

                    vbox xalign 0.5:
                        hbox xalign 0.5:
                            use URPS_Title(URPS.MOD_NAME + " v" + URPS.MOD_VERSION)
                        text "{a=https://github.com/[URPS.MOD_GITHUB_OWNER]/[URPS.MOD_GITHUB_REPO]}Click here to open the GitHub page.{/a}" xalign 0.5
                        text "{a=https://github.com/[URPS.MOD_GITHUB_OWNER]/[URPS.MOD_GITHUB_REPO]/issues}Click here to view and/or submit issue(s).{/a}" xalign 0.5

        hbox:
            xfill True
            yfill True

            style_prefix "URPS_dialog_action_buttons"

            vbox:
                # Reset
                hbox:
                    use URPS_IconButton(icon="\ue8ba", text="Reset", action=Show("URPS_ResetSettingsConfirm"), color=URPS.Colors.danger)

                # Close
                hbox:
                    use URPS_IconButton(icon="\ue5cd", text="Close", action=Hide("URPS_Settings"))
    
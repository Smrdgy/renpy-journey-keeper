screen SSSSS_Settings():
    layer "SSSSSoverlay"
    style_prefix 'SSSSS'
    modal True

    default originalSizeAdjustment = SSSSS.Settings.sizeAdjustment

    use SSSSS_Dialog(title="Settings", closeAction=Hide("SSSSS_Settings")):
        style_prefix "SSSSS"

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            pagekeys True
            ymaximum 0.85

            vbox:
                # Accessibility
                vbox:
                    use SSSSS_Title("Accessibility")
                    vbox:
                        use SSSSS_Title("Size adjustment {size=-15}{color=#f00}(EXPERIMENTAL!){/c}{/size}", 2)

                        hbox:
                            hbox:
                                yalign 0.0

                                use sssss_iconButton(icon="\ue15b", action=SSSSS.Settings.DecrementSizeAdjustment())

                                hbox xminimum 40 yalign 0.5:
                                    text ("+" if SSSSS.Settings.sizeAdjustment > 0 else "") + str(SSSSS.Settings.sizeAdjustment) xalign 0.5

                                use sssss_iconButton(icon="\ue145", action=SSSSS.Settings.IncrementSizeAdjustment())

                                use sssss_iconButton(icon="\ue8ba", action=SSSSS.Settings.ResetSizeAdjustment(), color=SSSSS.Colors.reset, disabled=SSSSS.Settings.sizeAdjustment == 0)

                                use SSSSS_XSpacer()

                            hbox:
                                text "T" size 30 yalign 1.0

                                hbox xsize 5

                                text "T" size adjustable(30) yalign 1.0

                    if originalSizeAdjustment != SSSSS.Settings.sizeAdjustment:
                        text "To properly display all changes of this value, a restart of the game is required." color SSSSS.Colors.warning
                        use SSSSS_InfoBox("If anything goes wrong, you can revert the value via confirm dialog, waiting 60 seconds, or manually, by simultaneously holding {u}CTRL + SHIFT + ALT + P{/u}.")

                use SSSSS_YSpacer()

                # Autosave
                vbox:
                    use SSSSS_Title("Autosave")
                    vbox:
                        hbox:
                            use SSSSS_Checkbox(checked=SSSSS.Settings.autosaveNotificationEnabled, text="Show notification when autosave is performed", action=SSSSS.Settings.ToggleAutosaveNotificationEnabled())
                            use SSSSS_ToggleSettingGlobalizationButton("autosaveNotificationEnabled")

                        hbox:
                            use SSSSS_Checkbox(checked=SSSSS.Settings.pageFollowsAutoSave, text="Change page based on the auto-saved slot", action=SSSSS.Settings.TogglePageFollowsAutoSaveEnabled())
                            use SSSSS_ToggleSettingGlobalizationButton("pageFollowsAutoSave")
                        
                        use SSSSS_YSpacer(2)

                        hbox:
                            text "Toggle autosave key" yalign 0.5
                            use SSSSS_ToggleSettingGlobalizationButton("autosaveKey")
                        use SSSSS_KeyInput(assignment=SSSSS.Settings.autosaveKey, action=SSSSS.Settings.SetAutosaveToggleKey)

                use SSSSS_YSpacer()

                # Quick save
                vbox:
                    use SSSSS_Title("Quick save")
                    vbox:
                        hbox:
                            use SSSSS_Checkbox(checked=SSSSS.Settings.quickSaveEnabled, text="Enabled", action=SSSSS.Settings.ToggleQuickSaveEnabled())
                            use SSSSS_ToggleSettingGlobalizationButton("quickSaveEnabled")

                        if SSSSS.Settings.quickSaveEnabled:
                            hbox:
                                use SSSSS_XSpacer()

                                vbox:
                                    hbox:
                                        use SSSSS_Checkbox(checked=SSSSS.Settings.quickSaveNotificationEnabled, text="Show notification when quick save is performed", action=SSSSS.Settings.ToggleQuickSaveNotificationEnabled(), disabled=not SSSSS.Settings.quickSaveEnabled)
                                        use SSSSS_ToggleSettingGlobalizationButton("quickSaveNotificationEnabled")

                                    hbox:
                                        use SSSSS_Checkbox(checked=SSSSS.Settings.pageFollowsQuickSave, text="Change page based on the quick-saved slot", action=SSSSS.Settings.TogglePageFollowsQuickSaveEnabled())
                                        use SSSSS_ToggleSettingGlobalizationButton("pageFollowsQuickSave")

                                    use SSSSS_YSpacer(2)

                                    hbox:
                                        text "Perform quick save key" yalign 0.5
                                        use SSSSS_ToggleSettingGlobalizationButton("quickSaveKey")

                                    use SSSSS_KeyInput(assignment=SSSSS.Settings.quickSaveKey, action=SSSSS.Settings.SetQuickSaveKey, disabled=not SSSSS.Settings.quickSaveEnabled)

                use SSSSS_YSpacer()

                # Sidepanel
                vbox:
                    use SSSSS_Title("Sidepanel")
                    vbox:
                        hbox:
                            text "Toggle visibility mode key" yalign 0.5
                            use SSSSS_ToggleSettingGlobalizationButton("changeSidepanelVisibilityKey")

                        use SSSSS_KeyInput(assignment=SSSSS.Settings.changeSidepanelVisibilityKey, action=SSSSS.Settings.SetChangeSidepanelVisibilityKey)

                use SSSSS_YSpacer()

                # Memories
                vbox:
                    use SSSSS_Title("Memories")
                    vbox:
                        use SSSSS_Checkbox(checked=SSSSS.Settings.memoriesEnabled, text="Enabled", action=SSSSS.Settings.ToggleMemoriesEnabled())

                        if SSSSS.Settings.memoriesEnabled:
                            use SSSSS_YSpacer(2)

                            hbox:
                                use SSSSS_XSpacer()

                                vbox:
                                    hbox:
                                        text "Create memory key" yalign 0.5
                                        use SSSSS_ToggleSettingGlobalizationButton("memoriesKey")

                                    use SSSSS_KeyInput(assignment=SSSSS.Settings.memoriesKey, action=SSSSS.Settings.SetCreateMemoryKey, disabled=not SSSSS.Settings.memoriesEnabled)

                use SSSSS_YSpacer()

                # Save/Load
                vbox:
                    use SSSSS_Title("Save/Load")
                    vbox:
                        hbox:
                            use SSSSS_Checkbox(checked=SSSSS.Settings.customGridEnabled, text="Custom slots grid", action=SSSSS.Settings.ToggleCustomGridEnabled())
                            use SSSSS_Helper("When enabled, two new options will appear where you can enter the number of columns and rows for the save slots in the game's save/load menu. This is needed because some games use custom save systems that the mod's autosave/quicksave system can't handle automatically.")

                        if SSSSS.Settings.customGridEnabled:
                            use SSSSS_YSpacer(2)

                            hbox:
                                use SSSSS_XSpacer()

                                hbox:
                                    vbox:
                                        text "Columns" xalign 0.5
                                        hbox:
                                            use sssss_iconButton(icon="\ue15b", action=SSSSS.Settings.DecrementCustomGridX())

                                            text str(SSSSS.Settings.customGridX) yalign 0.5

                                            use sssss_iconButton(icon="\ue145", action=SSSSS.Settings.IncrementCustomGridX())

                                    use SSSSS_XSpacer(2)

                                    vbox:
                                        text "Rows" xalign 0.5
                                        hbox:
                                            use sssss_iconButton(icon="\ue15b", action=SSSSS.Settings.DecrementCustomGridY())

                                            text str(SSSSS.Settings.customGridY) yalign 0.5

                                            use sssss_iconButton(icon="\ue145", action=SSSSS.Settings.IncrementCustomGridY())

                                grid SSSSS.Settings.customGridX SSSSS.Settings.customGridY spacing adjustable(5, minValue=1) offset (100, 0) yalign 0.5:
                                    for x in range(0, SSSSS.Settings.customGridX):
                                        for y in range(0, SSSSS.Settings.customGridY):
                                            frame style "SSSSS_default" xysize (10, 10) background SSSSS.Colors.theme

                            use SSSSS_YSpacer(2)

                        hbox:
                            use SSSSS_Checkbox(checked=SSSSS.Settings.offsetSlotAfterManualSaveIsLoaded, text="Always offset the slot after loading a manual save", action=SSSSS.Settings.ToggleOffsetSlotAfterManualSaveIsLoadedEnabled())
                            use SSSSS_Helper("If enabled, loading a save will shift the save slot by 1, ensuring the next autosave or quicksave does not overwrite the manual save.")
                            use SSSSS_ToggleSettingGlobalizationButton("offsetSlotAfterManualSaveIsLoaded")

                        hbox:
                            use SSSSS_Checkbox(checked=SSSSS.Settings.offsetSlotAfterManualSave, text="Offset the slot after a manual save is performed", action=SSSSS.Settings.ToggleOffsetSlotAfterManualSaveEnabled())
                            use SSSSS_Helper("If enabled, creating a manual save will shift the save slot by 1, preventing the next autosave or quicksave from overwriting it.")
                            use SSSSS_ToggleSettingGlobalizationButton("offsetSlotAfterManualSave")

                        use SSSSS_YSpacer(2)

                        hbox:
                            use SSSSS_XSpacer()

                            vbox:
                                use SSSSS_Title("Screens", 2)
                                
                                hbox:
                                    use SSSSS_XSpacer()

                                    vbox:
                                        use SSSSS_SettingsLoadSaveScreens()

                                        hbox:
                                            use sssss_iconButton("\ue8fb", text="Detach from settings", action=[Show("SSSSS_SettingsLoadSaveScreensStandalone"), SSSSS.SetSidepanelVisibilityAction(None), Hide("SSSSS_Settings")])
                                            use SSSSS_Helper("Click to isolate the 'Screens' section, hiding other settings for a focused view. Monitor real-time updates on currently displayed screens to easily choose the correct screen names, with immediate visual feedback on changes.")

                # Updates
                if not SSSSS.Updater.unavailable:
                    use SSSSS_YSpacer()

                    vbox:
                        hbox:
                            use SSSSS_Title("Updates")

                            use SSSSS_ToggleSettingGlobalizationButton("updaterEnabled", disabled=True, force_enabled=True)

                        vbox:
                            hbox:
                                hbox yalign 0.5:
                                    if SSSSS.Updater.latest:
                                        text "Latest version: {a=[SSSSS.Updater.latest_html_url]}[SSSSS.Updater.latest_version]"
                                    elif SSSSS.Updater.loading:
                                        text "Latest version: {color=[SSSSS.Colors.info]}Loading...{/color}"
                                    else:
                                        text "Latest version: {color=[SSSSS.Colors.na]}N/A{/color}"

                                use sssss_iconButton("\ue5d5", text="Refresh", action=SSSSS.Updater.CheckForUpdateAction())

                            use SSSSS_Checkbox(checked=SSSSS.Settings.updaterEnabled, text="Check for an update every time the game launches", action=SSSSS.Settings.ToggleUpdaterEnabled())

                            if SSSSS.Settings.updaterEnabled:
                                hbox:
                                    use SSSSS_XSpacer()

                                    vbox:
                                        use SSSSS_Checkbox(checked=SSSSS.Settings.autoUpdateWithoutPrompt, text="Perform automatic update without prompting", action=SSSSS.Settings.ToggleAutoUpdatesWithoutPromptEnabled())

                if renpy.config.developer:
                    use SSSSS_YSpacer()

                    vbox:
                        use SSSSS_Title("Debug", color=SSSSS.Colors.danger)
                        vbox:
                            use SSSSS_Checkbox(checked=SSSSS.Settings.debugEnabled, text="Debug mode", action=SSSSS.Settings.ToggleDebugEnabled())

                use SSSSS_YSpacer()

                hbox:
                    xfill True

                    vbox xalign 0.5:
                        hbox xalign 0.5:
                            use SSSSS_Title(SSSSS.MOD_NAME + " v" + SSSSS.MOD_VERSION)
                        text "{a=https://github.com/[SSSSS.MOD_GITHUB_OWNER]/[SSSSS.MOD_GITHUB_REPO]}Click here to open the GitHub page.{/a}" xalign 0.5
                        text "{a=https://github.com/[SSSSS.MOD_GITHUB_OWNER]/[SSSSS.MOD_GITHUB_REPO]/issues}Click here to view and/or submit issue(s).{/a}" xalign 0.5

        hbox:
            xfill True
            yfill True

            style_prefix "SSSSS_dialog_action_buttons"

            vbox:
                # Reset
                hbox:
                    use sssss_iconButton(icon="\ue8ba", text="Reset", action=Show("SSSSS_ResetSettingsConfirm"), color=SSSSS.Colors.danger)

                # Close
                hbox:
                    use sssss_iconButton(icon="\ue5cd", text="Close", action=Hide("SSSSS_Settings"))
    
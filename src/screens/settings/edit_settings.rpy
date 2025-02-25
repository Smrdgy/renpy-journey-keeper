screen JK_Settings():
    layer "JK_Overlay"
    style_prefix 'JK'
    modal True

    default originalSizeAdjustment = JK.Settings.sizeAdjustment

    python:
        reset_size_adjustment_hint = "If anything goes wrong, you can revert the value via:\n  a) confirm dialog\n  b) waiting for 60 seconds\n  c) manually, by simultaneously pressing {b}CTRL + SHIFT + ALT + P{/b}."

        default_close_action = Hide("JK_Settings")
        close_action = default_close_action
        if originalSizeAdjustment != JK.Settings.sizeAdjustment:
            close_action = [JK.ShowConfirmAction(title="You have unapplied size adjustment, would you like to apply it now?", message=reset_size_adjustment_hint, yes=[JK.Settings.ApplySizeAdjustment(), default_close_action], yesText="Apply now", yesColor=JK.Colors.success, noText="Back")]

    use JK_Dialog(title="Settings", closeAction=close_action):
        style_prefix "JK"

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            pagekeys True
            ymaximum 0.85

            vbox:
                # Accessibility
                vbox:
                    use JK_Title("Accessibility")
                    vbox:
                        use JK_Title("Size adjustment", 2)

                        hbox:
                            hbox:
                                yalign 0.0

                                use JK_IconButton(icon="\ue15b", action=JK.Settings.DecrementSizeAdjustment())

                                hbox xminimum 40 yalign 0.5:
                                    text ("+" if JK.Settings.sizeAdjustment > 0 else "") + str(JK.Settings.sizeAdjustment) xalign 0.5

                                use JK_IconButton(icon="\ue145", action=JK.Settings.IncrementSizeAdjustment())

                                use JK_IconButton(icon="\ue8ba", action=JK.Settings.ResetSizeAdjustment(), color=JK.Colors.reset, disabled=JK.Settings.sizeAdjustment == 0)

                                use JK_XSpacer()

                            hbox:
                                text "T" yalign 1.0

                                hbox xsize 5

                                text "T" size JK.scaled(20) yalign 1.0

                    text "The first 'T' represents the default text size, while the second 'T' reflects the applied scaling and any additional size adjustment"

                    if originalSizeAdjustment != JK.Settings.sizeAdjustment:
                        use JK_InfoBox(reset_size_adjustment_hint)

                        use JK_IconButton(icon="\ue86c", text="Click here to apply the new size\n{size=-7}{color=[JK.Colors.warning]}This will rebuild all the styles of the game, so don't be scared if it takes a few seconds.{/color}{/size}", action=[JK.Settings.ApplySizeAdjustment(), SetScreenVariable("originalSizeAdjustment", JK.Settings.sizeAdjustment)])

                use JK_YSpacer()

                # Autosave
                vbox:
                    use JK_Title("Autosave")
                    vbox:
                        hbox:
                            use JK_Checkbox(checked=JK.Settings.autosaveNotificationEnabled, text="Show notification when autosave is performed", action=JK.Settings.ToggleEnabled("autosaveNotificationEnabled"))
                            use JK_ToggleSettingGlobalizationButton("autosaveNotificationEnabled")

                        hbox:
                            use JK_Checkbox(checked=JK.Settings.pageFollowsAutoSave, text="Change page based on the auto-saved slot", action=JK.Settings.ToggleEnabled("pageFollowsAutoSave"))
                            use JK_ToggleSettingGlobalizationButton("pageFollowsAutoSave")
                        
                        hbox:
                            use JK_Checkbox(checked=JK.Settings.autosaveOnSingletonChoice, text="Perform autosave even when only one choice is available", action=JK.Settings.ToggleEnabled("autosaveOnSingletonChoice"))
                            use JK_Helper("When enabled, an autosave will be created even when there is only one choice is displayed.")
                            use JK_ToggleSettingGlobalizationButton("autosaveOnSingletonChoice")

                        hbox:
                            use JK_Checkbox(checked=JK.Settings.autosaveOnQuestion, text="Perform autosave on questions", action=JK.Settings.ToggleEnabled("autosaveOnQuestion"))
                            use JK_Helper("When disabled, the autosave system will attempt to prevent saving choices that loop back to the menu where they were made. This typically occurs in \"question\" menus, where none of the choices have an actual impact on story beyond providing exposition.\n\n{color=[JK.Colors.info]}Note: Even with this setting disabled, the choice may still be saved if it contains code that alters any variables.\nThis will mostly occur in menus where choices disappear after being selected.{/color}")
                            use JK_ToggleSettingGlobalizationButton("autosaveOnQuestion")

                        use JK_YSpacer(2)

                        hbox:
                            text "Toggle autosave key" yalign 0.5
                            use JK_ToggleSettingGlobalizationButton("autosaveKey")
                        use JK_KeyInput(assignment=JK.Settings.autosaveKey, action=JK.Settings.SetAutosaveToggleKey)

                        use JK_YSpacer(2)

                        use JK_Title("Advanced", size=3, color=JK.Colors.warning)

                        hbox:
                            use JK_Checkbox(checked=JK.Settings.preventAutosavingWhileNotInGame, text="Restict autosave to in-game only", action=JK.Settings.TogglePreventAutosavingWhileNotInGameEnabled())
                            use JK_Helper("Some games might not properly indicate when the game starts, which could prevent autosave on choices from working. Disabling this setting {b}may{/b} allow autosave to function as intended.\n\nFor technically apt users: The mod waits for the {u}start{/u} label to allow autosaving to function.\n\n{color=[JK.Colors.warning]}Warning! Disabling this might cause save(s) loss. For example, an 18+ age check might overwrite the 1-1 save slot, if it shows up before the main menu.{/color}")

                use JK_YSpacer()

                # Quick save
                vbox:
                    use JK_Title("Quick save")
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

                use JK_YSpacer()

                # Sidepanel
                vbox:
                    use JK_Title("Sidepanel")
                    vbox:
                        use JK_IconButton("\ue8ba", text="Reset position", action=JK.Settings.ResetSidepanelPosition())

                        use JK_YSpacer(2)

                        use JK_Checkbox(checked=JK.Settings.sidepanelHorizontal, text="Horizontal", action=JK.Settings.ToggleSidepanelHorizontalEnabled())

                        use JK_YSpacer(2)

                        hbox:
                            text "Toggle visibility mode key" yalign 0.5
                            use JK_ToggleSettingGlobalizationButton("changeSidepanelVisibilityKey")

                        use JK_KeyInput(assignment=JK.Settings.changeSidepanelVisibilityKey, action=JK.Settings.SetChangeSidepanelVisibilityKey)

                use JK_YSpacer()

                # Memories
                vbox:
                    use JK_Title("Memories{size=-20}{color=[JK.Colors.danger]} WIP{/color}{/size}")
                    vbox:
                        use JK_Checkbox(checked=JK.Settings.memoriesEnabled, text="Enabled", action=JK.Settings.ToggleEnabled("memoriesEnabled"))

                        if JK.Settings.memoriesEnabled:
                            use JK_YSpacer(2)

                            hbox:
                                use JK_XSpacer()

                                vbox:
                                    hbox:
                                        text "Create memory key" yalign 0.5
                                        use JK_ToggleSettingGlobalizationButton("memoriesKey")

                                    use JK_KeyInput(assignment=JK.Settings.memoriesKey, action=JK.Settings.SetCreateMemoryKey, disabled=not JK.Settings.memoriesEnabled)

                use JK_YSpacer()

                # Save/Load
                vbox:
                    use JK_Title("Save/Load")
                    vbox:
                        hbox:
                            use JK_Checkbox(checked=JK.Settings.customGridEnabled, text="Custom slots grid", action=JK.Settings.ToggleEnabled("customGridEnabled"))
                            use JK_Helper("When enabled, two new options will appear where you can enter the number of columns and rows for the save slots in the game's save/load menu. This is needed because some games use custom save systems that the mod's autosave/quicksave system can't handle automatically.")

                        if JK.Settings.customGridEnabled:
                            use JK_YSpacer(2)

                            hbox:
                                use JK_XSpacer()

                                hbox:
                                    vbox:
                                        text "Columns" xalign 0.5
                                        hbox:
                                            use JK_IconButton(icon="\ue15b", action=JK.Settings.DecrementCustomGridX())

                                            text str(JK.Settings.customGridX) yalign 0.5

                                            use JK_IconButton(icon="\ue145", action=JK.Settings.IncrementCustomGridX())

                                    use JK_XSpacer(2)

                                    vbox:
                                        text "Rows" xalign 0.5
                                        hbox:
                                            use JK_IconButton(icon="\ue15b", action=JK.Settings.DecrementCustomGridY())

                                            text str(JK.Settings.customGridY) yalign 0.5

                                            use JK_IconButton(icon="\ue145", action=JK.Settings.IncrementCustomGridY())

                                grid JK.Settings.customGridX JK.Settings.customGridY spacing JK.scaled(5) offset JK.scaled((100, 0)) yalign 0.5:
                                    for x in range(0, JK.Settings.customGridX):
                                        for y in range(0, JK.Settings.customGridY):
                                            frame style "JK_default" xysize JK.scaled((10, 10)) background JK.Colors.theme

                            use JK_YSpacer(2)

                        hbox:
                            use JK_Checkbox(checked=JK.Settings.offsetSlotAfterManualSaveIsLoaded, text="Always offset the slot after loading a manual save", action=JK.Settings.ToggleEnabled("offsetSlotAfterManualSaveIsLoaded"))
                            use JK_Helper("If enabled, loading a save will shift the save slot by 1, ensuring the next autosave or quicksave does not overwrite the manual save.")
                            use JK_ToggleSettingGlobalizationButton("offsetSlotAfterManualSaveIsLoaded")

                        hbox:
                            use JK_Checkbox(checked=JK.Settings.offsetSlotAfterManualSave, text="Offset the slot after a manual save is performed", action=JK.Settings.ToggleEnabled("offsetSlotAfterManualSave"))
                            use JK_Helper("If enabled, creating a manual save will shift the save slot by 1, preventing the next autosave or quicksave from overwriting it.")
                            use JK_ToggleSettingGlobalizationButton("offsetSlotAfterManualSave")

                        use JK_YSpacer(2)

                        vbox:
                            hbox:
                                text "Search playthrough key" yalign 0.5
                                use JK_ToggleSettingGlobalizationButton("searchPlaythroughKey")

                            use JK_KeyInput(assignment=JK.Settings.searchPlaythroughKey, action=JK.Settings.SetSearchPlaythroughKey)

                            hbox:
                                text "Search all playthroughs key" yalign 0.5
                                use JK_ToggleSettingGlobalizationButton("searchPlaythrougshKey")

                            use JK_KeyInput(assignment=JK.Settings.searchPlaythroughsKey, action=JK.Settings.SetSearchPlaythroughsKey)

                        use JK_YSpacer(2)

                        hbox:
                            use JK_XSpacer()

                            vbox:
                                use JK_Title("Screens", 2)
                                
                                hbox:
                                    use JK_XSpacer()

                                    vbox:
                                        use JK_SettingsLoadSaveScreens()

                                        use JK_YSpacer(2)

                                        hbox:
                                            use JK_IconButton("\ue8fb", text="Detach from settings", action=[Show("JK_SettingsLoadSaveScreensStandalone"), JK.SetSidepanelVisibilityAction(None), Hide("JK_Settings")])
                                            use JK_Helper("Click to isolate the 'Screens' section, hiding other settings for a focused view. Monitor real-time updates on currently displayed screens to easily choose the correct screen names, with immediate visual feedback on changes.")

                                use JK_YSpacer(2)

                                use JK_Title("Pagination", 2)

                                hbox:
                                    use JK_XSpacer()

                                    vbox:
                                        hbox:
                                            use JK_Checkbox(checked=JK.Settings.seamlessPagination, text="Use seamless pagination", action=JK.Settings.ToggleEnabled("seamlessPagination"))
                                            use JK_Helper("When enabled, the active page number stays centered, making it easier to navigate through many pages. However, the page numbers may shift, which could feel a bit disorienting at first.\n\n{b}{color=[JK.Colors.theme]}Example{/color}{/b}\n\n{b}Normal:{/b}\nCurrent page = 7\nPages = {b}1 2 3 4 5 6 {color=[JK.Colors.selected]}7{/color} 8 9{/b}\n\n{b}Seamless:{/b}\nCurrent page = 7\nPages = {b}3 4 5 6 {color=[JK.Colors.selected]}7{/color} 8 9 10 11{/b}")
                                            use JK_ToggleSettingGlobalizationButton("seamlessPagination")

                # Updates
                if not JK.Updater.unavailable:
                    use JK_YSpacer()

                    vbox:
                        hbox:
                            use JK_Title("Updates")

                            use JK_ToggleSettingGlobalizationButton("updaterEnabled", disabled=True, force_enabled=True)

                        vbox:
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

                if renpy.config.developer:
                    use JK_YSpacer()

                    vbox:
                        use JK_Title("Debug", color=JK.Colors.danger)
                        vbox:
                            use JK_Checkbox(checked=JK.Settings.debugEnabled, text="Debug mode", action=JK.Settings.ToggleEnabled("debugEnabled"))

                use JK_YSpacer()

                hbox:
                    xfill True

                    vbox xalign 0.5:
                        hbox xalign 0.5:
                            use JK_Title(JK.MOD_NAME + " v" + JK.MOD_VERSION)

                        use JK_YSpacer(2)

                        text "{a=https://github.com/[JK.MOD_GITHUB_OWNER]/[JK.MOD_GITHUB_REPO]}Click here to open the GitHub page.{/a}" xalign 0.5 text_align 0.5

                        hbox ysize JK.scaled(5)

                        text "Encountered an issue?" xalign 0.5 text_align 0.5
                        text "Visit our {a=[JK.DISCORD_URL]}Discord{/a} or check {a=https://github.com/[JK.MOD_GITHUB_OWNER]/[JK.MOD_GITHUB_REPO]/issues}GitHub issues{/a}" xalign 0.5 text_align 0.5

        hbox:
            xfill True
            yfill True

            style_prefix "JK_dialog_action_buttons"

            vbox:
                # Reset
                hbox:
                    use JK_IconButton(icon="\ue8ba", text="Reset", action=Show("JK_ResetSettingsConfirm"), color=JK.Colors.danger)

                # Close
                hbox:
                    use JK_IconButton(icon="\ue5cd", text="Close", action=close_action)
    
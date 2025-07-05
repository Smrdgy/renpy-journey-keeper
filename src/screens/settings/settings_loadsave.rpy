screen JK_Settings_LoadSave():
    vbox:
        hbox:
            $ sub_text = ""
            if hasattr(renpy.store.gui, "file_slot_cols") and hasattr(renpy.store.gui, "file_slot_rows"):
                $ sub_text = "\n{color=[JK.Colors.text_light]}{size=-5}Config values: [renpy.store.gui.file_slot_cols], [renpy.store.gui.file_slot_rows]{/size}{/color}"

            use JK_Checkbox(checked=JK.Settings.customGridEnabled, text="Custom slots grid" + sub_text, action=JK.Settings.ToggleEnabledAction("customGridEnabled"))
            use JK_Helper("When enabled, two new options will appear where you can enter the number of columns and rows for the save slots in the game's save/load menu. This is needed because some games use custom save systems that the mod's autosave/quicksave system can't handle automatically.")

        if JK.Settings.customGridEnabled:
            use JK_YSpacer(2)

            hbox:
                use JK_XSpacer()

                hbox:
                    vbox:
                        text "Columns" xalign 0.5
                        hbox:
                            use JK_IconButton(icon="\ue15b", action=JK.Settings.DecrementAction("customGridX", min=1))

                            text str(JK.Settings.customGridX) yalign 0.5

                            use JK_IconButton(icon="\ue145", action=JK.Settings.IncrementAction("customGridX"))

                    use JK_XSpacer(2)

                    vbox:
                        text "Rows" xalign 0.5
                        hbox:
                            use JK_IconButton(icon="\ue15b", action=JK.Settings.DecrementAction("customGridY", min=1))

                            text str(JK.Settings.customGridY) yalign 0.5

                            use JK_IconButton(icon="\ue145", action=JK.Settings.IncrementAction("customGridY"))

                grid JK.Settings.customGridX JK.Settings.customGridY spacing JK.scaled(5) offset JK.scaled((100, 0)) yalign 0.5:
                    for x in range(0, JK.Settings.customGridX):
                        for y in range(0, JK.Settings.customGridY):
                            frame style "JK_default" xysize JK.scaled((10, 10)) background JK.Colors.theme

            use JK_YSpacer(2)
        
        hbox:
            use JK_Checkbox(checked=JK.Settings.showPlaythroughNameBanner, text="Show playthrough name banner", action=JK.Settings.ToggleEnabledAction("showPlaythroughNameBanner"))
            use JK_Helper("When enabled, a banner will appear at the top of the save/load screen, displaying the name of the currently active playthrough. This helps to quickly identify which playthrough you are currently viewing.")
            use JK_ToggleSettingGlobalizationButton("showPlaythroughNameBanner")

        hbox:
            use JK_XSpacer()

            vbox:
                hbox:
                    use JK_XSpacer(2)

                    use JK_IconButton("\ue8ba", text="Reset position", action=JK.Settings.ResetPlayhtroughBannerPositionAction(), disabled=not JK.Settings.showPlaythroughNameBanner)

                hbox:
                    use JK_Checkbox(checked=JK.Settings.playthroughBannerShowThumbnail, text="Show playthrough thumbnail", action=JK.Settings.ToggleEnabledAction("playthroughBannerShowThumbnail"), disabled=not JK.Settings.showPlaythroughNameBanner)
                    use JK_ToggleSettingGlobalizationButton("playthroughBannerShowThumbnail", disabled=not JK.Settings.showPlaythroughNameBanner)

                hbox:
                    use JK_Checkbox(checked=JK.Settings.playthroughBannerShowChangePlaythroughButtons, text="Show prev/next playthrough buttons", action=JK.Settings.ToggleEnabledAction("playthroughBannerShowChangePlaythroughButtons"), disabled=not JK.Settings.showPlaythroughNameBanner)
                    use JK_ToggleSettingGlobalizationButton("playthroughBannerShowChangePlaythroughButtons", disabled=not JK.Settings.showPlaythroughNameBanner)

        hbox:
            use JK_Checkbox(checked=JK.Settings.offsetSlotAfterManualSaveIsLoaded, text="Always offset the slot after loading a manual save", action=JK.Settings.ToggleEnabledAction("offsetSlotAfterManualSaveIsLoaded"))
            use JK_Helper("If enabled, loading a save will shift the save slot by 1, ensuring the next autosave or quicksave does not overwrite the manual save.")
            use JK_ToggleSettingGlobalizationButton("offsetSlotAfterManualSaveIsLoaded")

        hbox:
            use JK_Checkbox(checked=JK.Settings.offsetSlotAfterManualSave, text="Offset the slot after a manual save is performed", action=JK.Settings.ToggleEnabledAction("offsetSlotAfterManualSave"))
            use JK_Helper("If enabled, creating a manual save will shift the save slot by 1, preventing the next autosave or quicksave from overwriting it.")
            use JK_ToggleSettingGlobalizationButton("offsetSlotAfterManualSave")

        use JK_YSpacer()

        use JK_Title("Search")

        vbox:
            hbox:
                text "Search playthrough key" yalign 0.5
                use JK_ToggleSettingGlobalizationButton("searchPlaythroughKey")

            use JK_KeyInput(assignment=JK.Settings.searchPlaythroughKey, action=JK.Settings.get_set_key_action("searchPlaythroughKey"), supress_ctrl_warning=True)

        use JK_YSpacer(2)

        vbox:
            hbox:
                text "Search all playthroughs key" yalign 0.5
                use JK_ToggleSettingGlobalizationButton("searchPlaythrougshKey")

            use JK_KeyInput(assignment=JK.Settings.searchPlaythroughsKey, action=JK.Settings.get_set_key_action("searchPlaythroughsKey"), supress_ctrl_warning=True)

        use JK_YSpacer()

        vbox:
            hbox:
                use JK_Title("Screens")

                hbox:
                    yalign 0.5

                    use JK_Helper("Here you can select screens that represent save/load screens. On the selected screens, the sidepanel will be visible.")

            use JK_YSpacer(3)
            
            hbox:
                use JK_XSpacer()

                vbox:
                    use JK_SettingsLoadSaveScreens()

                    use JK_YSpacer(2)

                    hbox:
                        use JK_IconButton("\ue8fb", text="Click here to detach from settings", action=[Show("JK_SettingsLoadSaveScreensStandalone"), JK.SetSidepanelVisibilityAction(None), Hide("JK_Settings")])
                        use JK_Helper("Click to isolate the {color=[JK.Colors.theme]}{b}Screens{/b}{/color} section, hiding other settings for a focused view.\nIn this mode, you can monitor real-time updates on currently displayed screens to easily choose the correct screen names, with immediate visual feedback on changes.")

            use JK_YSpacer()

            use JK_Title("Pagination")

            hbox:
                use JK_XSpacer()

                vbox:
                    hbox:
                        use JK_Checkbox(checked=JK.Settings.seamlessPagination, text="Use seamless pagination", action=JK.Settings.ToggleEnabledAction("seamlessPagination"))
                        use JK_Helper("When enabled, the active page number stays centered, making it easier to navigate through many pages. However, the page numbers may shift, which could feel a bit disorienting at first.\n\n{b}{color=[JK.Colors.theme]}Example{/color}{/b}\n\n{b}Normal:{/b}\nCurrent page = 7\nPages = {b}1 2 3 4 5 6 {color=[JK.Colors.selected]}7{/color} 8 9{/b}\n\n{b}Seamless:{/b}\nCurrent page = 7\nPages = {b}3 4 5 6 {color=[JK.Colors.selected]}7{/color} 8 9 10 11{/b}")
                        use JK_ToggleSettingGlobalizationButton("seamlessPagination")

                    use JK_YSpacer(2)

                    use JK_Title("Customization", 2)

                    hbox:
                        use JK_XSpacer()

                        vbox:
                            hbox:
                                use JK_Checkbox(checked=JK.Settings.paginationGoTo, text="Show go-to button", action=JK.Settings.ToggleEnabledAction("paginationGoTo"))
                                use JK_ToggleSettingGlobalizationButton("paginationGoTo")

                            hbox:
                                use JK_Checkbox(checked=JK.Settings.paginationAutoSaves, text="Show Autosaves button", action=JK.Settings.ToggleEnabledAction("paginationAutoSaves"))
                                use JK_ToggleSettingGlobalizationButton("paginationAutoSaves")

                            hbox:
                                use JK_Checkbox(checked=JK.Settings.paginationQuickSaves, text="Show Quick Saves button", action=JK.Settings.ToggleEnabledAction("paginationQuickSaves"))
                                use JK_ToggleSettingGlobalizationButton("paginationQuickSaves")

                            hbox:
                                use JK_Checkbox(checked=JK.Settings.paginationFirstPage, text="Show \"Jump to the first page\" button", action=JK.Settings.ToggleEnabledAction("paginationFirstPage"))
                                use JK_ToggleSettingGlobalizationButton("paginationFirstPage")

                            hbox:
                                use JK_Checkbox(checked=JK.Settings.paginationBigJump, text="Show << and >> buttons", action=JK.Settings.ToggleEnabledAction("paginationBigJump"))
                                use JK_ToggleSettingGlobalizationButton("paginationBigJump")

                            hbox:
                                use JK_Checkbox(checked=JK.Settings.paginationNumbers, text="Show page numbers", action=JK.Settings.ToggleEnabledAction("paginationNumbers"))
                                use JK_ToggleSettingGlobalizationButton("paginationNumbers")

                            hbox:
                                use JK_Checkbox(checked=JK.Settings.paginationLastPage, text="Show \"Jump to the last page\" button", action=JK.Settings.ToggleEnabledAction("paginationLastPage"))
                                use JK_ToggleSettingGlobalizationButton("paginationLastPage")

                    use JK_YSpacer(2)

                    use JK_Title("Preview", 3)

                    use JK_YSpacer(3)

                    hbox:
                        use JK_XSpacer(2)

                        use JK_PaginationContent(JK.Pagination.get_content())
screen JK_Settings_Autosave():
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

        hbox:
            use JK_Checkbox(checked=JK.Settings.showConfirmOnLargePageJump, text="Show confirmation on unexpected large page jump", action=JK.Settings.ToggleEnabled("showConfirmOnLargePageJump"))
            use JK_Helper("When enabled, a confirmation prompt will appear if the page number jumps unexpectedly far during gameplay (by more than one page)")
            use JK_ToggleSettingGlobalizationButton("showConfirmOnLargePageJump")

        use JK_YSpacer(2)

        hbox:
            text "Toggle autosave key" yalign 0.5
            use JK_ToggleSettingGlobalizationButton("autosaveKey")

        use JK_KeyInput(assignment=JK.Settings.autosaveKey, action=JK.Settings.SetAutosaveToggleKey)

        use JK_YSpacer()

        use JK_Title("Advanced", color=JK.Colors.warning)

        hbox:
            use JK_Checkbox(checked=JK.Settings.preventAutosavingWhileNotInGame, text="Restict autosave to in-game only", action=JK.Settings.TogglePreventAutosavingWhileNotInGameEnabled())
            use JK_Helper("Some games might not properly indicate when the game starts, which could prevent autosave on choices from working. Disabling this setting {b}may{/b} allow autosave to function as intended.\n\nFor technically apt users: This mod waits for the {u}start{/u} label to allow autosaving to function.\n\n{color=[JK.Colors.warning]}Warning! Disabling this might cause save(s) loss. For example, an 18+ age check might overwrite the 1-1 save slot, if it shows up before the main menu.{/color}")

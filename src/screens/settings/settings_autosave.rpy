screen JK_Settings_Autosave():
    vbox:
        hbox:
            use JK_Checkbox(checked=JK.Settings.autosaveNotificationEnabled, text="Show notification when autosave is performed", action=JK.Settings.ToggleEnabledAction("autosaveNotificationEnabled"))
            use JK_ToggleSettingGlobalizationButton("autosaveNotificationEnabled")

        hbox:
            use JK_Checkbox(checked=JK.Settings.pageFollowsAutoSave, text="Change page based on the auto-saved slot", action=JK.Settings.ToggleEnabledAction("pageFollowsAutoSave"))
            use JK_ToggleSettingGlobalizationButton("pageFollowsAutoSave")
        
        hbox:
            use JK_Checkbox(checked=JK.Settings.autosaveOnSingletonChoice, text="Perform autosave even when only one choice is available", action=JK.Settings.ToggleEnabledAction("autosaveOnSingletonChoice"))
            use JK_Helper("When enabled, an autosave will be created even when there is only one choice is displayed.")
            use JK_ToggleSettingGlobalizationButton("autosaveOnSingletonChoice")

        # Shelved feature, check __is_question() in Autosaver for more info
        # hbox:
        #     use JK_Checkbox(checked=JK.Settings.autosaveOnQuestion, text="Perform autosave on questions", action=JK.Settings.ToggleEnabledAction("autosaveOnQuestion"))
        #     use JK_Helper("When disabled, the autosave system will attempt to prevent saving choices that loop back to the menu where they were made. This typically occurs in \"question\" menus, where none of the choices have an actual impact on story beyond providing exposition.\n\n{color=[JK.Colors.info]}Note: Even with this setting disabled, the choice may still be saved if it contains code that alters any variables.\nThis will mostly occur in menus where choices disappear after being selected.{/color}")
        #     use JK_ToggleSettingGlobalizationButton("autosaveOnQuestion")

        hbox:
            use JK_Checkbox(checked=JK.Settings.showConfirmOnLargePageJump, text="Show confirmation on unexpected large page jump", action=JK.Settings.ToggleEnabledAction("showConfirmOnLargePageJump"))
            use JK_Helper("When enabled, a confirmation prompt will appear if the page number jumps unexpectedly far during gameplay (by more than one page)")
            use JK_ToggleSettingGlobalizationButton("showConfirmOnLargePageJump")

        use JK_YSpacer(2)

        hbox:
            text "Prevent autosave modifier key" yalign 0.5
            use JK_Helper("While holding this key, autosave won't be performed when you make a choice")
            use JK_ToggleSettingGlobalizationButton("preventAutosaveModifierKey")

        use JK_Radio(checked=not JK.Settings.preventAutosaveModifierKey, text="None", action=JK.Settings.SetAction("preventAutosaveModifierKey", None))
        use JK_Radio(checked="ALT" == JK.Settings.preventAutosaveModifierKey, text="Alt", action=JK.Settings.SetAction("preventAutosaveModifierKey", "ALT"))
        use JK_Radio(checked="SHIFT" == JK.Settings.preventAutosaveModifierKey, text="Shift", action=JK.Settings.SetAction("preventAutosaveModifierKey", "SHIFT"))

        use JK_YSpacer(2)

        hbox:
            text "Toggle autosave key" yalign 0.5
            use JK_ToggleSettingGlobalizationButton("autosaveKey")

        use JK_KeyInput(assignment=JK.Settings.autosaveKey, action=JK.Settings.get_set_key_action("autosaveKey"))

        use JK_YSpacer()

        use JK_Title("Advanced", color=JK.Colors.warning)

        hbox:
            use JK_Checkbox(checked=JK.Settings.preventAutosavingWhileNotInGame, text="Restict autosave to in-game only", action=JK.Settings.TogglePreventAutosavingWhileNotInGameEnabledAction())
            use JK_Helper("Some games might not properly indicate when the game starts, which could prevent autosave on choices from working. Disabling this setting {b}may{/b} allow autosave to function as intended.\n\nFor technically apt users: This mod waits for the {u}start{/u} label to allow autosaving to function.\n\n{color=[JK.Colors.warning]}Warning! Disabling this might cause save(s) loss. For example, an 18+ age check might overwrite the 1-1 save slot, if it shows up before the main menu.{/color}")

        hbox:
            use JK_Checkbox(checked=JK.Settings.autosaveOnNormalButtonsWithJump, text="Perform autosave on normal buttons", action=JK.Settings.ToggleEnabledAction("autosaveOnNormalButtonsWithJump"))
            use JK_Helper("{color=[JK.Colors.info]}If choices aren't triggering autosaves as expected, enabling this option may help.{/color}\n\nWhen enabled, every Button behaves as a choice button, triggering an autosave when clicked. However, only specific buttons qualify—those that logically represent choices in the game.\n{color=[JK.Colors.warning]}Be aware that some non-choice buttons, like free-roam navigation buttons, may still trigger autosaves.{/color}\n\n{b}For the curious advanced users:{/b}\nAutosaves are only performed on Buttons with a Jump action, ensuring that only navigation-relevant interactions are considered. Unfortunately, this filtering cannot be refined any further.")

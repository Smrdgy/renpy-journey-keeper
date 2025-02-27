screen JK_Settings(section="ACCESSIBILITY"):
    layer "JK_Overlay"
    style_prefix 'JK'
    modal True

    default originalSizeAdjustment = JK.Settings.sizeAdjustment
    default active_section = section

    python:
        reset_size_adjustment_hint = "If anything goes wrong, you can revert the value via:\n  a) confirm dialog\n  b) waiting 60 seconds\n  c) manually, by simultaneously pressing {b}CTRL + SHIFT + ALT + P{/b}."

        default_close_action = Hide("JK_Settings")
        close_action = default_close_action
        if originalSizeAdjustment != JK.Settings.sizeAdjustment and JK.Settings.sizeAdjustment != 0:
            close_action = [JK.ShowConfirmAction(title="You have unapplied size adjustment, would you like to apply it now?", message=reset_size_adjustment_hint, yes=[JK.Settings.ApplySizeAdjustment(), default_close_action], yesText="Apply now", yesColor=JK.Colors.success, noText="Back")]

        sections = [
            ("ACCESSIBILITY", "\ue84e", "Accessibility"),
            ("AUTOSAVE", "\ue167", "Autosave"),
            ("QUICKSAVE", "\ue161", "Quick save"),
            ("SIDEPANEL", "\ue8aa", "Sidepanel"),
            ("MEMORIES", "\ue02c", "Memories{size=-20}{color=[JK.Colors.danger]} WIP{/color}{/size}"),
            ("SAVE_LOAD", "\ue0e0", "Save/Load"),
            ("CUSTOMIZATION", "\ue40a", "Customize"),
            ("UPDATES", "\ue62a", "Updates"),
        ]

        if renpy.config.developer:
            sections.append(("DEBUG", "\ue868", "Debug"))

    use JK_Dialog(title="Settings", closeAction=close_action):
        style_prefix "JK"

        grid len(sections) 1:
            xfill True

            style_prefix "JK_Settings_Tab"

            for section in sections:
                button:
                    xfill True

                    if section[0] == "DEBUG":
                        selected JK.Settings.debugEnabled
                        style "JK_Settings_Tab_button_debug"
                        action JK.Settings.ToggleEnabled("debugEnabled")

                    else:
                        selected section[0] == active_section
                        action SetScreenVariable("active_section", section[0])

                    vbox:
                        xalign 0.5

                        if section[1]:
                            hbox:
                                xalign 0.5

                                use JK_Icon(section[1])

                        use JK_YSpacer(4)

                        text section[2]

        use JK_YSpacer(2)

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            pagekeys True
            ymaximum 0.85

            if active_section == "ACCESSIBILITY":
                use JK_Settings_Accessibility(originalSizeAdjustment, reset_size_adjustment_hint)
            elif active_section == "AUTOSAVE":
                use JK_Settings_Autosave()
            elif active_section == "QUICKSAVE":
                use JK_Settings_QuickSave()
            elif active_section == "SIDEPANEL":
                use JK_Settings_Sidepanel()
            elif active_section == "MEMORIES":
                use JK_Settings_Memories()
            elif active_section == "SAVE_LOAD":
                use JK_Settings_LoadSave()
            elif active_section == "UPDATES":
                use JK_Settings_Updater()
            elif active_section == "CUSTOMIZATION":
                use JK_Settings_Customization()

        hbox:
            xfill True
            yfill True

            vbox:
                yalign 1.0

                use JK_Title(JK.MOD_NAME + " v" + JK.MOD_VERSION)

                use JK_YSpacer(2)

                use JK_Title("Encountered an issue?", size=3, color=JK.Colors.error)
                text "Visit our {a=[JK.DISCORD_URL]}Discord{/a} or check {a=https://github.com/[JK.MOD_GITHUB_OWNER]/[JK.MOD_GITHUB_REPO]}GitHub{/a}."

            hbox:
                style_prefix "JK_dialog_action_buttons"

                vbox:
                    # Reset
                    hbox:
                        use JK_IconButton(icon="\ue8ba", text="Reset", action=Show("JK_ResetSettingsConfirm"), color=JK.Colors.danger)

                    # Close
                    hbox:
                        use JK_IconButton(icon="\ue5cd", text="Close", action=close_action)
    
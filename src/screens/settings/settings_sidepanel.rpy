screen JK_Settings_Sidepanel():
    vbox:
        use JK_IconButton("\ue8ba", text="Reset position", action=JK.Settings.ResetSidepanelPositionAction())

        use JK_YSpacer(2)

        use JK_Checkbox(checked=JK.Settings.sidepanelHorizontal, text="Horizontal", action=JK.Settings.ToggleSidepanelHorizontalEnabledAction())

        use JK_YSpacer(2)

        hbox:
            text "Change visibility mode key" yalign 0.5
            use JK_ToggleSettingGlobalizationButton("changeSidepanelVisibilityKey")

        use JK_KeyInput(assignment=JK.Settings.changeSidepanelVisibilityKey, action=JK.Settings.SetChangeSidepanelVisibilityKeyAction)
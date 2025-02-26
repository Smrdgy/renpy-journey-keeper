screen JK_Settings_Memories():
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
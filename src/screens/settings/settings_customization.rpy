screen JK_Settings_Customization():
    vbox:
        use JK_Title("Opacity")

        hbox:
            text "Dialog" yalign 0.5
            use JK_ToggleSettingGlobalizationButton("dialogOpacity")

        hbox:
            bar value JK.Settings.FieldValueAction(JK.Settings, "dialogOpacity", range=1.0, step=0.01) xsize 0.3
            text str(int(JK.Settings.dialogOpacity * 100)) + "%" yalign 0.5 xoffset JK.scaled(10)

        use JK_YSpacer(2)

        hbox:
            text "Sidepanel" yalign 0.5
            use JK_ToggleSettingGlobalizationButton("sidepanelOpacity")

        hbox:
            bar value JK.Settings.FieldValueAction(JK.Settings, "sidepanelOpacity", range=1.0, step=0.01) xsize 0.3
            text str(int(JK.Settings.sidepanelOpacity * 100)) + "%" yalign 0.5 xoffset JK.scaled(10)

        use JK_YSpacer(2)

        hbox:
            text "Pagination" yalign 0.5
            use JK_ToggleSettingGlobalizationButton("paginationOpacity")

        hbox:
            bar value JK.Settings.FieldValueAction(JK.Settings, "paginationOpacity", range=1.0, step=0.01) xsize 0.3
            text str(int(JK.Settings.paginationOpacity * 100)) + "%" yalign 0.5 xoffset JK.scaled(10)

screen JK_Settings_Accessibility(originalSizeAdjustment, reset_size_adjustment_hint):
    vbox:
        use JK_Title("Size adjustment")

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

        use JK_YSpacer(2)

        use JK_InfoBox(reset_size_adjustment_hint)

        use JK_YSpacer(2)

        if originalSizeAdjustment != JK.Settings.sizeAdjustment:
            use JK_IconButton(icon="\ue86c", text="Click here to apply the new size\n{size=-7}{color=[JK.Colors.warning]}This will rebuild all the styles of the game, so don't be scared if it takes a few seconds.{/color}{/size}", action=[JK.Settings.ApplySizeAdjustment(), SetScreenVariable("originalSizeAdjustment", JK.Settings.sizeAdjustment)])
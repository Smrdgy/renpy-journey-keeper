screen SSSSS_Settings():
    layer "SSSSSoverlay"
    style_prefix 'SSSSS'
    modal True

    #TODO: Move this into another thread? Or maybe make the sceens load on button click so that only when it's needed it will be there?; https://stackoverflow.com/questions/7168508/background-function-in-python
    default activeScreens = [screen[0] for screen in renpy.display.screen.screens if (renpy.get_screen(screen) and not ("SSSSS_" in screen[0] or screen[0] == "save" or screen[0] == "load"))]

    use SSSSS_Dialog(title="Settings", closeAction=Hide("SSSSS_Settings")):
        style_prefix "SSSSS"

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            pagekeys True
            ymaximum 0.85

            vbox:
                vbox:
                    text "Accessibility" size 40

                    hbox:
                        hbox xsize 40

                        vbox:
                            text("Size adjustment")

                            hbox:
                                use sssss_iconButton(icon="\ue15b", action=SSSSS.Settings.DecrementSizeAdjustment())

                                text str(SSSSS.Settings.sizeAdjustment) + "%" yalign 0.5

                                use sssss_iconButton(icon="\ue145", action=SSSSS.Settings.IncrementSizeAdjustment())


                vbox:
                    text "Autosave" size 40

                    hbox:
                        hbox xsize 40

                        vbox:
                            use SSSSS_Checkbox(checked=SSSSS.Settings.autosaveNotificationEnabled, text="Show notification when autosave is performed", action=SSSSS.Settings.ToggleAutosaveNotificationEnabled())
                            
                            vbox ysize 15

                            text "Toggle autosave key"
                            use SSSSS_KeyInput(assignment=SSSSS.Settings.autosaveKey, action=SSSSS.Settings.SetAutosaveToggleKey)

                vbox ysize 40

                vbox:
                    text "Quick save" size 40

                    hbox:
                        hbox xsize 40

                        vbox:
                            use SSSSS_Checkbox(checked=SSSSS.Settings.quickSaveEnabled, text="Enabled", action=SSSSS.Settings.ToggleQuickSaveEnabled())

                            if SSSSS.Settings.quickSaveEnabled:
                                hbox:
                                    hbox xsize 40

                                    vbox:
                                        use SSSSS_Checkbox(checked=SSSSS.Settings.quickSaveNotificationEnabled, text="Show notification when quick save is performed", action=SSSSS.Settings.ToggleQuickSaveNotificationEnabled(), disabled=not SSSSS.Settings.quickSaveEnabled)

                                        vbox ysize 15

                                        text "Perform quick save key"
                                        use SSSSS_KeyInput(assignment=SSSSS.Settings.quickSaveKey, action=SSSSS.Settings.SetQuickSaveKey, disabled=not SSSSS.Settings.quickSaveEnabled)

                vbox ysize 40

                vbox:
                    text "Memories" size 40

                    hbox:
                        hbox xsize 40

                        vbox:
                            use SSSSS_Checkbox(checked=SSSSS.Settings.memoriesEnabled, text="Enabled", action=SSSSS.Settings.ToggleMemoriesEnabled())

                            if SSSSS.Settings.memoriesEnabled:
                                vbox ysize 15

                                hbox:
                                    hbox xsize 40

                                    vbox:
                                        text "Create memory key"
                                        use SSSSS_KeyInput(assignment=SSSSS.Settings.memoriesKey, action=SSSSS.Settings.SetCreateMemoryKey, disabled=not SSSSS.Settings.memoriesEnabled)

                vbox ysize 40

                vbox:
                    text "Save/Load" size 40

                    hbox:
                        hbox xsize 40

                        vbox:
                            use SSSSS_Checkbox(checked=SSSSS.Settings.customGridEnabled, text="Custom slots grid", action=SSSSS.Settings.ToggleCustomGridEnabled())

                            vbox ysize 20

                            if SSSSS.Settings.customGridEnabled:
                                hbox:
                                    hbox xsize 40

                                    hbox:
                                        vbox:
                                            text "X axis" color ("#fff" if SSSSS.Settings.customGridEnabled else "#2f2f2f55") xalign 0.5
                                            hbox:
                                                use sssss_iconButton(icon="\ue15b", action=SSSSS.Settings.DecrementCustomGridX())

                                                text str(SSSSS.Settings.customGridX) yalign 0.5 color ("#fff" if SSSSS.Settings.customGridEnabled else "#2f2f2f55")

                                                use sssss_iconButton(icon="\ue145", action=SSSSS.Settings.IncrementCustomGridX())

                                        hbox xsize 20

                                        vbox:
                                            text "Y axis" color ("#fff" if SSSSS.Settings.customGridEnabled else "#2f2f2f55") xalign 0.5
                                            hbox:
                                                use sssss_iconButton(icon="\ue15b", action=SSSSS.Settings.DecrementCustomGridY())

                                                text str(SSSSS.Settings.customGridY) yalign 0.5 color ("#fff" if SSSSS.Settings.customGridEnabled else "#2f2f2f55")

                                                use sssss_iconButton(icon="\ue145", action=SSSSS.Settings.IncrementCustomGridY())

                                    grid SSSSS.Settings.customGridX SSSSS.Settings.customGridY spacing 5 offset (100, 0) yalign 0.5:
                                        for x in range(0, SSSSS.Settings.customGridX):
                                            for y in range(0, SSSSS.Settings.customGridY):
                                                frame style "SSSSS_default" xysize (10, 10) background ("#fff" if SSSSS.Settings.customGridEnabled else "#2f2f2f55")

                            vbox ysize 20

                            python:
                                relevantSaveScreens = ["save"] + activeScreens
                                relevantLoadScreens = ["load"] + activeScreens

                            vbox:
                                text "Save page" size 25
                                for screen in relevantSaveScreens:
                                    use SSSSS_Radio(checked=SSSSS.Settings.saveScreenName == screen, text=("\"save\" (default)" if screen == "save" else "\"" + screen + "\""), action=SSSSS.Settings.SetSaveScreenName(screen))

                                vbox ysize 15

                                text "Load page" size 25
                                for screen in relevantLoadScreens:
                                    use SSSSS_Radio(checked=SSSSS.Settings.loadScreenName == screen, text=("\"load\" (default)" if screen == "load" else "\"" + screen + "\""), action=SSSSS.Settings.SetLoadScreenName(screen))

        hbox:
            xfill True
            yfill True

            vbox at right:
                yalign 1.0

                # Save
                hbox at right:
                    use sssss_iconButton(icon="\ue8ba", text="Reset", action=SSSSS.Settings.Reset()) #TODO: Confirm

                # Close
                hbox at right:
                    use sssss_iconButton(icon="\ue5cd", text="Close", action=Hide("SSSSS_Settings"))
    
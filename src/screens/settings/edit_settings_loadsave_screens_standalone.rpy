screen SSSSS_SettingsLoadSaveScreensStandalone():
    layer "SSSSSoverlay"
    style_prefix "SSSSS"

    drag:
        draggable True
        drag_handle (0, 0, 1.0, 1.0)
        xpos 20
        ypos 20
        droppable False

        frame:
            background "#000000fc"
            padding adjustable((20, 20, 20, 20))

            vbox:
                use SSSSS_SettingsLoadSaveScreens(update_at_runtime=True)

                use sssss_iconButton("\ue5c4", text="Return to the settings", action=[Hide("SSSSS_SettingsLoadSaveScreensStandalone"), Show("SSSSS_Settings")])
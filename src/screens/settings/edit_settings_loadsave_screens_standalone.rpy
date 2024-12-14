screen URPS_SettingsLoadSaveScreensStandalone():
    layer "URPS_Overlay"
    style_prefix "URPS"

    drag:
        draggable True
        drag_handle (0, 0, 1.0, 1.0)
        xpos 20
        ypos 20
        droppable False

        frame:
            background "#000000fc"
            padding URPS.adjustable((20, 20, 20, 20))

            vbox:
                use URPS_SettingsLoadSaveScreens(update_at_runtime=True)

                use URPS_IconButton("\ue5c4", text="Return to the settings", action=[Hide("URPS_SettingsLoadSaveScreensStandalone"), Show("URPS_Settings")])
screen JK_SettingsLoadSaveScreensStandalone():
    layer "JK_Overlay"
    style_prefix "JK"

    drag:
        draggable True
        drag_handle (0, 0, 1.0, 1.0)
        xpos 20
        ypos 20
        droppable False

        frame style "JK_default":
            background "#f00"
            padding (2, 2, 2, 2)

            frame style "JK_default":
                background "#000"
                padding (10, 10, 10, 10)

                vbox:
                    use JK_SettingsLoadSaveScreens(update_at_runtime=True)

                    use JK_IconButton("\ue5c4", text="Return to the settings", action=[Hide("JK_SettingsLoadSaveScreensStandalone"), Show("JK_Settings", section="SAVE_LOAD")])
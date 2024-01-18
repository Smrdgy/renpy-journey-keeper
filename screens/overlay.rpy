screen SSSSS_Overlay():
    layer "SSSSSoverlay"

    button:
        xfill True
        yfill True

        # key "mousedown_1" action SSSSS.Autosaver.HandlePress()
        key "mousedown_1" action SSSSS.Autosaver.HandlePress(gui.file_slot_cols * gui.file_slot_rows)
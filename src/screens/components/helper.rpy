screen URPS_Helper(message, title=None, icon=None, interactive=False):
    use URPS_Tooltip(message=message, title=title, icon=icon, interactive=interactive):
        use URPS_Icon("\ue0c6", color=URPS.Colors.text_light, hover_color=URPS.Colors.info)
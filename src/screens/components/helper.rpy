screen JK_Helper(message, title=None, icon=None, interactive=False):
    use JK_Tooltip(message=message, title=title, icon=icon, interactive=interactive):
        use JK_Icon("\ue0c6", color=JK.Colors.text_light, hover_color=JK.Colors.info)
screen JK_Helper(message, title=None, icon=None, interactive=False, side=None, disabled=False):
    python:
        _icon_color = JK.Colors.disabled if disabled else JK.Colors.text_light
        _icon_hover_color = JK.Colors.disabled if disabled else JK.Colors.info

    use JK_Tooltip(message=message, title=title, icon=icon, interactive=interactive, side=side, disabled=disabled):
        use JK_Icon("\ue0c6", color=_icon_color, hover_color=_icon_hover_color)
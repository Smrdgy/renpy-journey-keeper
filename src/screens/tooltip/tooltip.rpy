screen JK_Tooltip(message, title=None, icon=None, interactive=False, default_button_style=False, side=None):
    python:        
        open_action = JK.OpenTooltipAction(title=title, icon=icon, message=message, interactive=interactive, side=side)

    button:
        action (open_action if interactive else NullAction())
        hovered (None if interactive else open_action)
        unhovered (None if interactive else Hide("JK_TooltipDialog"))

        key_events True

        if default_button_style:
            style "JK_default"

        transclude
screen SSSSS_Tooltip(message, title=None, icon=None, interactive=False, default_button_style=False):
    python:        
        open_action = SSSSS.OpenTooltipAction(title=title, icon=icon, message=message, interactive=interactive)

    button:
        action (open_action if interactive else NullAction())
        hovered (None if interactive else open_action)
        unhovered (None if interactive else Hide("SSSSS_TooltipDialog"))

        key_events True

        if default_button_style:
            style "SSSSS_default"

        transclude
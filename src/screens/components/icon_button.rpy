screen sssss_iconButton(icon, text=None, action=None, size=None, sensitive=None, tt=None, ttSide="top", toggled=False, toggledIcon=None, disabled=False, color=None, textColor=None, iconColor=None, toggledColor=None, hovered=None, unhovered=None, hover_color=None, disabled_color=SSSSS.Colors.disabled):
    style_prefix "SSSSS"

    python:
        text_color = (disabled_color if disabled else ((toggledColor or textColor or color) if toggled else (textColor or color)))
        icon_color = (disabled_color if disabled else ((toggledColor or iconColor or color) if toggled else (iconColor or color)))
        toggled_icon = toggledIcon or icon

    # fixed:
    #     fit_first True

    button:
        sensitive sensitive
        key_events True

        hovered [SSSSS.OpenTooltipAction(message=tt, side=ttSide), hovered]
        unhovered [Hide("SSSSS_TooltipDialog"), unhovered]
        selected toggled

        if(not disabled):
            action [Hide("SSSSS_TooltipDialog"), action]

        hbox:
            style_prefix "SSSSS_icon_button"

            use sssss_icon(toggled_icon if toggled else icon, color=icon_color, size=size, hover_color=hover_color)

            if text:
                text text yalign .5:
                    if text_color:
                        color text_color
                    if size:
                        size adjustable(size)
                    if hover_color:
                        hover_color hover_color

            transclude
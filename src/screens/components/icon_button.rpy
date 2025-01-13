screen JK_IconButton(icon=None, text=None, action=None, size=None, sensitive=None, tt=None, ttSide="top", toggled=False, toggledIcon=None, disabled=False, color=None, textColor=None, iconColor=None, toggledColor=None, hovered=None, unhovered=None, hover_color=None, disabled_color=JK.Colors.disabled, key=None):
    style_prefix "JK"

    python:
        text_color = (disabled_color if disabled else ((toggledColor or textColor or color) if toggled else (textColor or color)))
        icon_color = (disabled_color if disabled else ((toggledColor or iconColor or color) if toggled else (iconColor or color)))
        toggled_icon = toggledIcon or icon

    button:
        sensitive sensitive
        key_events True

        hovered [JK.OpenTooltipAction(message=tt, side=ttSide), hovered]
        unhovered [Hide("JK_TooltipDialog"), unhovered]
        selected toggled

        if(not disabled):
            action [Hide("JK_TooltipDialog"), action]

        hbox:
            style_prefix "JK_Icon_button"

            if key:
                key key action [Hide("JK_TooltipDialog"), action]

            use JK_Icon(toggled_icon if toggled else icon, color=icon_color, size=size, hover_color=hover_color)

            if text:
                python:
                    if key:
                        text = JK.Utils.add_key_underline(text, key)

                text text yalign .5:
                    if text_color:
                        color text_color
                    if size:
                        size JK.adjustable(size)
                    if hover_color:
                        hover_color hover_color

            transclude
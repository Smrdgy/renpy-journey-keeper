screen JK_IconButton(icon=None, text=None, action=None, size=None, tt=None, tt_side="top", tt_preferred_axis=None, toggled=False, toggled_icon=None, disabled=False, color=None, text_color=None, icon_color=None, toggled_color=None, hovered=None, unhovered=None, hover_color=None, disabled_color=JK.Colors.disabled, key=None, spacing=None, outlines=None):
    style_prefix "JK"

    python:
        text_color = (disabled_color if disabled else ((toggled_color or text_color or color) if toggled else (text_color or color)))
        icon_color = (disabled_color if disabled else ((toggled_color or icon_color or color) if toggled else (icon_color or color)))
        toggled_icon = toggled_icon or icon

    button:
        sensitive not disabled
        key_events True

        hovered [JK.OpenTooltipAction(message=tt, side=tt_side, preferred_axis=tt_preferred_axis), hovered]
        unhovered [Hide("JK_TooltipDialog"), unhovered]
        selected toggled
        action [Hide("JK_TooltipDialog"), action]

        hbox:
            style_prefix "JK_Icon_button"

            if key and not disabled:
                key key action [Hide("JK_TooltipDialog"), action]

            if spacing:
                spacing spacing

            use JK_Icon(toggled_icon if toggled else icon, color=icon_color, size=size, hover_color=hover_color, outlines=outlines)

            if text:
                python:
                    if key:
                        text = JK.Utils.add_key_underline(text, key)

                text text yalign .5:
                    if text_color:
                        color text_color
                    if size:
                        size JK.scaled(size)
                    if hover_color:
                        hover_color hover_color
                    if outlines:
                        outlines outlines

            transclude
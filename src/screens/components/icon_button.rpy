screen sssss_iconButton(icon, text=None, action=None, size=None, sensitive=None, tt=None, ttSide="top", toggled=False, toggledIcon=None, disabled=False, color=None, textColor=None, iconColor=None, toggledColor=None):
    style_prefix "SSSSS"

    python:
        text_color = (SSSSS.Colors.disabled if disabled else ((toggledColor or textColor or color) if toggled else (textColor or color)))
        icon_color = (SSSSS.Colors.disabled if disabled else ((toggledColor or iconColor or color) if toggled else (iconColor or color)))
        toggled_icon = toggledIcon or icon

    # fixed:
    #     fit_first True

    button:
        sensitive sensitive
        tooltip tt
        key_events True

        selected toggled

        if(not disabled):
            action action

        hbox:
            style_prefix "SSSSS_icon_button"

            use sssss_icon(toggled_icon if toggled else icon, color=icon_color, size=size)

            if text:
                text text yalign .5:
                    if text_color:
                        color text_color
                    if size:
                        size adjustable(size)

            transclude

        # if(tt):
        #     $ tooltip = GetTooltip()

        #     if tooltip:
        #         use sssss_tooltip(text=tooltip, side=ttSide)
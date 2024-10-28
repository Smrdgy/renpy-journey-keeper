screen sssss_iconButton(icon, text=None, action=None, size=None, sensitive=None, tt=None, ttSide="top", toggled=False, toggledIcon=icon, disabled=False, color=None, textColor=None, iconColor=None):
    style_prefix "SSSSS"

    python:
        text_color = ('#2f2f2f55' if disabled else (textColor or color))
        icon_color = ('#2f2f2f55' if disabled else (iconColor or color))

    # fixed:
    #     fit_first True

    button:
        sensitive sensitive
        tooltip tt
        key_events True

        if(not disabled):
            action action

        hbox:
            style_prefix "SSSSS_icon_button"

            use sssss_icon(toggledIcon if toggled else icon, color=icon_color, size=size)

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
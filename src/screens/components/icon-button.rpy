screen sssss_iconButton(icon, text=None, action=None, size=None, sensitive=None, tt=None, ttSide="top", toggled=False, toggledIcon=icon, disabled=False, color=None, textColor=None, iconColor=None):
    style_prefix "SSSSS"

    python:
        text_color = ('#1f1f1f55' if disabled else (textColor or color or '#ffffff'))
        icon_color = ('#1f1f1f55' if disabled else (iconColor or color or '#ffffff'))

    fixed:
        fit_first True

        button:
            sensitive sensitive
            tooltip tt
            key_events True

            if(not disabled):
                action action

            hbox:
                use sssss_icon(toggledIcon if toggled else icon, color=icon_color, size=size)

                if text:
                    text text yalign .5 color text_color:
                        if size:
                            size size

        # if(tt):
        #     $ tooltip = GetTooltip()

        #     if tooltip:
        #         use sssss_tooltip(text=tooltip, side=ttSide)
screen sssss_iconButton(icon, text=None, action=None, xsize=None, sensitive=None, tt=None, ttSide="top", toggled=False, toggledIcon=icon, disabled=False, textColor=None):
    style_prefix "SSSSS"

    python:
        text_color = ('#1f1f1f55' if disabled else (textColor or '#ffffff'))

    fixed:
        fit_first True

        button:
            xsize xsize
            sensitive sensitive
            tooltip tt
            key_events True

            if(not disabled):
                action action

            hbox:
                use sssss_icon(toggledIcon if toggled else icon, color=text_color)

                if text:
                    text text yalign .5 color text_color

        # if(tt):
        #     $ tooltip = GetTooltip()

        #     if tooltip:
        #         use sssss_tooltip(text=tooltip, side=ttSide)
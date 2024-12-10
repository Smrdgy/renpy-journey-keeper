screen URPS_Radio(checked, text, action=None, xsize=None, sensitive=None, disabled=False, color=None, iconColor=None, textColor=None):
    style_prefix 'URPS_radio'

    python:
        icon_color = URPS.Colors.disabled if disabled else (iconColor or color)
        text_color = URPS.Colors.disabled if disabled else (textColor or color)

    button:
        xsize xsize
        sensitive sensitive
        action (None if disabled else action)

        hbox:
            if checked:
                use URPS_Icon("\ue837", color=icon_color)
            else:
                use URPS_Icon("\ue836", color=icon_color)
            
            if text:
                text text yalign .5:
                    if text_color:
                        color text_color
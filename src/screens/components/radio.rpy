screen JK_Radio(checked, text, action=None, xsize=None, disabled=False, color=None, icon_color=None, text_color=None):
    style_prefix 'JK_radio'

    python:
        icon_color = JK.Colors.disabled if disabled else (icon_color or color)
        text_color = JK.Colors.disabled if disabled else (text_color or color)

    button:
        xsize xsize
        sensitive not disabled
        action action

        hbox:
            if checked:
                use JK_Icon("\ue837", color=icon_color)
            else:
                use JK_Icon("\ue836", color=icon_color)
            
            if text:
                text text yalign .5:
                    if text_color:
                        color text_color
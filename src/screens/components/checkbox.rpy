screen JK_Checkbox(checked=False, text=None, action=None, xsize=None, disabled=False, color=None, icon_color=None, text_color=None, size=None):
    style_prefix 'JK_checkbox'

    python:
        icon_color = JK.Colors.disabled if disabled else (icon_color or color)
        text_color = JK.Colors.disabled if disabled else (text_color or color)

    button:
        xsize xsize
        sensitive not disabled
        action action

        hbox:
            if checked:
                use JK_Icon("\ue834", color=icon_color, size=size)
            elif checked == None:
                use JK_Icon("\ue909", size=size) #Indetermined
            else:
                use JK_Icon("\ue835", color=icon_color, size=size)
            
            if text:
                text text yalign .5:
                    if text_color:
                        color text_color
                    if size:
                        size size
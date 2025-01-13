screen JK_Checkbox(checked, text, action=None, xsize=None, sensitive=None, disabled=False, color=None, iconColor=None, textColor=None):
    style_prefix 'JK_checkbox'

    python:
        icon_color = JK.Colors.disabled if disabled else (iconColor or color)
        text_color = JK.Colors.disabled if disabled else (textColor or color)

    button:
        xsize xsize
        sensitive sensitive
        action (None if disabled else action)

        hbox:
            if checked:
                use JK_Icon("\ue834", color=icon_color)
            elif checked == None:
                use JK_Icon("\ue909") #Indetermined
            else:
                use JK_Icon("\ue835", color=icon_color)
            
            if text:
                text text yalign .5:
                    if text_color:
                        color text_color
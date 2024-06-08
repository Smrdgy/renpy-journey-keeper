screen SSSSS_Checkbox(checked, text, action=None, xsize=None, sensitive=None, disabled=False, iconColor='#ffffff', textColor = '#ffffff'):
    style_prefix 'SSSSS'

    python:
        icon_color = '#2f2f2f55' if disabled else (iconColor or color or '#ffffff')
        text_color = '#2f2f2f55' if disabled else (textColor or color or '#ffffff')

    button:
        xsize xsize
        sensitive sensitive
        action (None if disabled else action)

        hbox:
            if checked:
                use sssss_icon("\ue834", color=icon_color)
            # elif checked == None:
            #     use sssss_icon("\ue909") #Indetermined
            else:
                use sssss_icon("\ue835", color=icon_color)
            
            if text:
                text text yalign .5 color text_color
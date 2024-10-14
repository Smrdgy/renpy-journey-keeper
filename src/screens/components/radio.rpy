screen SSSSS_Radio(checked, text, action=None, xsize=None, sensitive=None, disabled=False, iconColor='#ffffff', textColor = '#ffffff'):
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
                use sssss_icon("\ue837", color=icon_color)
            else:
                use sssss_icon("\ue836", color=icon_color)
            
            if text:
                text text yalign .5 color text_color
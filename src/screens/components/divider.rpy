screen JK_Divider(sizeX=2, sizeY=2, left_padding=3, top_padding=3, right_padding=3, bottom_padding=3):
    style_prefix 'JK'

    frame:
        xysize JK.scaled((sizeX, sizeY))
        background '#ffffff48'
        xalign 0.5
        yalign 0.5
        padding JK.scaled((left_padding, top_padding, right_padding, bottom_padding))
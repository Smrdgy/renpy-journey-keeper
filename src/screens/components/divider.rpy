screen URPS_Divider(sizeX=2, sizeY=2, left_padding=3, top_padding=3, right_padding=3, bottom_padding=3):
    style_prefix 'URPS'

    frame:
        xysize URPS.adjustable((sizeX, sizeY), minValue=1)
        background '#ffffff48'
        xalign 0.5
        padding URPS.adjustable((left_padding, top_padding, right_padding, bottom_padding), minValue=1)
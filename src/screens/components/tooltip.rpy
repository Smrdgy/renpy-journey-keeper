screen sssss_tooltip(text, side="top"):
    style_prefix 'SSSSS'

    viewport:
        frame:
            if(side == "top"):
                xalign 0.5 yalign 1
            elif(side == "left"):
                xalign 0 yalign 0.5
            elif(side == "bottom"):
                xalign 0.5 yalign 0
            elif(side == "right"):
                xalign 1 yalign 0.5

            text "[text]"

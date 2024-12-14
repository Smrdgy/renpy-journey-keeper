screen URPS_Icon(icon, color=None, hover_color=None, size=None):
    style_prefix "URPS"

    frame style "URPS_default":
        hbox:
            if icon:
                text icon style 'URPS_Icon':
                    if color:
                        color color
                    if hover_color:
                        hover_color hover_color
                    if size:
                        size URPS.adjustable(size)
            transclude
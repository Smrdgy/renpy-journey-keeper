screen sssss_icon(icon, color=None, hover_color=None, size=None):
    style_prefix "SSSSS"

    frame style "SSSSS_default":
        hbox:
            if icon:
                text icon style 'SSSSS_icon':
                    if color:
                        color color
                    if hover_color:
                        hover_color hover_color
                    if size:
                        size adjustable(size)
            transclude
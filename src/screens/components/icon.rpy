# Font paths are combined with "SSSSS/" in main.rpy's renpy.config.search_prefixes.append("SSSSS/")

style sssss_material_outlined_icon:
    font 'fonts/MaterialIconsOutlined-Regular.otf'

style sssss_material_regular_icon:
    font 'fonts/MaterialIcons-Regular.ttf'

style sssss_icon is SSSSS_text:
    font 'fonts/MaterialIconsOutlined-Regular.otf'
    hover_font 'fonts/MaterialIcons-Regular.ttf'
    size 30

screen sssss_icon(icon, color='#ffffff', size=None):
    style_prefix 'SSSSS'

    hbox xsize 5 yalign .5: # We want this size fixed, to prevent resizing on icon change
        if icon:
            text icon style 'sssss_icon' color color:
                if size:
                    size size
        transclude
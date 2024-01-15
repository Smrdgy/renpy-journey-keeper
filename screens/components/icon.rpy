style sssss_material_outlined_icon:
    font 'sssss/fonts/MaterialIconsOutlined-Regular.otf'

style sssss_material_regular_icon:
    font 'sssss/fonts/MaterialIcons-Regular.ttf'

style sssss_icon is text:
    font 'sssss/fonts/MaterialIconsOutlined-Regular.otf'
    hover_font 'sssss/fonts/MaterialIcons-Regular.ttf'

screen sssss_icon(icon):
    frame:
        background None
        padding (0, 0)

        hbox xsize 5 yalign .5: # We want this size fixed, to prevent resizing on icon change
            text icon style_suffix 'sssss_icon'
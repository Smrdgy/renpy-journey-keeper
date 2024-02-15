style SSSSS_default is default:
    background None
    hover_background None
    selected_background None
    selected_hover_background None
    insensitive_background None

    xalign .0 yalign .0
    xpadding 0 ypadding 0
    xmargin 0 ymargin 0
    spacing 0

style SSSSS_text:
    font 'fonts/BarlowCondensed-SemiBold.ttf'
    color '#ffffff'
    size x52URM.scalePxInt(24)
    text_align 0.0
    outlines [(1, '#14172820')]
    alt ''

style SSSSS_text_outlined is SSSSS_text:
    outlines [(2, '#7084e6')]

style SSSSS_label is SSSSS_default
style SSSSS_label_text is SSSSS_text:
    bold True

style SSSSS_input_frame:
    xysize (928, 55)
    background "gui/input_long.png"

style SSSSS_input_input is SSSSS_text:
    size 35
    offset (10, -5)

style SSSSS_vscrollbar:
    base_bar "#00000072"
    thumb '#fff'
    hover_thumb '#7084e6'
    xsize 18
    # base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", Borders(6, 10, 6, 10), tile=False)
    # thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", Borders(6, 10, 6, 10), tile=False)

style SSSSS_frame:
    padding (15, 15)

##################
#     DIALOG     #
##################

style SSSSS_dialog_overlay:
    xfill True
    yfill True
    background '#000000aa'

style SSSSS_dialog_frame:
    align (0.5, 0.5)
    xysize (x52URM.scalePxInt(800), x52URM.scalePxInt(600))
    background '#f00' #Debug value, this will be overridden per dialog

style SSSSS_dialog_title:
    padding (40, 40, 40, 0)
    xfill True

style SSSSS_dialog_close_frame:
    background None
    align (1, 0)
    xysize (128, 128)
    offset (-60, -60)

style SSSSS_dialog_close_button:
    background "gui/dialog/dialog_close_background.png"
    xysize (128, 128)
    align (0.5, 0.5)

style SSSSS_dialog_close_inner:
    background "gui/dialog/dialog_close_foreground.png"
    hover_background "gui/dialog/dialog_close_foreground_hover.png"
    xysize (64, 64)
    hover_xysize (80, 80)
    align (0.5, 0.5)

style SSSSS_dialog_content:
    padding (40, 0, 40, 40)

##################
#    CHECKBOX    #
##################

style SSSSS_checkbox_box:
    background "gui/checkbox.png"
    xysize (47, 47)

style SSSSS_checkbox_box_checked:
    background "gui/checkbox_checked.png"
    xysize (47, 47)

style SSSSS_checkbox_box_unchecked:
    background None

# style SSSSS_checkbox_box_indeterminate:
    
##################
#     BUTTON     #
##################

style SSSSS_textbutton_medium:
    xysize (237, 80)

style SSSSS_textbutton_medium_green is SSSSS_textbutton_medium:
    background "gui/button/button_green.png"

style SSSSS_textbutton_medium_red is SSSSS_textbutton_medium:
    background "gui/button/button_red.png"

style SSSSS_textbutton_medium_gray is SSSSS_textbutton_medium:
    background "gui/button/button_gray.png"
    
style SSSSS_pagination_textbutton:
    background None
    offset (0, -5)

style SSSSS_pagination_textbutton_text is SSSSS_text:
    color '#cdcdcd'
    hover_color '#ffffff'
    size 40
    text_align 0.5

style SSSSS_pagination_textbutton_active is SSSSS_pagination_textbutton

style SSSSS_pagination_textbutton_active_text is SSSSS_pagination_textbutton_text:
    color '#abe9ff'
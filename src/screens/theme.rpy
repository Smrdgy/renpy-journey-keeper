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

    outlines []

style SSSSS_text is SSSSS_default:
    color '#ffffff'
    size 20
    text_align 0.0
    outlines []
    alt ''
    font 'DejaVuSans.ttf'

style SSSSS_label is SSSSS_default
style SSSSS_label_text is SSSSS_text:
    bold True

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

style SSSSS_frame is SSSSS_default:
    padding (15, 15)

style SSSSS_vbox is SSSSS_default
style SSSSS_hbox is SSSSS_default

##################
#     DIALOG     #
##################

style SSSSS_dialog_overlay:
    xfill True
    yfill True
    background '#000000ff'

style SSSSS_dialog_title:
    padding (40, 40, 40, 0)
    xfill True

style SSSSS_dialog_content:
    padding (40, 0, 40, 40)
   
##################
#     BUTTON     #
##################

style SSSSS_button is SSSSS_default:
    padding (5, 5)
   
style SSSSS_pagination_textbutton:
    background None
    yalign 0.5

style SSSSS_pagination_textbutton_text is SSSSS_text:
    color '#cdcdcd'
    hover_color '#ffffff'
    size 25
    text_align 0.5

style SSSSS_pagination_textbutton_active is SSSSS_pagination_textbutton

style SSSSS_pagination_textbutton_active_text is SSSSS_pagination_textbutton_text:
    color '#abe9ff'
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
    color SSSSS.Colors.text_primary
    size adjustable(20)
    text_align 0.0
    outlines []
    alt ''
    font 'DejaVuSans.ttf'

style SSSSS_label is SSSSS_default
style SSSSS_label_text is SSSSS_text:
    bold True

style SSSSS_placeholder is SSSSS_text:
    color SSSSS.Colors.text_placeholder

style textinput is SSSSS_text:
    color "#959595"
    offset adjustable((10, 1), minValue=1)

style SSSSS_vscrollbar:
    base_bar "#00000072"
    thumb '#fff'
    hover_thumb SSSSS.Colors.hover
    xsize adjustable(18)
    # base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", Borders(6, 10, 6, 10), tile=False)
    # thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", Borders(6, 10, 6, 10), tile=False)

style SSSSS_frame is SSSSS_default:
    padding adjustable((15, 15), minValue=1)

style SSSSS_vbox is SSSSS_default
style SSSSS_hbox is SSSSS_default

##################
#     DIALOG     #
##################

style SSSSS_dialog_overlay:
    xfill True
    yfill True
    background '#000000ff'

style SSSSS_dialog_title is SSSSS_text:
    padding adjustable((40, 40, 40, 0), minValue=1)
    size adjustable(40)
    xfill True

style SSSSS_dialog_content:
    padding adjustable((40, 0, 40, 40), minValue=1)
   
style SSSSS_dialog_vbox is SSSSS_vbox
style SSSSS_dialog_hbox is SSSSS_hbox
style SSSSS_dialog_frame is SSSSS_frame
style SSSSS_dialog_text is SSSSS_text
style SSSSS_dialog_label is SSSSS_label
style SSSSS_dialog_label_text is SSSSS_label_text
style SSSSS_dialog_button is SSSSS_button

# Action buttons

style SSSSS_dialog_action_buttons_vbox is SSSSS_vbox:
    # "at right" @see 00definitions.rpy
    xpos 1.0
    xanchor 1.0
    ypos 1.0
    yanchor 1.0

    yalign 1.0

style SSSSS_dialog_action_buttons_hbox is SSSSS_hbox:
    # "at right" @see 00definitions.rpy
    xpos 1.0
    xanchor 1.0
    ypos 1.0
    yanchor 1.0

##################
#     BUTTON     #
##################

style SSSSS_button is SSSSS_default:
    padding adjustable((5, 5), minValue=1)

style SSSSS_icon_button is SSSSS_button

style SSSSS_icon_button_text is SSSSS_text:
    hover_color SSSSS.Colors.hover

style SSSSS_checkbox is SSSSS_button
style SSSSS_checkbox_text is SSSSS_icon_button_text
style SSSSS_checkbox_button is SSSSS_button

style SSSSS_radio is SSSSS_button
style SSSSS_radio_text is SSSSS_icon_button_text
style SSSSS_radio_button is SSSSS_button
   
style SSSSS_pagination_textbutton:
    background None
    yalign 0.5

style SSSSS_pagination_textbutton_text is SSSSS_text:
    color '#cdcdcd'
    hover_color SSSSS.Colors.hover
    size adjustable(25)
    text_align 0.5

style SSSSS_pagination_textbutton_active is SSSSS_pagination_textbutton

style SSSSS_pagination_textbutton_active_text is SSSSS_pagination_textbutton_text:
    color SSSSS.Colors.selected
    hover_color SSSSS.Colors.hover

style SSSSS_row_button is SSSSS_button:
    selected_background SSSSS.Colors.selected_background
    hover_background SSSSS.Colors.block_hover_background
    selected_hover_background SSSSS.Colors.block_selected_hover_background

style SSSSS_row_odd_button is SSSSS_row_button:
    background SSSSS.Colors.block_background
    selected_background SSSSS.Colors.selected_background
    hover_background SSSSS.Colors.block_hover_background
    selected_hover_background SSSSS.Colors.block_selected_hover_background

style SSSSS_playthrough_button is SSSSS_button:
    background SSSSS.Colors.block_background
    hover_background SSSSS.Colors.block_hover_background
    selected_background SSSSS.Colors.selected_background
    selected_hover_background SSSSS.Colors.block_selected_hover_background

##################
#      INPUT     #
##################

style keyinput is SSSSS_button:
    background "#ffffff22"
    xminimum adjustable(100)

style keyinput_text is SSSSS_text:
    size adjustable(25)
    color SSSSS.Colors.theme

style keyinput_text_placeholder is keyinput_text:
    color "#ccc"

style keyinput_disabled is keyinput:
    background "#0e0e0e"

style keyinput_disabled_text is keyinput_text:
    color SSSSS.Colors.disabled

style keyinput_disabled_text_placeholder is keyinput_text_placeholder:
    color SSSSS.Colors.disabled

##################
#      ICONS     #
##################

style SSSSS_material_outlined_icon:
    font 'fonts/MaterialIconsOutlined-Regular.otf'

style SSSSS_material_regular_icon:
    font 'fonts/MaterialIcons-Regular.ttf'

style SSSSS_icon is SSSSS_text:
    font 'fonts/MaterialIconsOutlined-Regular.otf'
    hover_font 'fonts/MaterialIcons-Regular.ttf'
    hover_color SSSSS.Colors.hover
    size adjustable(30)

##################
#     Titles     #
##################

style SSSSS_title is SSSSS_text:
    color SSSSS.Colors.theme

style SSSSS_title_1 is SSSSS_title:
    size adjustable(30)
    bold True

style SSSSS_title_2 is SSSSS_title:
    size adjustable(25)

style SSSSS_spacer_x_1:
    xsize adjustable(20)

style SSSSS_spacer_x_2:
    xsize adjustable(20)

style SSSSS_spacer_x_3:
    xsize adjustable(10)

style SSSSS_spacer_y_1:
    ysize adjustable(40)

style SSSSS_spacer_y_2:
    ysize adjustable(20)

style SSSSS_spacer_y_3:
    ysize adjustable(10)

##################
#     Toolbar    #
##################

style SSSSS_toolbar:
    padding adjustable((20, 0, 20, 0))

style SSSSS_toolbar_active is SSSSS_toolbar:
    background "#2b4047"
style URPS_default is default:
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

style URPS_text is URPS_default:
    color URPS.Colors.text_primary
    size URPS.adjustable(20)
    text_align 0.0
    outlines []
    alt ''
    font 'DejaVuSans.ttf'

style URPS_label is URPS_default
style URPS_label_text is URPS_text:
    bold True

style textinput is URPS_text:
    color "#959595"
    offset URPS.adjustable((10, 1), minValue=1)

style textinput_caret is textinput

style URPS_vscrollbar:
    base_bar "#00000072"
    thumb '#fff'
    hover_thumb URPS.Colors.hover
    xsize URPS.adjustable(18)
    # base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", Borders(6, 10, 6, 10), tile=False)
    # thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", Borders(6, 10, 6, 10), tile=False)

style URPS_frame is URPS_default:
    padding URPS.adjustable((15, 15), minValue=1)

style URPS_vbox is URPS_default
style URPS_hbox is URPS_default

##################
#     DIALOG     #
##################

style URPS_dialog_overlay:
    xfill True
    yfill True
    background '#000000ff'

style URPS_dialog_title is URPS_text:
    padding URPS.adjustable((40, 40, 40, 0), minValue=1)
    size URPS.adjustable(40)
    xfill True

style URPS_dialog_content:
    padding URPS.adjustable((40, 0, 40, 40), minValue=1)
   
style URPS_dialog_vbox is URPS_vbox
style URPS_dialog_hbox is URPS_hbox
style URPS_dialog_frame is URPS_frame
style URPS_dialog_text is URPS_text
style URPS_dialog_label is URPS_label
style URPS_dialog_label_text is URPS_label_text
style URPS_dialog_button is URPS_button

# Action buttons

style URPS_dialog_action_buttons_vbox is URPS_vbox:
    # "at right" @see 00definitions.rpy
    xpos 1.0
    xanchor 1.0
    ypos 1.0
    yanchor 1.0

    yalign 1.0

style URPS_dialog_action_buttons_hbox is URPS_hbox:
    # "at right" @see 00definitions.rpy
    xpos 1.0
    xanchor 1.0
    ypos 1.0
    yanchor 1.0

##################
#     BUTTON     #
##################

style URPS_button is URPS_default:
    padding URPS.adjustable((5, 5), minValue=1)

style URPS_Icon_button is URPS_button

style URPS_Icon_button_text is URPS_text:
    hover_color URPS.Colors.hover

style URPS_checkbox is URPS_button
style URPS_checkbox_text is URPS_Icon_button_text
style URPS_checkbox_button is URPS_button

style URPS_radio is URPS_button
style URPS_radio_text is URPS_Icon_button_text
style URPS_radio_button is URPS_button
   
style URPS_pagination_textbutton:
    background None
    yalign 0.5

style URPS_pagination_textbutton_text is URPS_text:
    color '#cdcdcd'
    hover_color URPS.Colors.hover
    size URPS.adjustable(25)
    text_align 0.5

style URPS_pagination_textbutton_active is URPS_pagination_textbutton

style URPS_pagination_textbutton_active_text is URPS_pagination_textbutton_text:
    color URPS.Colors.selected
    hover_color URPS.Colors.hover

style URPS_row_button is URPS_button:
    selected_background URPS.Colors.selected_background
    hover_background URPS.Colors.block_hover_background
    selected_hover_background URPS.Colors.block_selected_hover_background

style URPS_row_odd_button is URPS_row_button:
    background URPS.Colors.block_background
    selected_background URPS.Colors.selected_background
    hover_background URPS.Colors.block_hover_background
    selected_hover_background URPS.Colors.block_selected_hover_background

style URPS_playthrough_button is URPS_button:
    background URPS.Colors.block_background
    hover_background URPS.Colors.block_hover_background
    selected_background URPS.Colors.selected_background
    selected_hover_background URPS.Colors.block_selected_hover_background

##################
#      INPUT     #
##################

style keyinput is URPS_button:
    background "#ffffff22"
    xminimum URPS.adjustable(100)

style keyinput_text is URPS_text:
    size URPS.adjustable(25)
    color URPS.Colors.theme

style keyinput_text_placeholder is keyinput_text:
    color "#ccc"

style keyinput_disabled is keyinput:
    background "#0e0e0e"

style keyinput_disabled_text is keyinput_text:
    color URPS.Colors.disabled

style keyinput_disabled_text_placeholder is keyinput_text_placeholder:
    color URPS.Colors.disabled

##################
#      ICONS     #
##################

style URPS_material_outlined_icon:
    font 'fonts/MaterialIconsOutlined-Regular.otf'

style URPS_material_regular_icon:
    font 'fonts/MaterialIcons-Regular.ttf'

style URPS_Icon is URPS_text:
    font 'fonts/MaterialIconsOutlined-Regular.otf'
    hover_font 'fonts/MaterialIcons-Regular.ttf'
    hover_color URPS.Colors.hover
    size URPS.adjustable(30)

##################
#     Titles     #
##################

style URPS_title is URPS_text:
    color URPS.Colors.theme

style URPS_title_1 is URPS_title:
    size URPS.adjustable(30)
    bold True

style URPS_title_2 is URPS_title:
    size URPS.adjustable(25)

style URPS_title_3 is URPS_title:
    size URPS.adjustable(20)

style URPS_spacer_x_1:
    xsize URPS.adjustable(20)

style URPS_spacer_x_2:
    xsize URPS.adjustable(20)

style URPS_spacer_x_3:
    xsize URPS.adjustable(10)

style URPS_spacer_y_1:
    ysize URPS.adjustable(40)

style URPS_spacer_y_2:
    ysize URPS.adjustable(20)

style URPS_spacer_y_3:
    ysize URPS.adjustable(10)

##################
#     Toolbar    #
##################

style URPS_toolbar:
    padding URPS.adjustable((20, 0, 20, 0))

style URPS_toolbar_active is URPS_toolbar:
    background "#2b4047"
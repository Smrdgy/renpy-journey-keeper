style JK_default is default:
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

style JK_text is JK_default:
    color JK.Colors.text_primary
    size JK.adjustable(20)
    text_align 0.0
    outlines []
    alt ''
    font 'DejaVuSans.ttf'

style JK_label is JK_default
style JK_label_text is JK_text:
    bold True

style textinput is JK_text:
    color "#959595"
    offset JK.adjustable((10, 1), minValue=1)

style textinput_caret is textinput

style JK_vscrollbar:
    base_bar "#00000072"
    thumb '#fff'
    hover_thumb JK.Colors.hover
    xsize JK.adjustable(18)
    # base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", Borders(6, 10, 6, 10), tile=False)
    # thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", Borders(6, 10, 6, 10), tile=False)

style JK_frame is JK_default:
    padding JK.adjustable((15, 15), minValue=1)

style JK_vbox is JK_default
style JK_hbox is JK_default

##################
#     DIALOG     #
##################

style JK_dialog_overlay:
    xfill True
    yfill True
    background '#000000ff'

style JK_dialog_title is JK_text:
    padding JK.adjustable((40, 40, 40, 0), minValue=1)
    size JK.adjustable(40)
    xfill True

style JK_dialog_content:
    padding JK.adjustable((40, 0, 40, 40), minValue=1)
   
style JK_dialog_vbox is JK_vbox
style JK_dialog_hbox is JK_hbox
style JK_dialog_frame is JK_frame
style JK_dialog_text is JK_text
style JK_dialog_label is JK_label
style JK_dialog_label_text is JK_label_text
style JK_dialog_button is JK_button

# Action buttons

style JK_dialog_action_buttons_vbox is JK_vbox:
    # "at right" @see 00definitions.rpy
    xpos 1.0
    xanchor 1.0
    ypos 1.0
    yanchor 1.0

    yalign 1.0

style JK_dialog_action_buttons_hbox is JK_hbox:
    # "at right" @see 00definitions.rpy
    xpos 1.0
    xanchor 1.0
    ypos 1.0
    yanchor 1.0

##################
#     BUTTON     #
##################

style JK_button is JK_default:
    padding JK.adjustable((5, 5), minValue=1)

style JK_Icon_button is JK_button

style JK_Icon_button_text is JK_text:
    hover_color JK.Colors.hover

style JK_checkbox is JK_button
style JK_checkbox_text is JK_Icon_button_text
style JK_checkbox_button is JK_button

style JK_radio is JK_button
style JK_radio_text is JK_Icon_button_text
style JK_radio_button is JK_button
   
style JK_pagination_textbutton:
    background None
    yalign 0.5

style JK_pagination_textbutton_text is JK_text:
    color '#cdcdcd'
    hover_color JK.Colors.hover
    size JK.adjustable(25)
    text_align 0.5

style JK_pagination_textbutton_active is JK_pagination_textbutton

style JK_pagination_textbutton_active_text is JK_pagination_textbutton_text:
    color JK.Colors.selected
    hover_color JK.Colors.hover

style JK_row_button is JK_button:
    selected_background JK.Colors.selected_background
    hover_background JK.Colors.block_hover_background
    selected_hover_background JK.Colors.block_selected_hover_background

style JK_row_odd_button is JK_row_button:
    background JK.Colors.block_background
    selected_background JK.Colors.selected_background
    hover_background JK.Colors.block_hover_background
    selected_hover_background JK.Colors.block_selected_hover_background

style JK_playthrough_button is JK_button:
    background JK.Colors.block_background
    hover_background JK.Colors.block_hover_background
    selected_background JK.Colors.selected_background
    selected_hover_background JK.Colors.block_selected_hover_background

##################
#      INPUT     #
##################

style keyinput is JK_button:
    background "#ffffff22"
    xminimum JK.adjustable(100)

style keyinput_text is JK_text:
    size JK.adjustable(25)
    color JK.Colors.theme

style keyinput_text_placeholder is keyinput_text:
    color "#ccc"

style keyinput_disabled is keyinput:
    background "#0e0e0e"

style keyinput_disabled_text is keyinput_text:
    color JK.Colors.disabled

style keyinput_disabled_text_placeholder is keyinput_text_placeholder:
    color JK.Colors.disabled

##################
#      ICONS     #
##################

style JK_material_outlined_icon:
    font 'fonts/MaterialIconsOutlined-Regular.otf'

style JK_material_regular_icon:
    font 'fonts/MaterialIcons-Regular.ttf'

style JK_Icon is JK_text:
    font 'fonts/MaterialIconsOutlined-Regular.otf'
    hover_font 'fonts/MaterialIcons-Regular.ttf'
    hover_color JK.Colors.hover
    size JK.adjustable(30)

##################
#     Titles     #
##################

style JK_title is JK_text:
    color JK.Colors.theme

style JK_title_1 is JK_title:
    size JK.adjustable(30)
    bold True

style JK_title_2 is JK_title:
    size JK.adjustable(25)

style JK_title_3 is JK_title:
    size JK.adjustable(20)

style JK_spacer_x_1:
    xsize JK.adjustable(20)

style JK_spacer_x_2:
    xsize JK.adjustable(20)

style JK_spacer_x_3:
    xsize JK.adjustable(10)

style JK_spacer_y_1:
    ysize JK.adjustable(40)

style JK_spacer_y_2:
    ysize JK.adjustable(20)

style JK_spacer_y_3:
    ysize JK.adjustable(10)

##################
#     Toolbar    #
##################

style JK_toolbar:
    padding JK.adjustable((20, 0, 20, 0))

style JK_toolbar_active is JK_toolbar:
    background "#2b4047"
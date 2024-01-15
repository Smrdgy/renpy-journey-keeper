style sssss_icon_button is button
style sssss_icon_button_text is text:
    font 'sssss/fonts/MaterialIconsOutlined-Regular.otf'
    hover_font 'sssss/fonts/MaterialIcons-Regular.ttf'

screen sssss_iconButton(icon, text=None, action=None, xsize=None, sensitive=None, tt=None, ttSide="top", toggled=False, toggledIcon=icon):
    fixed:
        fit_first True

        button:
            xsize xsize
            sensitive sensitive
            action action
            tooltip tt

            if text: # It's a button with text?
                hbox:
                    use sssss_icon(toggledIcon if toggled else icon)

                    if text:
                        text text style_suffix 'sssss_button_text' yalign .5
            else: # Icon only button
                use sssss_icon(toggledIcon if toggled else icon)

        # if(tt):
        #     $ tooltip = GetTooltip()

        #     if tooltip:
        #         use sssss_tooltip(text=tooltip, side=ttSide)
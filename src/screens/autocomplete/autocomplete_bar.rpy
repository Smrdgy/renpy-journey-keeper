screen JK_AutocompleteBar():
    layer "JK_Autocomplete"
    style_prefix "JK"

    timer 0.2 repeat True action JK.Autocomplete.TickAction()

    python:
        if JK.Autocomplete.loading:
            status_text = "Loading choices..."
            status_color = JK.Colors.theme
        elif JK.Autocomplete.paused:
            status_text = "Paused"
            status_color = JK.Colors.warning
        elif JK.Utils.is_save_load_screen():
            status_text = "Waiting for you to return to the game..."
            status_color = JK.Colors.info
        else:
            status_text = "Autocompleting..."
            status_color = JK.Colors.theme

        if JK.Autocomplete.cursor < len(JK.Autocomplete.choices):
            upcoming_text = JK.Utils.escape_renpy_reserved_characters(JK.Autocomplete.choices[JK.Autocomplete.cursor])
            if len(upcoming_text) > 20:
                upcoming_text = upcoming_text[:20] + "..."
        else:
            upcoming_text = "(end of list)"

    frame:
        xfill True
        xpos 0
        ypos 0
        background "#000000cc"
        padding JK.scaled((15, 10))

        hbox:
            xfill True
            yalign 0.5
            spacing JK.scaled(15)

            hbox yalign 0.5:
                text status_text style "JK_text" color status_color yalign 0.5

                if JK.Autocomplete.pause_reason:
                    use JK_Helper(message=JK.Autocomplete.pause_reason)

            hbox:
                xalign 1.0
                yalign 0.5
                spacing JK.scaled(10)

                use JK_IconButton(icon=JK.Autocomplete.ICON_UPCOMING, text=upcoming_text, action=Show("JK_AutocompletePicker"), tt="Upcoming choice - click to adjust")

                use JK_IconButton(icon=(JK.Autocomplete.ICON_RESUME if JK.Autocomplete.paused else JK.Autocomplete.ICON_PAUSE), text=("Resume" if JK.Autocomplete.paused else "Pause"), action=(JK.Autocomplete.ResumeAction() if JK.Autocomplete.paused else JK.Autocomplete.PauseAction()), disabled=JK.Autocomplete.loading)

                use JK_IconButton(icon=JK.Autocomplete.ICON_STOP, text="Stop", action=JK.Autocomplete.StopAction(), color=JK.Colors.danger)

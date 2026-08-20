screen JK_AutocompletePicker():
    layer "JK_Overlay"
    style_prefix "JK"
    modal True
    zorder 155

    default choices_vlist = JK.VirtualListState()

    python:
        choices = JK.Autocomplete.choices
        row_height = JK.scaled(50)

    use JK_Dialog(title="Upcoming choices", close_action=Hide("JK_AutocompletePicker")):
        if choices:
            python:
                viewport_size = choices_vlist.estimate_viewport_size(renpy.config.screen_height)
                window_start, window_end, top_spacer, bottom_spacer = choices_vlist.compute(len(choices), row_height, viewport_size)
                windowed_choices = list(enumerate(choices))[window_start:window_end]

            viewport:
                mousewheel True
                draggable True
                scrollbars "vertical"
                vscrollbar_unscrollable "hide"
                pagekeys True
                ymaximum 0.75
                yadjustment choices_vlist.adjustment

                vbox:
                    null height top_spacer

                    for index, choice_text in windowed_choices:
                        $ is_cursor = index == JK.Autocomplete.cursor
                        $ display_number = index + 1

                        button:
                            ysize row_height
                            style ("JK_row_button" if index % 2 == 0 else "JK_row_odd_button")
                            selected is_cursor
                            action [JK.Autocomplete.SetCursorAction(index), Hide("JK_AutocompletePicker")]

                            hbox:
                                spacing JK.scaled(10)
                                xfill True
                                yalign 0.5

                                text "[display_number]." style "JK_text" xsize JK.scaled(50) yalign 0.5

                                text JK.Utils.escape_renpy_reserved_characters(choice_text) style "JK_text" yalign 0.5

                                hbox:
                                    xalign 1.0
                                    yalign 0.5

                                    use JK_IconButton(icon="\ue316", tt="Move up", action=JK.Autocomplete.MoveEntryAction(index, -1), disabled=index == 0)
                                    use JK_IconButton(icon="\ue313", tt="Move down", action=JK.Autocomplete.MoveEntryAction(index, 1), disabled=index == len(choices) - 1)
                                    use JK_IconButton(icon="\ue3c9", tt="Edit", action=Show("JK_AutocompleteEditEntry", index=index, text=choice_text))
                                    use JK_IconButton(icon="\ue872", tt="Delete", action=JK.Autocomplete.DeleteEntryAction(index), color=JK.Colors.danger)

                    null height bottom_spacer
        else:
            hbox:
                xfill True
                yfill True

                hbox xalign 0.5 yalign 0.5:
                    use JK_Title("No choices yet.", color=JK.Colors.error)

        hbox:
            xfill True
            yfill True

            style_prefix "JK_dialog_action_buttons"

            vbox xalign 0.0:
                hbox:
                    use JK_IconButton(icon="\uea20", text="Add choice", action=Show("JK_AutocompleteEditEntry", index=None, text=""), key="alt_K_a")

            vbox xalign 1.0:
                hbox:
                    use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_AutocompletePicker"))


screen JK_AutocompleteEditEntry(index=None, text=""):
    layer "JK_Overlay"
    style_prefix "JK"
    modal True
    zorder 160

    default entry_text = text
    default entry_text_input = JK.TextInput("entry_text", auto_focus=True)

    if JK.TextInput.is_active("entry_text"):
        key 'K_ESCAPE' action JK.TextInput.SetActiveAction(None)

    python:
        if index is not None:
            save_action = [JK.Autocomplete.EditEntryAction(index, entry_text), Hide("JK_AutocompleteEditEntry")]
        else:
            save_action = [JK.Autocomplete.InsertEntryAction(entry_text), Hide("JK_AutocompleteEditEntry")]

    key "ctrl_K_s" action save_action

    use JK_Dialog(title=("Edit choice" if index is not None else "Add choice"), close_action=Hide("JK_AutocompleteEditEntry")):
        button:
            action entry_text_input.get_enable_action()
            key_events True

            vbox:
                add entry_text_input.displayable(placeholder="Choice text")
                frame style "JK_default" background "#ffffff22" hover_background JK.Colors.hover ysize 2 offset JK.scaled((0, 2))

        hbox:
            style_prefix "JK_dialog_action_buttons"
            xfill True
            yfill True

            vbox xalign 1.0:
                hbox:
                    use JK_IconButton(icon="\ue161", text="Save", action=save_action, color=JK.Colors.success, key="alt_K_s")

                hbox:
                    use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_AutocompleteEditEntry"))

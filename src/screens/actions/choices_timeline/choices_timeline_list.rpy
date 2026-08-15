screen JK_ChoicesTimelineList(view_model, show_thumbnails, search, choices_vlist):
    default search_input = JK.TextInput("search")

    python:
        timeline = JK.Utils.filter_timeline(view_model.timeline, search)

        current_state_text = "{color=" + JK.Colors.status_disabled + "}disabled{/color}"
        if view_model.playthrough.autosaveOnChoices:
            current_state_text = "{color=" + JK.Colors.status_enabled + "}enabled{/color}"

        choices_text = "Choices are saved into save files {u}only{/u} when this mod is active and \"Autosave on choice\" is enabled (currently [current_state_text]) in the playthrough settings.\n{color=[JK.Colors.warning]}Warning - Manual and quick saves are unable to store choices.{/c}"

        has_timeline_entry = False
        for entry in view_model.timeline:
            if entry[1] != None:
                has_timeline_entry = True

        export_action = JK.ChoicesTimelineViewModel.ExportTimelineToFileAction(view_model)

        # Fixed row pitch so windowing math is exact - rows used to auto-size
        # around the optional thumbnail image.
        row_spacing = 3 if show_thumbnails else 0
        row_height = JK.scaled(110) if show_thumbnails else JK.scaled(40)
        row_pitch = row_height + row_spacing

        # Matches the single JK_YSpacer(offset=3) placed at the top of the
        # scrollable content below.
        list_header_size = JK.scaled(10)

    if has_timeline_entry:
        key 'ctrl_K_f' action JK.TextInput.SetActiveAction("search")
        if JK.TextInput.is_active("search"):
            key 'K_ESCAPE' action JK.TextInput.SetActiveAction(None)

        # Header content, kept outside the viewport (fixed, doesn't scroll
        # with the list) so scroll-position math only has to account for the
        # list content itself.
        hbox:
            xfill True

            text choices_text xalign 0.5 text_align 0.5

        hbox:
            xalign 0.5

            use JK_IconButton('', text="Export to file", action=export_action, key="alt_K_e")

        use JK_YSpacer(offset=3)

        hbox:
            xfill True

            # Toggle thumbnails
            use JK_Checkbox(checked=show_thumbnails, text="Show thumbnails\n{size=-5}(Might be laggy or outright crash){/size}", action=SetScreenVariable("show_thumbnails", not show_thumbnails))

            # Seach box
            hbox yalign 0.0 xpos 1.0 xanchor 1.0:
                frame style "JK_frame":
                    xysize JK.scaled((300, 50))

                    button:
                        key_events True
                        action SetScreenVariable(JK.TextInput.active_text_input_screen_variable_name, "search")

                        vbox:
                            hbox:
                                hbox yalign 0.5:
                                    use JK_Icon(icon="", size=20, hover_color=JK.Colors.hover)

                                add search_input.displayable(placeholder="Search for choice")

                            frame style "JK_default" background "#ffffff22" hover_background JK.Colors.hover ysize 2 offset JK.scaled((0, 2))

                use JK_XSpacer(offset=2)

        python:
            viewport_size = choices_vlist.estimate_viewport_size(renpy.config.screen_height)
            window_start, window_end, top_spacer, bottom_spacer = choices_vlist.compute(len(timeline), row_pitch, viewport_size, list_header_size)
            windowed_timeline = timeline[window_start:window_end]

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            vscrollbar_unscrollable "hide"
            pagekeys True
            yadjustment choices_vlist.adjustment

            vbox:
                use JK_YSpacer(offset=3)

                null height top_spacer

                vbox:
                    spacing row_spacing

                    for entry in windowed_timeline:
                        $ page, slot = JK.Utils.split_slotname(entry[2])

                        button style "JK_text":
                            ysize row_height
                            action [FileLoad(slot, confirm=True, page=page), Hide("JK_ChoicesTimeline")]

                            hbox:
                                if show_thumbnails:
                                    image renpy.slot_screenshot(entry[2]) size JK.Utils.resize_dimensions_to_limits((renpy.config.thumbnail_width, renpy.config.thumbnail_height), (100, 100))

                                    use JK_XSpacer(offset=3)

                                hbox yalign 0.5:
                                    $ n = entry[0] + 1
                                    text "[n]." hover_color JK.Colors.hover:
                                        if entry[1] is None:
                                            color JK.Colors.na

                                    if entry[1] is None:
                                        text "??????" color JK.Colors.na hover_color JK.Colors.hover
                                    else:
                                        text JK.Utils.escape_renpy_reserved_characters(entry[1]) hover_color JK.Colors.hover

                                    use JK_XSpacer(offset=3)

                                    text "{size=-5}([entry[2]]){/size}" color "#4b4b4b" hover_color JK.Colors.hover yalign 0.5

                null height bottom_spacer
    else:
        vbox:
            hbox:
                xfill True

                text choices_text xalign 0.5 text_align 0.5

            hbox:
                xfill True
                yfill True

                hbox xalign 0.5 yalign 0.5:
                    use JK_Title("No choices found.", color=JK.Colors.error)

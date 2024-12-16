screen URPS_ChoicesTimelineList(viewModel, show_thumbnails, search):
    default search_input = URPS.TextInput("search")

    python:
        timeline = URPS.Utils.filter_timeline(viewModel.timeline, search)

        current_state_text = "{color=" + URPS.Colors.status_disabled + "}disabled{/color}"
        if viewModel.playthrough.autosaveOnChoices:
            current_state_text = "{color=" + URPS.Colors.status_enabled + "}enabled{/color}"

        choicesText = "Choices are saved into save files {u}only{/u} when this mod is active and \"Autosave on choice\" is enabled (currently [current_state_text]) in the playthrough settings.\n{color=[URPS.Colors.warning]}Warning - Manual and quick saves are unable to store choices.{/c}"

        hasTimelineEntry = False
        for entry in viewModel.timeline:
            if entry[1] != None:
                hasTimelineEntry = True

        exportAction = URPS.ChoicesTimelineViewModel.ExportTimelineToFile(viewModel)

    if hasTimelineEntry:
        key 'ctrl_K_f' action URPS.TextInput.SetActiveAction("search")
        if URPS.TextInput.is_active("search"):
            key 'K_ESCAPE' action URPS.TextInput.SetActiveAction(None)

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            pagekeys True

            vbox:
                hbox:
                    xfill True

                    text choicesText xalign 0.5 text_align 0.5

                hbox:
                    xalign 0.5

                    use URPS_IconButton('\uf0fb', text="Export to file", action=exportAction, key="ctrl_K_e")

                use URPS_YSpacer(offset=3)

                hbox:
                    xfill True

                    # Toggle thumbnails
                    use SmrdgyLib_Checkbox(checked=show_thumbnails, text="Show thumbnails\n{size=-5}(Might be laggy or outright crash){/size}", action=SetScreenVariable("show_thumbnails", not show_thumbnails))

                    # Seach box
                    hbox yalign 0.0 xpos 1.0 xanchor 1.0:
                        frame style "URPS_frame":
                            xysize URPS.adjustable((300, 50))

                            button:
                                key_events True
                                action SetScreenVariable(URPS.TextInput.activeTextInputScreenVariableName, "search")

                                vbox:
                                    hbox:
                                        hbox yalign 0.5:
                                            use URPS_Icon(icon="\ue8b6", size=20, hover_color=URPS.Colors.hover)

                                        add search_input.displayable(placeholder="Search for choice")

                                    frame style "URPS_default" background "#ffffff22" hover_background URPS.Colors.hover ysize 2 offset URPS.adjustable((0, 2))

                        use URPS_XSpacer(offset=2)

                use URPS_YSpacer(offset=3)

                vbox:
                    spacing (3 if show_thumbnails else 0)

                    for entry in timeline:
                        $ page, slot = SmrdgyLib.save.split_save_name(entry[2])

                        button style "URPS_text":
                            action [FileLoad(slot, confirm=True, page=page), Hide("URPS_ChoicesTimeline")]

                            hbox:
                                if show_thumbnails:
                                    image renpy.slot_screenshot(entry[2]) size URPS.Utils.SmrdgyLib.image.resize_dimensions_to_limits((renpy.config.thumbnail_width, renpy.config.thumbnail_height), (100, 100))

                                    use URPS_XSpacer(offset=3)

                                hbox yalign 0.5:
                                    $ n = entry[0] + 1
                                    text "[n]." hover_color URPS.Colors.hover:
                                        if entry[1] is None:
                                            color URPS.Colors.na

                                    if entry[1] is None:
                                        text "??????" color URPS.Colors.na hover_color URPS.Colors.hover
                                    else:
                                        text SmrdgyLib.text.replace_reserved_characters(entry[1]) hover_color URPS.Colors.hover

                                    use URPS_XSpacer(offset=3)

                                    text "([entry[2]])" size 18 color "#4b4b4b" hover_color URPS.Colors.hover
    else:
        vbox:
            hbox:
                xfill True

                text choicesText xalign 0.5 text_align 0.5

            hbox:
                xfill True
                yfill True
            
                hbox xalign 0.5 yalign 0.5:
                    use URPS_Title("No choices found.", color=URPS.Colors.error)
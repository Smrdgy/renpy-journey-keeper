screen JK_ChoicesTimelineList(viewModel, show_thumbnails, search):
    default search_input = JK.TextInput("search")

    python:
        timeline = JK.Utils.filter_timeline(viewModel.timeline, search)

        current_state_text = "{color=" + JK.Colors.status_disabled + "}disabled{/color}"
        if viewModel.playthrough.autosaveOnChoices:
            current_state_text = "{color=" + JK.Colors.status_enabled + "}enabled{/color}"

        choicesText = "Choices are saved into save files {u}only{/u} when this mod is active and \"Autosave on choice\" is enabled (currently [current_state_text]) in the playthrough settings.\n{color=[JK.Colors.warning]}Warning - Manual and quick saves are unable to store choices.{/c}"

        hasTimelineEntry = False
        for entry in viewModel.timeline:
            if entry[1] != None:
                hasTimelineEntry = True

        exportAction = JK.ChoicesTimelineViewModel.ExportTimelineToFile(viewModel)

    if hasTimelineEntry:
        key 'ctrl_K_f' action JK.TextInput.SetActiveAction("search")
        if JK.TextInput.is_active("search"):
            key 'K_ESCAPE' action JK.TextInput.SetActiveAction(None)

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

                    use JK_IconButton('\uf0fb', text="Export to file", action=exportAction, key="ctrl_K_e")

                use JK_YSpacer(offset=3)

                hbox:
                    xfill True

                    # Toggle thumbnails
                    use JK_Checkbox(checked=show_thumbnails, text="Show thumbnails\n{size=-5}(Might be laggy or outright crash){/size}", action=SetScreenVariable("show_thumbnails", not show_thumbnails))

                    # Seach box
                    hbox yalign 0.0 xpos 1.0 xanchor 1.0:
                        frame style "JK_frame":
                            xysize JK.adjustable((300, 50))

                            button:
                                key_events True
                                action SetScreenVariable(JK.TextInput.activeTextInputScreenVariableName, "search")

                                vbox:
                                    hbox:
                                        hbox yalign 0.5:
                                            use JK_Icon(icon="\ue8b6", size=20, hover_color=JK.Colors.hover)

                                        add search_input.displayable(placeholder="Search for choice")

                                    frame style "JK_default" background "#ffffff22" hover_background JK.Colors.hover ysize 2 offset JK.adjustable((0, 2))

                        use JK_XSpacer(offset=2)

                use JK_YSpacer(offset=3)

                vbox:
                    spacing (3 if show_thumbnails else 0)

                    for entry in timeline:
                        $ page, slot = JK.Utils.split_slotname(entry[2])

                        button style "JK_text":
                            action [FileLoad(slot, confirm=True, page=page), Hide("JK_ChoicesTimeline")]

                            hbox:
                                if show_thumbnails:
                                    image renpy.slot_screenshot(entry[2]) size JK.Utils.resizeDimensionsToLimits((renpy.config.thumbnail_width, renpy.config.thumbnail_height), (100, 100))

                                    use JK_XSpacer(offset=3)

                                hbox yalign 0.5:
                                    $ n = entry[0] + 1
                                    text "[n]." hover_color JK.Colors.hover:
                                        if entry[1] is None:
                                            color JK.Colors.na

                                    if entry[1] is None:
                                        text "??????" color JK.Colors.na hover_color JK.Colors.hover
                                    else:
                                        text JK.Utils.replaceReservedCharacters(entry[1]) hover_color JK.Colors.hover

                                    use JK_XSpacer(offset=3)

                                    text "{size=-5}([entry[2]]){/size}" color "#4b4b4b" hover_color JK.Colors.hover yalign 0.5
    else:
        vbox:
            hbox:
                xfill True

                text choicesText xalign 0.5 text_align 0.5

            hbox:
                xfill True
                yfill True
            
                hbox xalign 0.5 yalign 0.5:
                    use JK_Title("No choices found.", color=JK.Colors.error)
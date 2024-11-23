screen SSSSS_ChoicesTimelineList(viewModel, show_thumbnails, search, activeTextInput):
    python:
        timeline = SSSSS.Utils.filter_timeline(viewModel.timeline, search)

        current_state_text = "{color=" + SSSSS.Colors.status_disabled + "}disabled{/color}"
        if viewModel.playthrough.autosaveOnChoices:
            current_state_text = "{color=" + SSSSS.Colors.status_enabled + "}enabled{/color}"

        choicesText = "Choices are saved into save files {u}only{/u} when this mod is active and \"Autosave on choice\" is enabled (currently [current_state_text]) in the playthrough settings.\n{color=[SSSSS.Colors.warning]}Warning - Manual and quick saves are unable to store choices.{/c}"

        hasTimelineEntry = False
        for entry in viewModel.timeline:
            if entry[1] != None:
                hasTimelineEntry = True

        exportAction = SSSSS.ChoicesTimelineViewModel.ExportTimelineToFile(viewModel)

    if hasTimelineEntry:
        key 'K_e' action exportAction
        key 'ctrl_K_f' action SetScreenVariable("__activeTextInput__", "search")
        if activeTextInput == "search":
            key 'K_ESCAPE' action SetScreenVariable("__activeTextInput__", None)

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

                    use sssss_iconButton('\uf0fb', text="{u}E{/u}xport to file", action=exportAction)

                use SSSSS_YSpacer(offset=3)

                hbox:
                    xfill True

                    # Toggle thumbnails
                    use SSSSS_Checkbox(checked=show_thumbnails, text="Show thumbnails\n{size=-5}(Might be laggy or outright crash){/size}", action=SetScreenVariable("show_thumbnails", not show_thumbnails))

                    # Seach box
                    hbox yalign 0.0 xpos 1.0 xanchor 1.0 ypos 1.0 yanchor 1.0:
                        frame style "SSSSS_frame":
                            xysize adjustable((300, 50))

                            button:
                                key_events True
                                action NullAction()

                                vbox:
                                    hbox:
                                        hbox yalign 0.5:
                                            use sssss_icon(icon="\ue8b6", size=20, hover_color=SSSSS.Colors.hover)

                                        use SSSSS_TextInput(id="search", variableName="search", placeholder="Search for choice")

                                    frame style "SSSSS_default" background "#ffffff22" hover_background SSSSS.Colors.hover ysize 2 offset adjustable((0, -10))

                        use SSSSS_XSpacer(offset=2)

                use SSSSS_YSpacer(offset=3)

                vbox:
                    spacing (3 if show_thumbnails else 0)

                    for entry in timeline:
                        $ page, slot = SSSSS.Utils.splitSavename(entry[2])

                        button style "SSSSS_text":
                            action [FileLoad(slot, confirm=True, page=page), Hide("SSSSS_ChoicesTimeline")]

                            hbox:
                                if show_thumbnails:
                                    image renpy.slot_screenshot(entry[2]) size SSSSS.Utils.resizeDimensionsToLimits((renpy.config.thumbnail_width, renpy.config.thumbnail_height), (100, 100))

                                    use SSSSS_XSpacer(offset=3)

                                hbox yalign 0.5:
                                    $ n = entry[0] + 1
                                    text "[n]." hover_color SSSSS.Colors.hover:
                                        if entry[1] is None:
                                            color SSSSS.Colors.na

                                    if entry[1] is None:
                                        text "??????" color SSSSS.Colors.na hover_color SSSSS.Colors.hover
                                    else:
                                        text SSSSS.Utils.replaceReservedCharacters(entry[1]) hover_color SSSSS.Colors.hover

                                    use SSSSS_XSpacer(offset=3)

                                    text "([entry[2]])" size 18 color "#4b4b4b" hover_color SSSSS.Colors.hover
    else:
        vbox:
            hbox:
                xfill True

                text choicesText xalign 0.5 text_align 0.5

            hbox:
                xfill True
                yfill True
            
                hbox xalign 0.5 yalign 0.5:
                    use SSSSS_Title("No choices found.", color=SSSSS.Colors.error)
screen SSSSS_ChoicesTimeline(timeline, playthrough):
    layer "SSSSSoverlay"
    style_prefix "SSSSS"
    modal True

    default show_thumbnails = False

    use SSSSS_Dialog(title="Choices timeline", closeAction=Hide("SSSSS_ChoicesTimeline")):
        python:
            i = 1

            hasTimelineEntry = False
            for entry in timeline:
                if entry[1] != None:
                    hasTimelineEntry = True

            exportAction = SSSSS.Playthroughs.ExportTimelineToFile(timeline, playthrough=playthrough)

        if hasTimelineEntry:
            key 'K_e' action exportAction

            viewport:
                mousewheel True
                draggable True
                scrollbars "vertical"
                pagekeys True

                vbox:
                    hbox:
                        xfill True

                        python:
                            current_state_text = "{color=#ff623a}disabled{/color}"
                            if playthrough.autosaveOnChoices:
                                current_state_text = "{color=#0f0}enabled{/color}"

                        text "Choices are saved into save files {u}only{/u} when this mod is active and \"Autosave on choice\" is enabled (currently [current_state_text]) in the playthrough settings.\n{color=#ffb14c}Warning - Manual and quick saves are unable to store choices.{/c}" xalign 0.5 text_align 0.5

                    hbox:
                        xalign 0.5

                        use sssss_iconButton('\uf0fb', text="{u}E{/u}xport to file", action=exportAction)

                    use SSSSS_YSpacer(offset=3)

                    # Toggle thumbnails
                    use SSSSS_Checkbox(checked=show_thumbnails, text="Show thumbnails\n{size=-5}(Might be laggy or outright crash){/size}", action=SetScreenVariable("show_thumbnails", not show_thumbnails))

                    use SSSSS_YSpacer(offset=3)

                    vbox:
                        spacing (3 if show_thumbnails else 0)

                        for entry in timeline:
                            $ page, slot = SSSSS.Utils.splitSavename(entry[0])

                            button style "SSSSS_text":
                                action [FileLoad(slot, confirm=True, page=page), Hide("SSSSS_ChoicesTimeline")]

                                hbox:
                                    if show_thumbnails:
                                        image renpy.slot_screenshot(entry[0]) size SSSSS.Utils.resizeDimensionsToLimits((renpy.config.thumbnail_width, renpy.config.thumbnail_height), (100, 100))

                                        use SSSSS_XSpacer(offset=3)

                                    hbox yalign 0.5:
                                        text "[i]." hover_color "#abe9ff":
                                            if entry[1] is None:
                                                color "#f2f2f255"

                                        if entry[1] is None:
                                            text "??????" color "#f2f2f255" hover_color "#abe9ff"
                                        else:
                                            text SSSSS.Utils.replaceReservedCharacters(entry[1]) hover_color "#abe9ff"

                                        use SSSSS_XSpacer(offset=3)

                                        text "([entry[0]])" size 18 color "#4b4b4b" hover_color "#abe9ff"

                            $ i += 1
        else:
            vbox:
                hbox:
                    xfill True

                    text choicesText xalign 0.5 text_align 0.5

                hbox:
                    xfill True
                    yfill True
                
                    text "{color=#f00}No choices found.{/c}" xalign 0.5 yalign 0.5
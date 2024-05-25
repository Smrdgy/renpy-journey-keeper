screen SSSSS_ChoicesTimeline(timeline, playthrough):
    layer "SSSSSoverlay"
    style_prefix "SSSSS"

    default choicesText = "Choices are saved into a save file {u}only{/u} when this mod is active and \"Autosave on choice\" is enabled in the playthrough settings.\n{color=#ff623a}Warning - Manual and quick saves are unable to store choices.{/c}"

    use SSSSS_Dialog(title="Choices timeline", closeAction=Hide("SSSSS_ChoicesTimeline")):
        python:
            i = 1

            hasTimelineEntry = False
            for entry in timeline:
                if entry[1] != "N/A":
                    hasTimelineEntry = True

        if hasTimelineEntry:
            viewport:
                mousewheel True
                draggable True
                scrollbars "vertical"
                pagekeys True

                vbox:
                    hbox:
                        xfill True

                        text choicesText xalign 0.5 text_align 0.5

                        hbox ysize 5

                    hbox:
                        xalign 0.5

                        use sssss_iconButton('\uf0fb', text="Export to file", action=SSSSS.Playthroughs.ExportTimelineToFile(timeline, playthrough=playthrough))

                    hbox ysize 5

                    for entry in timeline:
                        hbox:
                            text "[i]." color "#bbe4ff"

                            text entry[1].replace("[", "⟦").replace("]", "⟧")

                            text "([entry[0]])" size 18 color "#4b4b4b"

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
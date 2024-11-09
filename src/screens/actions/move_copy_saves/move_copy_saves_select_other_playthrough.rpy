screen SSSSS_MoveCopySavesSelectOtherPlaythrough(source_playthrough, destination_playthrough):
    python:
        thumbnailSize = (150, 100)
        playthroughs = [p for p in SSSSS.Playthroughs.playthroughs if p.id != 2 and p != source_playthrough and p != destination_playthrough] # Get all playthroughs except memories, source/destination playthroughs

    viewport:
        mousewheel True
        draggable True
        scrollbars "vertical"
        pagekeys True
        ymaximum 0.85

        vbox:
            xfill True
            spacing 5

            for playthrough in playthroughs:
                button:
                    xfill True
                    background "#ffffff11"
                    action SetScreenVariable("destination_playthrough" if source_playthrough else "source_playthrough", playthrough)

                    hbox:
                        frame:
                            padding (0, 0, 0, 0)
                            xmaximum thumbnailSize[0]
                            ymaximum thumbnailSize[1]

                            if playthrough.hasThumbnail():
                                add playthrough.getThumbnail(thumbnailSize[0], thumbnailSize[1])
                            else:
                                frame:
                                    xysize thumbnailSize

                                    button:
                                        style_prefix ""
                                        action None
                                        xalign 0.5
                                        yalign 0.5

                                        use sssss_icon(icon="\ue3f4", color="#333", size=50)

                        use SSSSS_XSpacer(2)

                        text "[playthrough.name]" yalign 0.5

    # Dialog footer
    hbox:
        xfill True
        yfill True

        style_prefix "SSSSS_dialog_action_buttons"

        vbox:
            # Close
            hbox:
                use sssss_iconButton(icon="\ue5cd", text="Close", action=Hide("SSSSS_MoveCopySaves"))
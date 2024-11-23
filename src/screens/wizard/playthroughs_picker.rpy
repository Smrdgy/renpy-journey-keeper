screen SSSSS_PlaythroughsPicker():
    layer "SSSSSoverlay"
    style_prefix 'SSSSS'
    modal True

    default columns = 4
    default thumbnailSize = (int((renpy.config.screen_width - 100) / columns - renpy.config.screen_width / 20), 200)

    use SSSSS_Dialog(title="Select a playthrough", closeAction=Hide("SSSSS_PlaythroughsPicker")):
        style_prefix "SSSSS"

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            pagekeys True

            python:
                playthroughs = [p for p in SSSSS.Playthroughs.playthroughs if p.id != 2] # Get all playthroughs except memories
                total_playthroughs = len(playthroughs)
                rows = total_playthroughs // columns
                if total_playthroughs % columns != 0:
                    rows += 1
                spotsToFill = rows * columns - total_playthroughs

            grid columns rows:
                xfill True
                spacing 20

                for playthrough in playthroughs:
                    $ isActivePlaythrough = SSSSS.Playthroughs.activePlaythrough == playthrough or (playthrough.id == 1 and SSSSS.Playthroughs.activePlaythrough == None)

                    button:
                        xmaximum renpy.config.screen_width
                        ymaximum renpy.config.screen_height
                        background (SSSSS.Colors.selected_background if isActivePlaythrough else SSSSS.Colors.block_background) #TODO: Convert to style and add hover effect
                        action [SSSSS.Playthroughs.ActivatePlaythrough(playthrough), Hide("SSSSS_PlaythroughsPicker")]

                        vbox:
                            xpos 0.5
                            xanchor 0.5
                            ypos 1.0
                            yanchor 1.0

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

                            hbox ysize 5

                            vbox:
                                xsize thumbnailSize[0]

                                text "[playthrough.name]":
                                    xalign 0.5

                                hbox:
                                    xfill True

                                    hbox xpos 0.0 xanchor 0.0 ypos 1.0 yanchor 1.0:
                                        use sssss_iconButton('\ue872', text="Remove", tt="Remove playthrough", action=Show("SSSSS_RemovePlaythroughConfirm", playthrough=playthrough), disabled=playthrough.id == 1, color=SSSSS.Colors.danger)

                                    hbox xpos 1.0 xanchor 1.0 ypos 1.0 yanchor 1.0:
                                        use sssss_iconButton('\ue3c9', text="Edit", tt="Edit playthrough", action=Show("SSSSS_EditPlaythrough", playthrough=playthrough.copy(), isEdit=True))

                for _ in range(0, spotsToFill):
                    text ""
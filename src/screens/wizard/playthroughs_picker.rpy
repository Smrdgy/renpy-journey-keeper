screen SSSSS_PlaythroughsPicker():
    layer "SSSSSoverlay"
    style_prefix 'SSSSS'
    modal True

    default columns = 4
    default thumbnailSize = (int((renpy.config.screen_width - 100) / columns - renpy.config.screen_width / 20), 200)
    default activeColor = "#00ff15"
    default onActiveColor = "#333"

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
                        background (activeColor if isActivePlaythrough else "#ffffff11")
                        action [SSSSS.Playthroughs.ActivatePlaythrough(playthrough), Hide("SSSSS_PlaythroughsPicker")]

                        vbox at center:
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
                                    if isActivePlaythrough:
                                        color onActiveColor

                                hbox:
                                    xfill True

                                    hbox at left:
                                        use sssss_iconButton('\ue872', text="Remove", tt="Remove playthrough", action=Show("SSSSS_RemovePlaythroughConfirm", playthrough=playthrough), disabled=playthrough.id == 1, textColor = "#ff0000")

                                    hbox at right:
                                        use sssss_iconButton('\ue3c9', text="Edit", tt="Edit playthrough", action=Show("SSSSS_EditPlaythrough", playthrough=playthrough.copy(), isEdit=True), textColor=(onActiveColor if isActivePlaythrough else None))

                for _ in range(0, spotsToFill):
                    text ""
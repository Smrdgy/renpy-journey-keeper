screen JK_PlaythroughsPicker():
    layer "JK_Overlay"
    style_prefix 'JK'
    modal True

    default columns = 4
    default thumbnailSize = (int((renpy.config.screen_width - 100) / columns - renpy.config.screen_width / 20), 200)

    use JK_Dialog(title="Select a playthrough", closeAction=Hide("JK_PlaythroughsPicker")):
        style_prefix "JK"

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            pagekeys True

            python:
                playthroughs = [p for p in JK.Playthroughs.playthroughs if p.id != 2] # Get all playthroughs except memories
                total_playthroughs = len(playthroughs) + 1 # Add 1 for the "+" slot
                rows = total_playthroughs // columns
                if total_playthroughs % columns != 0:
                    rows += 1
                spotsToFill = rows * columns - total_playthroughs

            grid columns rows:
                xfill True
                spacing 20

                for playthrough in playthroughs:
                    python:
                        is_active_playthrough = JK.Playthroughs.activePlaythrough == playthrough or (playthrough.id == 1 and JK.Playthroughs.activePlaythrough == None)
                        delete_action = Show("JK_RemovePlaythroughConfirm", playthrough=playthrough)
                        edit_action = Show("JK_EditPlaythrough", playthrough=playthrough.copy(), isEdit=True)

                    button style "JK_playthrough_button":
                        selected is_active_playthrough
                        action [JK.Playthroughs.ActivatePlaythrough(playthrough), Hide("JK_PlaythroughsPicker")]

                        vbox:
                            xpos 0.5
                            xanchor 0.5
                            ypos 1.0
                            yanchor 1.0

                            key "K_DELETE" action delete_action
                            key "K_e" action edit_action

                            frame style "JK_default":
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

                                            use JK_Icon(icon="\ue3f4", color="#333", size=50)

                                if playthrough.description:
                                    hbox xalign 1.0 yalign 0.0:
                                        use JK_IconButton(icon="\uef42", tt=playthrough.description, ttSide="bottom")

                            hbox ysize 5

                            vbox:
                                xsize thumbnailSize[0]

                                text "[playthrough.name]":
                                    xalign 0.5

                                hbox:
                                    xfill True

                                    hbox xpos 0.0 xanchor 0.0 ypos 1.0 yanchor 1.0:
                                        use JK_IconButton('\ue872', text="Remove", action=delete_action, disabled=playthrough.id == 1, color=JK.Colors.danger)

                                    hbox xpos 1.0 xanchor 1.0 ypos 1.0 yanchor 1.0:
                                        use JK_IconButton('\ue3c9', text="Edit", action=edit_action)

                button style "JK_playthrough_button":
                    action Show("JK_EditPlaythrough", playthrough=None)

                    vbox:
                        xpos 0.5
                        xanchor 0.5
                        ypos 1.0
                        yanchor 1.0

                        frame style "JK_default":
                            xmaximum thumbnailSize[0]
                            ymaximum thumbnailSize[1]

                            frame:
                                xysize thumbnailSize

                                button:
                                    style_prefix ""
                                    action None
                                    xalign 0.5
                                    yalign 0.5

                                    use JK_Icon(icon="\ue148", color="#333", hover_color="#fff", size=50)

                        hbox ysize 5

                        vbox:
                            xsize thumbnailSize[0]

                            text "New playthrough" xalign 0.5

                            use JK_IconButton('smrdgy', text="")

                for _ in range(0, spotsToFill):
                    text ""
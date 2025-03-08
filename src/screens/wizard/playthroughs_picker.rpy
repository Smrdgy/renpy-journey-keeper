screen JK_PlaythroughsPicker():
    layer "JK_Overlay"
    style_prefix 'JK'
    modal True

    default columns = 4
    default thumbnailSize = (
        int((renpy.config.screen_width - 100) / columns - renpy.config.screen_width / 20),
        JK.scaled(200)
    )
    default reorder_source = None

    use JK_Dialog(title="Select a playthrough", close_action=Hide("JK_PlaythroughsPicker")):
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
                        is_active_playthrough = JK.Playthroughs.active_playthrough == playthrough or (playthrough.id == 1 and JK.Playthroughs.active_playthrough == None)
                        delete_action = Show("JK_RemovePlaythroughConfirm", playthrough=playthrough)
                        edit_action = Show("JK_EditPlaythrough", playthrough=playthrough.copy(), isEdit=True)

                    button style "JK_playthrough_button":
                        selected is_active_playthrough
                        action [JK.Playthroughs.ActivatePlaythroughAction(playthrough), Hide("JK_PlaythroughsPicker")]

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

                                # Thumbnail
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

                                # Description
                                if playthrough.description:
                                    hbox xalign 1.0 yalign 0.0:
                                        use JK_IconButton(icon="\uef42", tt=playthrough.description, tt_side="bottom")

                                # Reorder
                                hbox xalign 0.0 yalign 0.0:
                                    if reorder_source == playthrough.id:
                                        use JK_IconButton(icon="\ue5c9", action=SetScreenVariable("reorder_source", None), tt="Cancel", tt_side="bottom", hover_color=JK.Colors.error)
                                    elif reorder_source:
                                        use JK_IconButton(icon="\ue39e", action=[JK.Playthroughs.ReorderPlaythroughsAction(source=reorder_source, target=playthrough.id), SetScreenVariable("reorder_source", None)], tt="Move here", tt_side="bottom")
                                    else:
                                        use JK_IconButton(icon="\ue074", action=SetScreenVariable("reorder_source", playthrough.id), tt="Change order", tt_side="bottom", color=JK.Colors.text_light, hover_color=JK.Colors.hover)

                            use JK_YSpacer(4)

                            vbox:
                                xsize thumbnailSize[0]

                                # Name
                                text "[playthrough.name]" xalign 0.5 text_align 0.5

                                # Action buttons
                                hbox:
                                    xfill True

                                    hbox xpos 0.0 xanchor 0.0 ypos 1.0 yanchor 1.0:
                                        use JK_IconButton('\ue872', text="Remove", action=delete_action, disabled=playthrough.id == 1, color=JK.Colors.danger)

                                    hbox xpos 1.0 xanchor 1.0 ypos 1.0 yanchor 1.0:
                                        use JK_IconButton('\ue3c9', text="Edit", action=edit_action)

                # New playthrough
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

                        use JK_YSpacer(4)

                        vbox:
                            xsize thumbnailSize[0]

                            text "New playthrough" xalign 0.5

                            use JK_IconButton('smrdgy', text="")

                # Placeholders
                for _ in range(0, spotsToFill):
                    text ""
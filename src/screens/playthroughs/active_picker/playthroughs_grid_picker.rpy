screen JK_PlaythroughsGridPicker(playthroughs, reorder_source, playthroughs_vlist):
    python:
        columns = 4
        thumbnailSize = (
            int((renpy.config.screen_width - 100) / columns - renpy.config.screen_width / 20),
            JK.scaled(200)
        )
        total_playthroughs = len(playthroughs) + 1 # Add 1 for the "+" slot
        total_rows = (total_playthroughs + columns - 1) // columns

        # Ren'Py's Grid displayable requires exactly columns*rows children, so
        # windowing here has to happen in whole grid-row units rather than
        # arbitrary item indices. Row pitch (thumbnail + name/action footer +
        # spacing) is an estimate - the footer auto-sizes around a text line
        # and an icon-button row, whose exact pixel height isn't known
        # without rendering. Only needs to be close: the overscan margin
        # absorbs small errors.
        row_footer_height = JK.scaled(70)
        row_spacing = 20
        row_pitch = thumbnailSize[1] + row_footer_height + row_spacing

        viewport_size = playthroughs_vlist.estimate_viewport_size(renpy.config.screen_height)
        row_start, row_end, top_spacer, bottom_spacer = playthroughs_vlist.compute(total_rows, row_pitch, viewport_size)

        window_rows = row_end - row_start
        item_start = row_start * columns
        item_end = min(total_playthroughs, row_end * columns)
        spotsToFill = window_rows * columns - (item_end - item_start)

        outlines = [(JK.scaled(2), "#000000", 0, 0)]

    vbox:
        null height top_spacer

        grid columns window_rows:
            xfill True
            spacing row_spacing

            for item_index in range(item_start, item_end):
                if item_index < len(playthroughs):
                    $ playthrough = playthroughs[item_index]

                    python:
                        is_active_playthrough = JK.Playthroughs.active_playthrough == playthrough or (playthrough.id == 1 and JK.Playthroughs.active_playthrough == None)
                        delete_action = Show("JK_RemovePlaythroughConfirm", playthrough=playthrough) if playthrough.deletable else NullAction()
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

                                            use JK_Icon(icon="", color="#333", size=50)

                                # Description
                                if playthrough.description:
                                    hbox xalign 1.0 yalign 0.0:
                                        use JK_IconButton(icon="", tt=playthrough.description, tt_side="bottom", outlines=outlines)

                                # Reorder
                                if len(playthroughs) > 1:
                                    hbox xalign 0.0 yalign 0.0:
                                        if reorder_source == playthrough.id:
                                            use JK_IconButton(icon="", action=SetScreenVariable("reorder_source", None), tt="Cancel", tt_side="bottom", hover_color=JK.Colors.error, outlines=outlines)
                                        elif reorder_source:
                                            use JK_IconButton(icon="", action=[JK.Playthroughs.ReorderPlaythroughsAction(source=reorder_source, target=playthrough.id), SetScreenVariable("reorder_source", None)], tt="Move here", tt_side="bottom", outlines=outlines)
                                        else:
                                            use JK_IconButton(icon="", action=SetScreenVariable("reorder_source", playthrough.id), tt="Change order", tt_side="bottom", color=JK.Colors.text_light, hover_color=JK.Colors.hover, outlines=outlines)

                            use JK_YSpacer(4)

                            vbox:
                                xsize thumbnailSize[0]

                                # Name
                                text "[playthrough.name]" xalign 0.5 text_align 0.5

                                # Action buttons
                                hbox:
                                    xfill True

                                    hbox xpos 0.0 xanchor 0.0 ypos 1.0 yanchor 1.0:
                                        use JK_IconButton('', text="Remove", action=delete_action, disabled=not playthrough.deletable, color=JK.Colors.danger)

                                    hbox xpos 1.0 xanchor 1.0 ypos 1.0 yanchor 1.0:
                                        use JK_IconButton('', text="Edit", action=edit_action)
                else:
                    # New playthrough
                    button style "JK_playthrough_button":
                        action Show("JK_EditPlaythrough", playthrough=None)

                        vbox:
                            xpos 0.5
                            xanchor 0.5
                            ypos 1.0
                            yanchor 1.0

                            frame style "JK_default":
                                xysize thumbnailSize

                                vbox:
                                    xalign 0.5
                                    yalign 0.5

                                    use JK_Icon(icon="", hover_color=JK.Colors.text_primary, size=60)

                            use JK_YSpacer(4)

                            vbox:
                                xsize thumbnailSize[0]

                                text "New playthrough" xalign 0.5

                                use JK_IconButton('smrdgy', text="")

            # Placeholders to keep this windowed grid slice exactly columns*window_rows
            for _ in range(0, spotsToFill):
                text ""

        null height bottom_spacer

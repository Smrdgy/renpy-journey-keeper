screen JK_PlaythroughsTablePicker(playthroughs, reorder_source, playthroughs_vlist):
    style_prefix "JK"

    python:
        total_items = len(playthroughs) + 1 # Add 1 for the "New playthrough" row

        # Fixed row pitch (thumbnail height + a little padding) so windowing
        # math is exact - rows used to auto-size around the thumbnail frame.
        row_pitch = JK.scaled(90)

        viewport_size = playthroughs_vlist.estimate_viewport_size(renpy.config.screen_height)
        item_start, item_end, top_spacer, bottom_spacer = playthroughs_vlist.compute(total_items, row_pitch, viewport_size)

    vbox:
        null height top_spacer

        for item_index in range(item_start, item_end):
            $ i = item_index + 1

            if item_index < len(playthroughs):
                $ playthrough = playthroughs[item_index]

                python:
                    is_active_playthrough = JK.Playthroughs.active_playthrough == playthrough or (playthrough.id == 1 and JK.Playthroughs.active_playthrough == None)
                    delete_action = Show("JK_RemovePlaythroughConfirm", playthrough=playthrough)
                    edit_action = Show("JK_EditPlaythrough", playthrough=playthrough.copy(), isEdit=True)
                    activate_action = [JK.Playthroughs.ActivatePlaythroughAction(playthrough), Hide("JK_PlaythroughsPicker")]

                button:
                    ysize row_pitch
                    style ("JK_row_button" if i % 2 == 0 else "JK_row_odd_button")
                    action activate_action
                    selected is_active_playthrough

                    hbox:
                        spacing 10
                        xfill True

                        hbox:
                            # Thumbnail
                            frame style "JK_default":
                                xysize JK.scaled((150, 80))

                                hbox:
                                    xalign 0.5
                                    yalign 0.5

                                    add playthrough.getThumbnail(JK.scaled(150), JK.scaled(80))

                                if not playthrough.hasThumbnail():
                                    button:
                                        style_prefix ""
                                        action None
                                        xalign 0.5
                                        yalign 0.5

                                        use JK_Icon(icon="", color="#333", size=30)

                            use JK_XSpacer()

                            # Name
                            text playthrough.name yalign 0.5

                            # Description
                            hbox:
                                yalign 0.5
                                xsize 80

                                if playthrough.description:
                                    use JK_IconButton(icon="", tt=playthrough.description)

                        hbox:
                            xalign 1.0
                            yalign 0.5

                            # Move button
                            if len(playthroughs) > 1:
                                if reorder_source == playthrough.id:
                                    use JK_IconButton(icon="", action=SetScreenVariable("reorder_source", None), tt="Cancel", hover_color=JK.Colors.error)
                                elif reorder_source:
                                    use JK_IconButton(icon="", action=[JK.Playthroughs.ReorderPlaythroughsAction(source=reorder_source, target=playthrough.id), SetScreenVariable("reorder_source", None)], tt="Move here")
                                else:
                                    use JK_IconButton(icon="", action=SetScreenVariable("reorder_source", playthrough.id), tt="Change order")

                            # Edit button
                            use JK_IconButton(icon="", tt="Edit", action=edit_action)

                            # Delete button
                            use JK_IconButton(icon="", tt="Delete", action=delete_action, disabled=not playthrough.deletable, disabled_color="#00000000")
            else:
                # New playthrough
                button:
                    ysize row_pitch
                    style ("JK_row_button" if i % 2 == 0 else "JK_row_odd_button")
                    action Show("JK_EditPlaythrough", playthrough=None)

                    hbox:
                        spacing 10
                        xfill True

                        hbox:
                            # Thumbnail
                            frame style "JK_default":
                                xysize JK.scaled((150, 80))

                                hbox:
                                    xalign 0.5
                                    yalign 0.5

                                    use JK_Icon("", hover_color=JK.Colors.text_primary, size=40)

                            use JK_XSpacer()

                            text "New playthrough" yalign 0.5

        null height bottom_spacer

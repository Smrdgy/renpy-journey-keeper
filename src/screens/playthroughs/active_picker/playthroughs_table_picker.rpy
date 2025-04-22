screen JK_PlaythroughsTablePicker(playthroughs, reorder_source):
    style_prefix "JK"

    vbox:
        $ i = 0
        for playthrough in playthroughs:
            python:
                is_active_playthrough = JK.Playthroughs.active_playthrough == playthrough or (playthrough.id == 1 and JK.Playthroughs.active_playthrough == None)
                delete_action = Show("JK_RemovePlaythroughConfirm", playthrough=playthrough)
                edit_action = Show("JK_EditPlaythrough", playthrough=playthrough.copy(), isEdit=True)
                activate_action = [JK.Playthroughs.ActivatePlaythroughAction(playthrough), Hide("JK_PlaythroughsPicker")]
                i += 1

            button:
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

                                    use JK_Icon(icon="\ue3f4", color="#333", size=30)

                        use JK_XSpacer()

                        # Name
                        text playthrough.name yalign 0.5

                        # Description
                        hbox:
                            yalign 0.5
                            xsize 80

                            if playthrough.description:
                                use JK_IconButton(icon="\uef42", tt=playthrough.description)

                    hbox:
                        xalign 1.0
                        yalign 0.5

                        # Move button
                        if len(playthroughs) > 1:
                            if reorder_source == playthrough.id:
                                use JK_IconButton(icon="\ue5c9", action=SetScreenVariable("reorder_source", None), tt="Cancel", tt_side="bottom", hover_color=JK.Colors.error)
                            elif reorder_source:
                                use JK_IconButton(icon="\ue39e", action=[JK.Playthroughs.ReorderPlaythroughsAction(source=reorder_source, target=playthrough.id), SetScreenVariable("reorder_source", None)], tt="Move here", tt_side="bottom")
                            else:
                                use JK_IconButton(icon="\ue074", action=SetScreenVariable("reorder_source", playthrough.id), tt="Change order", tt_side="bottom", color=JK.Colors.text_light, hover_color=JK.Colors.hover)

                        # Edit button
                        use JK_IconButton(icon="\ue3c9", tt="Edit", action=edit_action)

                        # Delete button
                        use JK_IconButton(icon="\ue872", tt="Delete", action=delete_action, disabled=playthrough.id == 1, disabled_color="#00000000")

        $ i += 1
        button:
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

                            use JK_Icon("\ue148", hover_color=JK.Colors.text_primary, size=40)

                    use JK_XSpacer()

                    text "New playthrough" yalign 0.5
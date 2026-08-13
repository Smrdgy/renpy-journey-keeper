screen JK_MoveCopySavesSelectDestination(playthrough, mode, saves):
    style_prefix 'JK'
    modal True

    python:
        thumbnailSize = JK.scaled((150, 100))
        playthroughs = [p for p in JK.Playthroughs.playthroughs if p.id != 2 and p != playthrough] # Get all playthroughs except memories and the source playthrough

    text ("Select the playthrough you want to " + ("move" if mode == "MOVE" else "copy") + " " + str(len(saves)) + " save(s) into.")

    use JK_YSpacer()

    viewport:
        mousewheel True
        draggable True
        scrollbars "vertical"
        vscrollbar_unscrollable "hide"
        pagekeys True
        ymaximum 0.75

        vbox:
            xfill True
            spacing 5

            if not playthroughs:
                text "No other playthroughs available." xalign 0.5

            $ i = 0
            for other_playthrough in playthroughs:
                button style ("JK_row_button" if i % 2 == 0 else "JK_row_odd_button"):
                    xfill True
                    action JK.MoveCopySavesViewModel.SelectDestinationAndStartAction(playthrough, other_playthrough, saves, mode)

                    hbox:
                        frame:
                            padding (0, 0, 0, 0)
                            xmaximum thumbnailSize[0]
                            ymaximum thumbnailSize[1]

                            if other_playthrough.hasThumbnail():
                                add other_playthrough.getThumbnail(thumbnailSize[0], thumbnailSize[1])
                            else:
                                frame:
                                    xysize thumbnailSize

                                    button:
                                        style_prefix ""
                                        action None
                                        xalign 0.5
                                        yalign 0.5

                                        use JK_Icon(icon="\ue3f4", color="#333", size=50)

                        use JK_XSpacer(2)

                        text "[other_playthrough.name]" yalign 0.5

                $ i += 1

    # Dialog footer
    hbox:
        xfill True
        yfill True

        style_prefix "JK_dialog_action_buttons"

        vbox:
            # Back
            hbox:
                use JK_IconButton(icon="\ue5c4", text="Back", action=JK.SavesListViewModel.CancelMoveCopyAction())

            # Close
            hbox:
                use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_SavesList"))

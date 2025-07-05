screen JK_ActivePlaythroughBanner():
    style_prefix "JK"

    python:
        drag_pos = store.persistent.JK_PlaythroughBannerPos or JK.scaled((0.5, 5))

        def dragged(drags, drop):
            d = drags[0]
            xalign = (float(d.x) + float(d.w) / 2) / float(d.parent_width)
            renpy.store.persistent.JK_PlaythroughBannerPos = (xalign, d.y)

        class ResetBannerPositionAction(renpy.ui.Action):
            def __call__(self):
                d = renpy.display.screen.get_widget(None, "JK_ActivePlaythroughBannerDrag")
                if d:
                    if d.drag_moved:
                        return

                    banner_pos_x = store.persistent.JK_PlaythroughBannerPos[0] or 0.5

                    new_x = int(d.parent_width * banner_pos_x - d.w / 2)

                    if new_x - d.w / 2 < 0:
                        new_x = 0
                    elif new_x + d.w > d.parent_width:
                        new_x = int(d.parent_width - d.w)

                    if new_x != d.x:
                        d.snap(new_x, d.y)

        active_playthrough = JK.Playthroughs.active_playthrough

    timer 0.001 repeat True action [ResetBannerPositionAction()]

    drag:
        id "JK_ActivePlaythroughBannerDrag"
        draggable True
        drag_handle (0, 0, 1.0, 1.0)
        xpos drag_pos[0]
        xanchor 0.5
        ypos drag_pos[1]
        droppable False
        dragged dragged
        clicked Show("JK_PlaythroughsPicker")

        frame:
            style "JK_default"
            background "#000000{:02X}".format(int(JK.Settings.sidepanelOpacity * 255))

            hbox:
                if JK.Settings.playthroughBannerShowChangePlaythroughButtons:
                    hbox:
                        yalign 0.5

                        use JK_IconButton(icon="\ue5cb", action=JK.Playthroughs.ActivatePrevPlaythroughAction(), tt="Previous Playthrough", tt_side="auto", tt_preferred_axis="y")


                if JK.Settings.playthroughBannerShowThumbnail:
                    frame style "JK_default":
                        xysize JK.scaled((50, 30))
                        yalign 0.5

                        hbox:
                            xalign 0.5
                            yalign 0.5

                            add active_playthrough.getThumbnail(JK.scaled(50), JK.scaled(30))

                        if not active_playthrough.hasThumbnail():
                            button:
                                style_prefix ""
                                action None
                                xalign 0.5
                                yalign 0.5

                                use JK_Icon(icon="\ue3f4", color="#333", size=20)

                    use JK_XSpacer()

                text active_playthrough.name:
                    size JK.scaled(20)
                    color JK.Colors.theme
                    outlines [(JK.scaled(5), "#000000", 0, 0)]
                    xmaximum renpy.config.screen_width // 3
                    yalign 0.5
                    text_align 0.5

                if JK.Settings.playthroughBannerShowChangePlaythroughButtons:
                    hbox:
                        yalign 0.5

                        use JK_IconButton(icon="\ue5cc", action=JK.Playthroughs.ActivateNextPlaythroughAction(), tt="Next Playthrough", tt_side="auto", tt_preferred_axis="y")
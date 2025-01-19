screen JK_TooltipDialog(title=None, icon=None, message=None, pos=None, interactive=False, side="top", distance=JK.scaled(20), follow_mouse=True):
    layer "JK_Overlay"
    style_prefix 'JK_dialog'
    zorder 99999

    $ closeAction = Hide("JK_TooltipDialog")
    if closeAction:
        key 'K_ESCAPE' action closeAction
        key 'mouseup_3' action closeAction

    if not interactive:
        timer 0.01 repeat follow_mouse action JK.UpdateTooltipPositionAction(side, distance, pos)

    drag:
        id "JK_TooltipDialog"
        draggable interactive
        drag_handle (0, 0, 1.0, 1.0)
        xpos 2.0
        ypos 2.0
        droppable False

        frame style "JK_default":
            id "JK_TooltipDialog_Window"
            background "#0c0c0cfc"
            padding JK.scaled((10, 10, 10, 10))
            xmaximum int(renpy.config.screen_width / 4)

            vbox:
                if title or icon or interactive:
                    hbox:
                        if interactive:
                            use JK_IconButton(icon=None, action=None)

                        hbox:
                            xalign 0.5
                            yalign 0.5

                            if icon:
                                use JK_Icon(icon)

                            if title:
                                hbox xalign 0.5:
                                    use JK_Title(title)

                        if interactive:
                            hbox xpos 1.0 xanchor 1.0:
                                use JK_IconButton(icon="\ue5cd", action=[closeAction, NullAction()])

                if message:
                    text message style "JK_text" xalign 0.5
                transclude

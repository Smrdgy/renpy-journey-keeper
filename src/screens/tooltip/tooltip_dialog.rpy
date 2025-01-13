screen JK_TooltipDialog(title=None, icon=None, message=None, pos=None, interactive=False, side="top", distance=JK.adjustable(20), clamp=False):
    layer "JK_Overlay"
    style_prefix 'JK_dialog'
    zorder 99999
    
    default mouse_position = renpy.get_mouse_pos()

    python:
        pos = pos or mouse_position
        
        if side == "top":
            xanchor = 0.5
            yanchor = 1.0
            draggable_pos = (
                pos[0],
                pos[1] - distance,
            )
        elif side == "bottom":
            xanchor = 0.5
            yanchor = 0.0
            draggable_pos = (
                pos[0],
                pos[1] + distance,
            )
        elif side == "left":
            xanchor = 1.0
            yanchor = 0.5
            draggable_pos = (
                pos[0] - distance,
                pos[1],
            )
        elif side == "right":
            xanchor = 0.0
            yanchor = 0.5
            draggable_pos = (
                pos[0] + distance,
                pos[1],
            )

        if clamp:
            draggable_pos = (
                min(max(draggable_pos[0], 0), renpy.config.screen_width - JK.adjustable(200 + distance)),
                min(max(draggable_pos[1], 0), renpy.config.screen_height - JK.adjustable(200 + distance)),
            )

        closeAction = Hide("JK_TooltipDialog")

    if closeAction:
        key 'K_ESCAPE' action closeAction
        key 'mouseup_3' action closeAction

    timer 0.05 repeat True action [SetScreenVariable("mouse_position", renpy.get_mouse_pos())]

    drag:
        draggable True
        drag_handle (0, 0, 1.0, 1.0)
        xpos draggable_pos[0]
        ypos draggable_pos[1]
        xanchor xanchor
        yanchor yanchor
        droppable False

        frame style "JK_default":
            background "#0c0c0cfc"
            padding (10, 10, 10, 10)
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

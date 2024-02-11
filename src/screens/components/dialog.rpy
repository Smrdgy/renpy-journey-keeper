screen SSSSS_Dialog(title=None, message=None, closeAction=None, xsize=None, modal=True, icon=None, background, size):
    style_prefix 'SSSSS'

    if closeAction:
        key 'K_ESCAPE' action closeAction

    if modal:
        button style "SSSSS_dialog_overlay" xfill True yfill True action [closeAction, NullAction()]

    drag:
        draggable True
        drag_handle (0, 0, 1.0, x52URM.scalePxInt(42))
        if renpy.variant('touch'):
            align (.5,.15)
        else:
            align (.5,.5)

        frame:
            style "SSSSS_dialog_frame"
            background background
            xysize size

            vbox:
                hbox:
                    style "SSSSS_dialog_title"

                    hbox spacing x52URM.scalePxInt(4) yalign .5:
                        xfill True

                        hbox:
                            xalign .5

                            if icon:
                                use sssss_icon(icon)

                            if title:
                                text title yalign .5 size 40 text_align 0.5

                    use SSSSS_DialogCloseButton(action=closeAction)

                button:
                    style_prefix 'SSSSS'
                    style "SSSSS_dialog_content"
                    key_events True # We need this to still trigger key events defined inside of this button
                    action NullAction() # Prevent clicking through
                    has vbox

                    if(message):
                        text message style "SSSSS_text" xalign 0.5 text_align 0.5

                    transclude

screen SSSSS_DialogCloseButton(action=None):
    frame style "SSSSS_dialog_close_frame":
        button style "SSSSS_dialog_close_button":
            action action

            frame style "SSSSS_dialog_close_inner":
                hbox:
                    align (0.5, 0.5)

                    use sssss_icon('\ue5cd')

            
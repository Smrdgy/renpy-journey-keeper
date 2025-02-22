screen JK_Dialog(title=None, message=None, closeAction=None, icon=None):
    layer "overlay"
    style_prefix 'JK_dialog'
    modal True

    if closeAction:
        key 'K_ESCAPE' action closeAction
        key 'mouseup_3' action closeAction

    frame style_suffix "overlay":
        vbox:
            hbox:
                xfill True

                hbox # Alignment placeholder

                hbox:
                    xalign 0.5
                    yalign 0.5

                    if icon:
                        use JK_Icon(icon)

                    if title:
                        text title style_suffix "title" yalign .5 text_align 0.5

                frame:
                    xalign 1.0
                    yalign 0.5

                    use JK_IconButton(icon="\ue5cd", action=[closeAction, NullAction()])

            button:
                style_suffix "content"
                key_events True # We need this to still trigger key events defined inside of this button
                action NullAction() # Prevent clicking through
                has vbox

                if(message):
                    text message style "JK_text" xalign 0.5 text_align 0.5

                transclude

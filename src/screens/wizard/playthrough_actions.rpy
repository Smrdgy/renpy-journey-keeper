screen SSSSS_PlaythroughActions(playthrough):
    style_prefix 'SSSSS'
    use SSSSS_Dialog(title="Playtrhough actions", closeAction=Hide("SSSSS_PlaythroughActions"), background="gui/select_playthrough_dialog_background.png", size=(x52URM.scalePxInt(581), x52URM.scalePxInt(623))):
        style_prefix "SSSSS"

        vbox:
            yfill True

            button:
                style "SSSSS_textbutton_medium_gray"
                action [SSSSS.Playthroughs.TryCycleSaves(playthrough), Hide("SSSSS_PlaythroughActions")]
                key_events True
                xalign 0.5
                
                text "Cycle saves" yalign .5 xalign 0.5 size 28

            button:
                style "SSSSS_textbutton_medium_gray"
                action [SSSSS.Playthroughs.ConstructTimeline(playthrough), Hide("SSSSS_PlaythroughActions")]
                key_events True
                xalign 0.5
                
                text "Show choice timeline" yalign .5 xalign 0.5 size 28
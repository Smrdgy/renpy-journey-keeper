screen SSSSS_PlaythroughActions(playthrough):
    layer "SSSSSoverlay"
    style_prefix 'SSSSS'

    use SSSSS_Dialog(title="Playtrhough actions", closeAction=Hide("SSSSS_PlaythroughActions")):
        style_prefix "SSSSS"

        hbox:
            xfill True
            yfill True

            vbox at right:
                yalign 1.0

                # Cycle saves
                hbox at right:
                    use sssss_iconButton(icon="\ue089", text="Cycle saves", action=[SSSSS.Playthroughs.TryCycleSaves(playthrough), Hide("SSSSS_PlaythroughActions")])
                
                # Show choices timeline
                hbox at right:
                    use sssss_iconButton(icon="\uf184", text="Show choice timeline", action=[SSSSS.Playthroughs.ConstructTimeline(playthrough), Hide("SSSSS_PlaythroughActions")])
                
                # Close
                hbox at right:
                    use sssss_iconButton(icon="\ue5cd", text="Close", action=Hide("SSSSS_PlaythroughActions"))
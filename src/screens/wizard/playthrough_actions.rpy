screen SSSSS_PlaythroughActions(playthrough):
    layer "SSSSSoverlay"
    style_prefix 'SSSSS'
    modal True

    use SSSSS_Dialog(title="Playtrhough actions", closeAction=Hide("SSSSS_PlaythroughActions")):
        style_prefix "SSSSS"

        hbox:
            xfill True
            yfill True

            vbox at right:
                yalign 1.0

                # List all saves
                hbox at right:
                    use sssss_iconButton(icon="\ue617", text="List saves", action=[SSSSS.Playthroughs.ListSaves(playthrough), Hide("SSSSS_PlaythroughActions")])

                # Sequentialize saves
                hbox at right:
                    use sssss_iconButton(icon="\ue089", text="Sequentialize saves", action=[SSSSS.Playthroughs.TrySequentializeSaves(playthrough), Hide("SSSSS_PlaythroughActions")])
                
                # Show choices timeline
                hbox at right:
                    use sssss_iconButton(icon="\uf184", text="Show choice timeline", action=[SSSSS.Playthroughs.ConfirmConstructTimeline(playthrough), Hide("SSSSS_PlaythroughActions")])
                
                # Delete all saves
                hbox at right:
                    use sssss_iconButton(icon="\ue92b", text="Delete all saves", action=[SSSSS.Playthroughs.ConfirmDeleteAllSaves(playthrough), Hide("SSSSS_PlaythroughActions")], color="#f00")
                
                # Close
                hbox at right:
                    use sssss_iconButton(icon="\ue5cd", text="Close", action=Hide("SSSSS_PlaythroughActions"))
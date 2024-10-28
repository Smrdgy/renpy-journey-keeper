screen SSSSS_PlaythroughActions(playthrough):
    layer "SSSSSoverlay"
    style_prefix 'SSSSS'
    modal True

    python:
        listSavesAction = [SSSSS.Playthroughs.ListSaves(playthrough), Hide("SSSSS_PlaythroughActions")]
        sequentializeSavesAction = [SSSSS.Playthroughs.TrySequentializeSaves(playthrough), Hide("SSSSS_PlaythroughActions")]
        constructTimelineAction = [SSSSS.Playthroughs.ConfirmConstructTimeline(playthrough), Hide("SSSSS_PlaythroughActions")]
        deleteAllSavesAction = [SSSSS.Playthroughs.ConfirmDeleteAllSaves(playthrough), Hide("SSSSS_PlaythroughActions")]

    key 'K_l' action listSavesAction
    key 'K_s' action sequentializeSavesAction
    key 'K_t' action constructTimelineAction
    key 'K_d' action deleteAllSavesAction

    use SSSSS_Dialog(title="Playtrhough actions", closeAction=Hide("SSSSS_PlaythroughActions")):
        style_prefix "SSSSS"

        hbox:
            xfill True
            yfill True

            style_prefix "SSSSS_dialog_action_buttons"

            vbox:
                # List all saves
                hbox:
                    use sssss_iconButton(icon="\ue617", text="{u}L{/u}ist saves", action=listSavesAction)

                # Sequentialize saves
                hbox:
                    use sssss_iconButton(icon="\ue089", text="{u}S{/u}equentialize saves", action=sequentializeSavesAction, disabled=not SSSSS.Utils.hasColsAndRowsConfiguration())
                
                # Show choices timeline
                hbox:
                    use sssss_iconButton(icon="\uf184", text="Show choice {u}t{/u}imeline", action=constructTimelineAction)
                
                # Delete all saves
                hbox:
                    use sssss_iconButton(icon="\ue92b", text="{u}D{/u}elete all saves", action=deleteAllSavesAction, color="#f00")
                
                # Close
                hbox:
                    use sssss_iconButton(icon="\ue5cd", text="Close", action=Hide("SSSSS_PlaythroughActions"))
screen SSSSS_PlaythroughActions(playthrough):
    layer "SSSSSoverlay"
    style_prefix 'SSSSS'
    modal True

    python:
        listSavesAction = [Show("SSSSS_SavesList", playthrough=playthrough), Hide("SSSSS_PlaythroughActions")]
        sequentializeSavesAction = [SSSSS.Playthroughs.TrySequentializeSaves(playthrough), Hide("SSSSS_PlaythroughActions")]
        constructTimelineAction = [Show("SSSSS_ChoicesTimeline", playthrough=playthrough), Hide("SSSSS_PlaythroughActions")]
        MoveCopySavesAction = [Show("SSSSS_MoveCopySaves", playthrough=playthrough), Hide("SSSSS_PlaythroughActions")]

    key 'K_e' action listSavesAction
    key 'K_s' action sequentializeSavesAction
    key 'K_t' action constructTimelineAction
    key 'K_m' action MoveCopySavesAction

    use SSSSS_Dialog(title="Playthrough actions", closeAction=Hide("SSSSS_PlaythroughActions")):
        style_prefix "SSSSS"

        hbox:
            xfill True
            yfill True

            style_prefix "SSSSS_dialog_action_buttons"

            vbox:
                # List all saves
                hbox:
                    use sssss_iconButton(icon="\ue617", text="Manag{u}e{/u} saves", action=listSavesAction)

                # Sequentialize saves
                hbox:
                    use sssss_iconButton(icon="\ue089", text="{u}S{/u}equentialize saves", action=sequentializeSavesAction, disabled=not SSSSS.Utils.hasColsAndRowsConfiguration())
                
                # Show choices timeline
                hbox:
                    use sssss_iconButton(icon="\uf184", text="Show choice {u}t{/u}imeline", action=constructTimelineAction)

                # Move/copy saves
                hbox:
                    use sssss_iconButton(icon="\ueb7d", text="{u}M{/u}ove/copy saves", action=MoveCopySavesAction)
                
                # Close
                hbox:
                    use sssss_iconButton(icon="\ue5cd", text="Close", action=Hide("SSSSS_PlaythroughActions"))
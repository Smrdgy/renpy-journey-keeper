screen URPS_PlaythroughActions(playthrough):
    layer "URPS_Overlay"
    style_prefix 'URPS'
    modal True

    python:
        listSavesAction = [Show("URPS_SavesList", playthrough=playthrough), Hide("URPS_PlaythroughActions")]
        sequentializeSavesAction = [URPS.Playthroughs.TrySequentializeSaves(playthrough), Hide("URPS_PlaythroughActions")]
        constructTimelineAction = [Show("URPS_ChoicesTimeline", playthrough=playthrough), Hide("URPS_PlaythroughActions")]
        MoveCopySavesAction = [Show("URPS_MoveCopySaves", playthrough=playthrough), Hide("URPS_PlaythroughActions")]
        duplicatePlaythroughAction = [Show("URPS_DuplicatePlaythrough", playthrough=playthrough), Hide("URPS_PlaythroughActions")]

    key 'K_e' action listSavesAction
    key 'K_s' action sequentializeSavesAction
    key 'K_t' action constructTimelineAction
    key 'K_m' action MoveCopySavesAction

    use URPS_Dialog(title="Playthrough actions", closeAction=Hide("URPS_PlaythroughActions")):
        style_prefix "URPS"

        hbox:
            xfill True
            yfill True

            style_prefix "URPS_dialog_action_buttons"

            vbox:
                # Duplicate playthrough
                hbox:
                    use URPS_IconButton(icon="\uebbd", text="{u}D{/u}uplicate playthrough", action=duplicatePlaythroughAction)

                # List all saves
                hbox:
                    use URPS_IconButton(icon="\ue617", text="Manag{u}e{/u} saves", action=listSavesAction)

                # Sequentialize saves
                hbox:
                    use URPS_IconButton(icon="\ue089", text="{u}S{/u}equentialize saves", action=sequentializeSavesAction, disabled=not URPS.Utils.hasColsAndRowsConfiguration())
                
                # Show choices timeline
                hbox:
                    use URPS_IconButton(icon="\uf184", text="Show choice {u}t{/u}imeline", action=constructTimelineAction)

                # Move/copy saves
                hbox:
                    use URPS_IconButton(icon="\ueb7d", text="{u}M{/u}ove/copy saves", action=MoveCopySavesAction)
                
                # Close
                hbox:
                    use URPS_IconButton(icon="\ue5cd", text="Close", action=Hide("URPS_PlaythroughActions"))
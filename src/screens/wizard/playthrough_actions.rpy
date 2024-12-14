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

    use URPS_Dialog(title="Playthrough actions", closeAction=Hide("URPS_PlaythroughActions")):
        style_prefix "URPS"

        hbox:
            xfill True
            yfill True

            style_prefix "URPS_dialog_action_buttons"

            vbox:
                # Duplicate playthrough
                hbox:
                    use URPS_IconButton(icon="\uebbd", text="Duplicate playthrough", action=duplicatePlaythroughAction, key="ctrl_K_d")

                # List all saves
                hbox:
                    use URPS_IconButton(icon="\ue617", text="Manage saves", action=listSavesAction, key="ctrl_K_e")

                # Sequentialize saves
                hbox:
                    use URPS_IconButton(icon="\ue089", text="Sequentialize saves", action=sequentializeSavesAction, disabled=not URPS.Utils.hasColsAndRowsConfiguration(), key="ctrl_K_s")
                
                # Show choices timeline
                hbox:
                    use URPS_IconButton(icon="\uf184", text="Show choice Timeline", action=constructTimelineAction, key="ctrl_K_t")

                # Move/copy saves
                hbox:
                    use URPS_IconButton(icon="\ueb7d", text="Move/copy saves", action=MoveCopySavesAction, key="ctrl_K_m")
                
                # Close
                hbox:
                    use URPS_IconButton(icon="\ue5cd", text="Close", action=Hide("URPS_PlaythroughActions"))
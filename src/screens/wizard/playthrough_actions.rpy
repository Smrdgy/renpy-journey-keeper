screen JK_PlaythroughActions(playthrough):
    layer "JK_Overlay"
    style_prefix 'JK'
    modal True

    python:
        listSavesAction = [Show("JK_SavesList", playthrough=playthrough), Hide("JK_PlaythroughActions")]
        sequentializeSavesAction = [JK.Playthroughs.TrySequentializeSaves(playthrough), Hide("JK_PlaythroughActions")]
        constructTimelineAction = [Show("JK_ChoicesTimeline", playthrough=playthrough), Hide("JK_PlaythroughActions")]
        MoveCopySavesAction = [Show("JK_MoveCopySaves", playthrough=playthrough), Hide("JK_PlaythroughActions")]
        duplicatePlaythroughAction = [Show("JK_DuplicatePlaythrough", playthrough=playthrough), Hide("JK_PlaythroughActions")]

    use JK_Dialog(title="Playthrough actions", closeAction=Hide("JK_PlaythroughActions")):
        style_prefix "JK"

        hbox:
            xfill True
            yfill True

            style_prefix "JK_dialog_action_buttons"

            vbox:
                # Search playthrough
                hbox:
                    use JK_IconButton(icon="\ue8b6", text="Seach playthrough", action=[Show("JK_SearchPlaythrough"), Hide("JK_PlaythroughActions")], key="ctrl_K_f")

                # Duplicate playthrough
                hbox:
                    use JK_IconButton(icon="\uebbd", text="Duplicate playthrough", action=duplicatePlaythroughAction, key="ctrl_K_d")

                # List all saves
                hbox:
                    use JK_IconButton(icon="\ue617", text="Manage saves", action=listSavesAction, key="ctrl_K_e")

                # Sequentialize saves
                hbox:
                    use JK_IconButton(icon="\ue089", text="Sequentialize saves", action=sequentializeSavesAction, disabled=not JK.Utils.hasColsAndRowsConfiguration(), key="ctrl_K_s")
                
                # Show choices timeline
                hbox:
                    use JK_IconButton(icon="\uf184", text="Show choice Timeline", action=constructTimelineAction, key="ctrl_K_t")

                # Move/copy saves
                hbox:
                    use JK_IconButton(icon="\ueb7d", text="Move/copy saves", action=MoveCopySavesAction, key="ctrl_K_m")
                
                # Close
                hbox:
                    use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_PlaythroughActions"))
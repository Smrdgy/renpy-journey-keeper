screen JK_PlaythroughActions(playthrough):
    layer "JK_Overlay"
    style_prefix 'JK'
    modal True

    use JK_Dialog(title="Playthrough actions", close_action=Hide("JK_PlaythroughActions")):
        style_prefix "JK"

        hbox:
            xfill True
            yfill True

            style_prefix "JK_dialog_action_buttons"

            vbox:
                # Search playthrough
                hbox:
                    use JK_IconButton(icon="\ue8b6", text="Seach playthrough", action=[Show("JK_SearchPlaythrough"), Hide("JK_PlaythroughActions")], key="alt_K_f")

                # Duplicate playthrough
                hbox:
                    use JK_IconButton(icon="\uebbd", text="Duplicate playthrough", action=[Show("JK_DuplicatePlaythrough", playthrough=playthrough), Hide("JK_PlaythroughActions")], key="alt_K_d")

                # List all saves
                hbox:
                    use JK_IconButton(icon="\ue617", text="Manage saves", action=[Show("JK_SavesList", playthrough=playthrough), Hide("JK_PlaythroughActions")], key="alt_K_e")

                # Sequentialize saves
                hbox:
                    use JK_IconButton(icon="\ue089", text="Sequentialize saves", action=[JK.Playthroughs.TrySequentializeSaves(playthrough), Hide("JK_PlaythroughActions")], disabled=not JK.Utils.has_cols_and_rows_configuration(), key="alt_K_s")
                
                # Show choices timeline
                hbox:
                    use JK_IconButton(icon="\uf184", text="Show choice Timeline", action=[Show("JK_ChoicesTimeline", playthrough=playthrough), Hide("JK_PlaythroughActions")], key="alt_K_t")

                # Move/copy saves
                hbox:
                    use JK_IconButton(icon="\ueb7d", text="Move/copy saves", action=[Show("JK_MoveCopySaves", playthrough=playthrough), Hide("JK_PlaythroughActions")], key="alt_K_m")
                
                # Close
                hbox:
                    use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_PlaythroughActions"))
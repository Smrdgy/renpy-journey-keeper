screen JK_ImportPlaythroughsConflict(view_model):
    viewport:
        mousewheel True
        draggable True
        scrollbars "vertical"
        vscrollbar_unscrollable "hide"
        pagekeys True
        ymaximum 0.85

        grid 2 1 xfill True:
            $ i = 0
            for playthrough in view_model.conflicts[0]:
                $ i += 1
                vbox xalign 0.5:
                    hbox xalign 0.5:
                        use JK_Title("Existing" if i == 1 else "New")

                    use JK_YSpacer()

                    hbox xalign 0.5:
                        use JK_Title(playthrough.name, 2)

                    use JK_YSpacer(3)

                    text "/game/" + playthrough.directory xalign 0.5 text_align 0.5

                    use JK_YSpacer(3)

                    text (playthrough.description or "(No description)") xalign 0.5 text_align 0.5

                    use JK_YSpacer(3)

                    image playthrough.getThumbnail(width=renpy.config.screen_width // 4, height=renpy.config.screen_width // 4) xalign 0.5


    # Dialog footer
    hbox:
        xfill True
        yfill True

        style_prefix "JK_dialog_action_buttons"

        vbox xalign 1.0:
            # Overwrite
            hbox:
                use JK_IconButton(icon="\ue161", text="Overwrite", action=[Function(view_model.conflict_overwrite)], color=JK.Colors.danger)

            # Keep both
            hbox:
                use JK_IconButton(icon="\ue161", text="Keep both", action=[Function(view_model.conflict_keep_both)])
            
            # Skip
            hbox:
                use JK_IconButton(icon="\ue044", text="Skip", action=[Function(view_model.conflict_skip)])

            # Close
            hbox:
                use JK_IconButton(icon="\ue5cd", text="Abort", action=Hide("JK_ImportPlaythroughs"))
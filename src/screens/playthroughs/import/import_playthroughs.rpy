screen JK_ImportPlaythroughs():
    layer "JK_Overlay"
    style_prefix 'JK'
    modal True

    default view_model = JK.ImportPlaythroughsViewModel()
    default show_thumbnails = False
    default copySaves = False
    default search = ""
    default import_games_vlist = JK.VirtualListState()
    default import_playthroughs_vlist = JK.VirtualListState()

    $ game_name = view_model.selected_game[0] if view_model.selected_game else None
    use JK_Dialog(title="Import playthrough(s)", message="Select playthroughs you want to import from {}.".format(game_name) if view_model.selected_game else "Select a game you want to import from.", close_action=Hide("JK_ImportPlaythroughs")):
        style_prefix "JK"

        if view_model.error_message:
            vbox:
                xfill True
                yfill True
                ymaximum 0.85

                vbox:
                    align (0.5, 0.5)

                    hbox:
                        xalign 0.5

                        use JK_Title("Error", color=JK.Colors.error)

                    hbox:
                        xalign 0.5

                        use JK_Title(view_model.error_message, size=4)

            # Dialog footer
            hbox:
                xfill True
                yfill True

                style_prefix "JK_dialog_action_buttons"

                vbox xalign 1.0:
                    # Close
                    hbox:
                        use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_ImportPlaythroughs"))

        elif view_model.loading:
            vbox:
                xfill True
                yfill True
                ymaximum 0.85

                vbox:
                    align (0.5, 0.5)

                    use JK_Title("Loading playthroughs..." if view_model.selected_game else "Loading games...")

            # Dialog footer
            hbox:
                xfill True
                yfill True

                style_prefix "JK_dialog_action_buttons"

                vbox xalign 1.0:
                    # Close
                    hbox:
                        use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_ImportPlaythroughs"))

        elif len(view_model.conflicts) > 0:
            use JK_ImportPlaythroughsConflict(view_model)

        elif view_model.saves_view_model and view_model.saves_view_model.processing:
            python:
                saves_processed = view_model.saves_view_model.processed
                saves_to_process = len(view_model.saves_view_model.saves_to_process)

            vbox:
                xfill True
                yfill True
                ymaximum 0.85

                vbox:
                    align (0.5, 0.5)
                    xfill True
                    xmaximum 0.85

                    hbox xalign 0.5:
                        use JK_Title("Copying saves...")

                    use JK_YSpacer()

                    text "[saves_processed]/[saves_to_process]" xalign 0.5
                    bar value saves_processed range saves_to_process

            # Dialog footer
            hbox:
                xfill True
                yfill True

                style_prefix "JK_dialog_action_buttons"

                vbox xalign 1.0:
                    # Stop
                    hbox:
                        use JK_IconButton(icon="", text="Stop", action=Function(view_model.saves_view_model.process_stop), color=JK.Colors.danger)

        elif view_model.saves_view_model and view_model.saves_view_model.error:
            vbox:
                xfill True
                yfill True
                ymaximum 0.85

                vbox:
                    align (0.5, 0.5)

                    hbox xalign 0.5:
                        use JK_Title("Error", color=JK.Colors.danger)

                    use JK_YSpacer(offset=2)

                    vbox xalign 0.5:
                        text view_model.saves_view_model.error xalign 0.5 text_align 0.5

                        use JK_YSpacer(offset=2)

                        use JK_ErrorFooter()

            # Dialog footer
            hbox:
                xfill True
                yfill True

                style_prefix "JK_dialog_action_buttons"

                vbox xalign 1.0:
                    # Close
                    hbox:
                        use JK_IconButton(icon="", text="Close", action=Hide("JK_ImportPlaythroughs"))

        elif view_model.success:
            vbox:
                xfill True
                yfill True
                ymaximum 0.85

                vbox:
                    align (0.5, 0.5)

                    use JK_Title("Done", color=JK.Colors.success)

            # Dialog footer
            hbox:
                xfill True
                yfill True

                style_prefix "JK_dialog_action_buttons"

                vbox xalign 1.0:
                    # Close
                    hbox:
                        use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_ImportPlaythroughs"))

        elif view_model.selected_game:
            use JK_ImportPlaythroughsSelectPlaythroughs(view_model, show_thumbnails, import_playthroughs_vlist, copySaves)

        else:
            use JK_ImportPlaythroughsSelectGame(view_model, search, import_games_vlist)
            
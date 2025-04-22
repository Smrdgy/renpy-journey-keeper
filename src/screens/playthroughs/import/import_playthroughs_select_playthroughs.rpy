screen JK_ImportPlaythroughsSelectPlaythroughs(view_model, last_selected_playthrough, show_thumbnails):
    key "ctrl_K_a" action JK.ImportPlaythroughsViewModel.SelectAllAction(view_model)

    vbox:
        hbox:
            xfill True

            hbox:
                use JK_Checkbox(checked=None if len(view_model.selected_playthroughs) > 0 and len(view_model.selected_playthroughs) < len(view_model.playthroughs) else len(view_model.playthroughs) == len(view_model.selected_playthroughs), action=JK.ImportPlaythroughsViewModel.ToggleAllAction(view_model))

            hbox:
                xalign 1.0

                # Toggle thumbnails
                use JK_Checkbox(checked=show_thumbnails, text="Show thumbnails\n{size=-5}(Might be laggy or outright crash){/size}", action=SetScreenVariable("show_thumbnails", not show_thumbnails))

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            vscrollbar_unscrollable "hide"
            pagekeys True
            ymaximum 0.85

            vbox:
                text "Found {} playthrough(s)".format(len(view_model.playthroughs))

                $ i = 0
                for playthrough in view_model.playthroughs:
                    $ i += 1

                    button:
                        style ("JK_row_button" if i % 2 == 0 else "JK_row_odd_button")
                        selected playthrough in view_model.selected_playthroughs
                        action JK.ImportPlaythroughsViewModel.SelectionAction(view_model, playthrough, last_selected_playthrough)

                        xsize 1.0

                        hbox:
                            # Checkbox
                            vbox:
                                yalign 0.5

                                use JK_Checkbox(checked=playthrough in view_model.selected_playthroughs, action=ToggleSetMembership(view_model.selected_playthroughs, playthrough))

                            # Thumbnail
                            if show_thumbnails:
                                hbox:
                                    xysize (100, 100)

                                    image playthrough.getThumbnail(maxWidth=100, maxHeight=100) align (0.5, 0.5)

                                use JK_XSpacer(2)

                            # Name
                            text playthrough.name yalign 0.5

    # Dialog footer
    hbox:
        xfill True
        yfill True

        vbox:
            use JK_YSpacer(offset=2)

            text "{color=#abe9ff}click{/color} to select only one"
            text "{color=#abe9ff}shift + click{/color} to select multiple"
            text "{color=#abe9ff}ctrl + click{/color} or {color=#abe9ff}click the checkbox{/color} to select/deselect one"

        vbox:
            style_prefix "JK_dialog_action_buttons"

            vbox xalign 1.0:
                # Import playthroughs
                hbox:
                    use JK_IconButton(icon="\ue884", text="Import playthrough(s)", action=Function(view_model.import_selected_playthroughs), key="alt_K_i", disabled=len(view_model.selected_playthroughs) == 0)

                # Back
                hbox:
                    use JK_IconButton(icon="\ue5c4", text="Back", action=JK.ImportPlaythroughsViewModel.BackAction(view_model))

                # Close
                hbox:
                    use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_ImportPlaythroughs"))
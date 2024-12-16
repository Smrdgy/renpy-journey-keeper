screen URPS_SavesListSelectSaves(playthrough, viewModel, hovered_button, last_selected_save, selection_mode, show_thumbnails):
    style_prefix 'URPS'
    modal True

    python:
        saves_length = viewModel.saves_length
        selected_length = len(viewModel.selection)
        row_height = 80 if show_thumbnails else 50
        col_size = 1.0 / len(viewModel.locations) - 0.01

    key "ctrl_K_a" action URPS.SavesListViewModel.SelectAllAction(viewModel, selection_mode)

    hbox ysize URPS.adjustable(42):
        xfill True

        frame style ("URPS_toolbar" if selected_length == 0 else "URPS_toolbar_active"):
            hbox yalign 0.5:
                hbox yalign 0.5:
                    if selected_length == 0:
                        text "{b}{color=#70bde6}[saves_length]{/c}{/b} saves found."
                    else:
                        text "[selected_length] item(s) selected"

                if selected_length == 0:
                    use URPS_IconButton(icon="\ue5d5", action=URPS.SavesListViewModel.RefreshSavesAction(viewModel), tt="Rescan saves")

            hbox xalign 0.5 yalign 0.5:
                use URPS_IconButton(icon="\ue8fe", text="Per save selection", action=URPS.SavesListViewModel.SetSelectionModeAction(viewModel, "PER_SAVE"), toggled=selection_mode == "PER_SAVE", toggledColor=URPS.Colors.selected)
                use URPS_IconButton(icon="\ue949", text="Per directory selection", action=URPS.SavesListViewModel.SetSelectionModeAction(viewModel, "PER_DIRECTORY"), toggled=selection_mode == "PER_DIRECTORY", toggledColor=URPS.Colors.selected)

            if selected_length > 0:
                hbox xpos 1.0 xanchor 1.0:
                    # Delete selection
                    use URPS_IconButton(icon="\ue872", action=URPS.SavesListViewModel.MassDeleteConfirmAction(viewModel), tt="Delete {} save(s)".format(selected_length), ttSide="left")

    viewport:
        mousewheel True
        draggable True
        scrollbars "vertical"
        pagekeys True
        ymaximum 0.85

        vbox:
            use URPS_YSpacer()

            hbox xalign 1.0:
                xfill True

                hbox xpos 1.0 xanchor 1.0 ypos 1.0 yanchor 1.0:
                    # Toggle thumbnails
                    use URPS_Checkbox(checked=show_thumbnails, text="Show thumbnails\n{size=-5}(Might be laggy or outright crash){/size}", action=SetScreenVariable("show_thumbnails", not show_thumbnails))

                    use URPS_XSpacer(offset=2)

            grid len(viewModel.locations) 1:
                spacing (1 if selection_mode == "PER_SAVE" else 5)

                $ directory_index = 0
                for location, saves in viewModel.locations:
                    vbox:
                        xsize col_size

                        hbox:
                            text location.directory size URPS.adjustable(10) yalign 0.5

                            use URPS_IconButton(icon="\ue2c8", action=SmrdgyLib.path.OpenDirectoryAction(path=location.directory), size=15, tt="Open directory")

                        $ i = 0
                        for save in viewModel.all_saves:
                            python:
                                page, slot = SmrdgyLib.save.split_save_name(save)
                                id = (save, None) if selection_mode == "PER_SAVE" else (save, location)
                                i += 1

                            if save in saves:
                                button:
                                    ysize URPS.adjustable(row_height)
                                    xsize 1.0
                                    style ("URPS_row_button" if i % 2 == 0 else "URPS_row_odd_button") selected id in viewModel.selection

                                    key_events True
                                    action URPS.SavesListViewModel.SelectionAction(viewModel, id, saves, last_selected_save)

                                    if hovered_button != id:
                                        hovered SetScreenVariable('hovered_button', id)

                                    frame style "URPS_default":
                                        xsize 1.0

                                        hbox:
                                            xfill True

                                            hbox xysize URPS.adjustable((42, 42)) yalign 0.5:
                                                if hovered_button == id and (directory_index == 0 if selection_mode == "PER_SAVE" else True):
                                                    hbox yalign 0.5:
                                                        use URPS_Checkbox(checked=id in viewModel.selection, text="", action=ToggleSetMembership(viewModel.selection, id))

                                            hbox:
                                                yalign 0.5
                                                xfill True

                                                hbox yalign 0.5:
                                                    if show_thumbnails:
                                                        image location.screenshot(save) size SmrdgyLib.image.get_limited_image_size_with_aspect_ratio(100, 80) yalign 0.5

                                                        use URPS_XSpacer(offset=2)

                                                    text "[save]" yalign 0.5

                                                hbox:
                                                    xalign 1.0
                                                    yalign 0.5

                                                    if hovered_button == id:
                                                        # Load
                                                        use URPS_IconButton(icon="\ue1c4", action=FileLoad(slot, confirm=True, page=page), tt="Load save")

                                                        # Delete
                                                        use URPS_IconButton(icon="\ue872", action=URPS.SavesListViewModel.DeleteSingleConfirmAction(viewModel, (save, location)), tt="Delete save")
                            else:
                                hbox ysize URPS.adjustable(row_height):
                                    hbox xysize URPS.adjustable((42, 42))

                                    text "N/A" yalign 0.5 color URPS.Colors.disabled

                        $ directory_index += 1
    
    # Dialog footer
    hbox:
        xfill True
        yfill True

        vbox:
            use URPS_YSpacer(offset=2)

            text "{color=#abe9ff}click{/color} to select only one"
            text "{color=#abe9ff}shift + click{/color} to select multiple"
            text "{color=#abe9ff}ctrl + click{/color} or {color=#abe9ff}click the checkbox{/color} to select/deselect one"

        vbox:
            style_prefix "URPS_dialog_action_buttons"

            vbox xalign 1.0:
                # Delete all saves
                hbox:
                    use URPS_IconButton(icon="\ue92b", text="Delete all saves", action=[URPS.Playthroughs.ConfirmDeleteAllSaves(playthrough), Hide("URPS_SavesList")], color=URPS.Colors.danger, key="ctrl_K_d")

                # Close
                hbox:
                    use URPS_IconButton(icon="\ue5cd", text="Close", action=Hide("URPS_SavesList"))
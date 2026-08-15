screen JK_SavesListSelectSaves(playthrough, view_model, last_selected_save, selection_mode, show_thumbnails, saves_vlist):
    style_prefix 'JK'
    modal True

    python:
        saves_length = view_model.saves_length
        selected_length = len(view_model.selection)
        row_height = 80 if show_thumbnails else 50
        col_size = 1.0 / len(view_model.locations) - 0.01

        # A JK_Title file-page banner is interleaved before the first save of
        # each file page, so rows aren't uniform height - build a per-save
        # pixel height list for the virtual list's windowing math. The exact
        # banner height is an estimate (font line height isn't known without
        # rendering); it only needs to be close, since the list's overscan
        # margin absorbs small errors.
        title_height = JK.scaled(40)
        scaled_row_height = JK.scaled(row_height)

        row_sizes = []
        for save in view_model.all_saves:
            _, slot = JK.Utils.split_slotname_fast(save)
            size = scaled_row_height
            if slot == 1:
                size += title_height
            row_sizes.append(size)

        # Matches the single JK_YSpacer() placed at the top of the scrollable
        # content below, so scroll-position math accounts for it.
        list_header_size = JK.scaled(40)

        viewport_size = saves_vlist.estimate_viewport_size(renpy.config.screen_height)
        window_start, window_end, top_spacer, bottom_spacer = saves_vlist.compute_variable(row_sizes, viewport_size, list_header_size)
        windowed_saves = view_model.all_saves[window_start:window_end]

    key "ctrl_K_a" action JK.SavesListViewModel.SelectAllAction(view_model, selection_mode)

    if selected_length > 0:
        key "K_DELETE" action JK.SavesListViewModel.MassDeleteConfirmAction(view_model)

    hbox ysize JK.scaled(42):
        xfill True

        frame style ("JK_toolbar" if selected_length == 0 else "JK_toolbar_active"):
            hbox yalign 0.5:
                hbox yalign 0.5:
                    if selected_length == 0:
                        text "{b}{color=#70bde6}[saves_length]{/c}{/b} saves found."
                    else:
                        text "[selected_length] item(s) selected"

                if selected_length == 0:
                    use JK_IconButton(icon="", action=Function(view_model.load_saves, _update_screens=True), tt="Rescan saves")

            hbox xalign 0.5 yalign 0.5:
                use JK_IconButton(icon="", text="Per save selection", action=JK.SavesListViewModel.SetSelectionModeAction(view_model, "PER_SAVE"), toggled=selection_mode == "PER_SAVE", toggled_color=JK.Colors.selected)
                use JK_IconButton(icon="", text="Per directory selection", action=JK.SavesListViewModel.SetSelectionModeAction(view_model, "PER_DIRECTORY"), toggled=selection_mode == "PER_DIRECTORY", toggled_color=JK.Colors.selected)

            if selected_length > 0:
                hbox xpos 1.0 xanchor 1.0:
                    # Move selection to another playthrough
                    use JK_IconButton(icon="", action=JK.SavesListViewModel.StartMoveCopyAction(view_model, "MOVE"), tt="Move {} save(s) to another playthrough".format(selected_length), tt_side="left")

                    # Copy selection to another playthrough
                    use JK_IconButton(icon="", action=JK.SavesListViewModel.StartMoveCopyAction(view_model, "COPY"), tt="Copy {} save(s) to another playthrough".format(selected_length), tt_side="left")

                    # Delete selection
                    use JK_IconButton(icon="", action=JK.SavesListViewModel.MassDeleteConfirmAction(view_model), tt="Delete {} save(s)".format(selected_length), tt_side="left")

    hbox xalign 1.0:
        xfill True

        hbox xpos 1.0 xanchor 1.0 ypos 1.0 yanchor 1.0:
            # Toggle thumbnails
            use JK_Checkbox(checked=show_thumbnails, text="Show thumbnails\n{size=-5}(Might be laggy or outright crash){/size}", action=SetScreenVariable("show_thumbnails", not show_thumbnails))

            use JK_XSpacer(2)

    # Per-location column headers, kept outside the viewport (fixed, doesn't
    # scroll with the list) so scroll-position math only has to account for
    # the list content itself.
    grid len(view_model.locations) 1:
        spacing (1 if selection_mode == "PER_SAVE" else 5)

        for location, saves in view_model.locations:
            hbox:
                xsize col_size

                text location.directory size JK.scaled(10) yalign 0.5

                use JK_IconButton(icon="", action=JK.OpenDirectoryAction(path=location.directory), size=15, tt="Open directory")

    viewport:
        mousewheel True
        draggable True
        scrollbars "vertical"
        vscrollbar_unscrollable "hide"
        pagekeys True
        ymaximum 0.85
        yadjustment saves_vlist.adjustment

        vbox:
            use JK_YSpacer()

            null height top_spacer

            grid len(view_model.locations) 1:
                spacing (1 if selection_mode == "PER_SAVE" else 5)

                $ directory_index = 0
                for location, saves in view_model.locations:
                    vbox:
                        xsize col_size

                        $ i = window_start
                        for save in windowed_saves:
                            python:
                                page, slot = JK.Utils.split_slotname(save)
                                id = (save, None) if selection_mode == "PER_SAVE" else (save, location)
                                i += 1
                                file_page_name = renpy.store.persistent._file_page_name.get(str(page), None) or renpy.store.persistent._file_page_name.get(page, None)

                            if file_page_name and slot == 1:
                                use JK_Title(file_page_name, size=2)

                            if save in saves:
                                button:
                                    ysize JK.scaled(row_height)
                                    xsize 1.0
                                    style ("JK_row_button" if i % 2 == 0 else "JK_row_odd_button") selected id in view_model.selection

                                    key_events True
                                    action JK.SavesListViewModel.SelectionAction(view_model, id, saves, last_selected_save)

                                    frame style "JK_default":
                                        xsize 1.0

                                        hbox:
                                            xfill True

                                            hbox xysize JK.scaled((42, 42)) yalign 0.5:
                                                if (directory_index == 0 if selection_mode == "PER_SAVE" else True):
                                                    hbox yalign 0.5:
                                                        use JK_Checkbox(checked=id in view_model.selection, text="", action=ToggleSetMembership(view_model.selection, id))

                                            hbox:
                                                yalign 0.5
                                                xfill True

                                                hbox yalign 0.5:
                                                    if show_thumbnails:
                                                        image location.screenshot(save) size JK.Image.get_limited_image_size_with_preserved_aspect_ratio(100, 80) yalign 0.5

                                                        use JK_XSpacer(offset=2)

                                                    text "[save]" yalign 0.5

                                                    use JK_XSpacer(2)

                                                    text "{size=-7}" + (location.mtime_as_date(save) or '') + "{/size}" yalign 0.5 xalign 1.0 color JK.Colors.text_light

                                                hbox:
                                                    xalign 1.0
                                                    yalign 0.5

                                                    # Edit
                                                    use JK_IconButton(icon="", action=Show("JK_EditSave", slotname=save, location=location), tt="Edit name & choice text")

                                                    # Load
                                                    use JK_IconButton(icon="", action=FileLoad(slot, confirm=True, page=page), tt="Load save")

                                                    # Delete
                                                    use JK_IconButton(icon="", action=JK.SavesListViewModel.DeleteSingleConfirmAction(view_model, (save, location)), tt="Delete save")
                            else:
                                hbox ysize JK.scaled(row_height):
                                    hbox xysize JK.scaled((42, 42))

                                    text "N/A" yalign 0.5 color JK.Colors.disabled

                        $ directory_index += 1

            null height bottom_spacer

    # Dialog footer
    vbox:
        xfill True
        yfill True

        hbox:
            xfill True

            vbox:
                use JK_YSpacer(offset=2)

                text "{color=#abe9ff}click{/color} to select only one"
                text "{color=#abe9ff}shift + click{/color} to select multiple"
                text "{color=#abe9ff}ctrl + click{/color} or {color=#abe9ff}click the checkbox{/color} to select/deselect one"

            vbox:
                style_prefix "JK_dialog_action_buttons"

                vbox xalign 1.0:
                    # Delete all saves
                    hbox:
                        use JK_IconButton(icon="", text="Delete all saves", action=[JK.Playthroughs.ConfirmDeleteAllSavesAction(playthrough), Hide("JK_SavesList")], color=JK.Colors.danger, key="alt_K_d")

                    # Close
                    hbox:
                        use JK_IconButton(icon="", text="Close", action=Hide("JK_SavesList"))

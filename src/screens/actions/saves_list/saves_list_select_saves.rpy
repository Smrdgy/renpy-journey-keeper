screen JK_SavesListSelectSaves(playthrough, view_model, hovered_button, last_selected_save, selection_mode, show_thumbnails):
    style_prefix 'JK'
    modal True

    python:
        saves_length = view_model.saves_length
        selected_length = len(view_model.selection)
        row_height = 80 if show_thumbnails else 50
        col_size = 1.0 / len(view_model.locations) - 0.01

    key "ctrl_K_a" action JK.SavesListViewModel.SelectAllAction(view_model, selection_mode)

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
                    use JK_IconButton(icon="\ue5d5", action=JK.Call(view_model.load_saves, _restart_interaction=True), tt="Rescan saves")

            hbox xalign 0.5 yalign 0.5:
                use JK_IconButton(icon="\ue8fe", text="Per save selection", action=JK.SavesListViewModel.SetSelectionModeAction(view_model, "PER_SAVE"), toggled=selection_mode == "PER_SAVE", toggled_color=JK.Colors.selected)
                use JK_IconButton(icon="\ue949", text="Per directory selection", action=JK.SavesListViewModel.SetSelectionModeAction(view_model, "PER_DIRECTORY"), toggled=selection_mode == "PER_DIRECTORY", toggled_color=JK.Colors.selected)

            if selected_length > 0:
                hbox xpos 1.0 xanchor 1.0:
                    # Delete selection
                    use JK_IconButton(icon="\ue872", action=JK.SavesListViewModel.MassDeleteConfirmAction(view_model), tt="Delete {} save(s)".format(selected_length), tt_side="left")
            else:
                hbox xalign 1.0:
                    text "Saves per page:" yalign 0.5

                    use JK_IconButton(text="10", action=JK.Call(view_model.set_saves_per_page, _restart_interaction=True, amount=10), toggled=view_model.saves_per_page == 10, toggled_color=JK.Colors.selected)
                    use JK_IconButton(text="20", action=JK.Call(view_model.set_saves_per_page, _restart_interaction=True, amount=20), toggled=view_model.saves_per_page == 20, toggled_color=JK.Colors.selected)
                    use JK_IconButton(text="50", action=JK.Call(view_model.set_saves_per_page, _restart_interaction=True, amount=50), toggled=view_model.saves_per_page == 50, toggled_color=JK.Colors.selected)
                    use JK_IconButton(text="100", action=JK.Call(view_model.set_saves_per_page, _restart_interaction=True, amount=100), toggled=view_model.saves_per_page == 100, toggled_color=JK.Colors.selected)
                    use JK_IconButton(text="All", action=JK.Call(view_model.set_saves_per_page, _restart_interaction=True, amount=None), toggled=view_model.saves_per_page == None, toggled_color=JK.Colors.selected)
   
    hbox xalign 1.0:
        xfill True

        hbox xpos 1.0 xanchor 1.0 ypos 1.0 yanchor 1.0:
            # Toggle thumbnails
            use JK_Checkbox(checked=show_thumbnails, text="Show thumbnails\n{size=-5}(Might be laggy or outright crash){/size}", action=SetScreenVariable("show_thumbnails", not show_thumbnails))

            use JK_XSpacer(2)

    viewport:
        mousewheel True
        draggable True
        scrollbars "vertical"
        vscrollbar_unscrollable "hide"
        pagekeys True
        ymaximum 0.85

        vbox:
            use JK_YSpacer()

            grid len(view_model.locations) 1:
                spacing (1 if selection_mode == "PER_SAVE" else 5)

                $ directory_index = 0
                for location, saves in view_model.locations:
                    vbox:
                        xsize col_size

                        hbox:
                            text location.directory size JK.scaled(10) yalign 0.5

                            use JK_IconButton(icon="\ue2c8", action=JK.OpenDirectoryAction(path=location.directory), size=15, tt="Open directory")

                        $ i = 0
                        for save in view_model.pages[view_model.current_page]:
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

                                    if hovered_button != id:
                                        hovered SetScreenVariable('hovered_button', id)

                                    frame style "JK_default":
                                        xsize 1.0

                                        hbox:
                                            xfill True

                                            hbox xysize JK.scaled((42, 42)) yalign 0.5:
                                                if hovered_button == id and (directory_index == 0 if selection_mode == "PER_SAVE" else True):
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

                                                    if hovered_button == id:
                                                        # Edit
                                                        use JK_IconButton(icon="\ue9a2", action=Show("JK_EditSave", slotname=save, location=location), tt="Edit name & choice text")

                                                        # Load
                                                        use JK_IconButton(icon="\ue1c4", action=FileLoad(slot, confirm=True, page=page), tt="Load save")

                                                        # Delete
                                                        use JK_IconButton(icon="\ue872", action=JK.SavesListViewModel.DeleteSingleConfirmAction(view_model, (save, location)), tt="Delete save")
                            else:
                                hbox ysize JK.scaled(row_height):
                                    hbox xysize JK.scaled((42, 42))

                                    text "N/A" yalign 0.5 color JK.Colors.disabled

                        $ directory_index += 1
    
    # Dialog footer
    vbox:
        xfill True
        yfill True

        if view_model.saves_per_page:
            hbox xalign 0.5 yalign 0.5:
                hbox yalign 0.5:
                    $ prev_jump_page = max(view_model.current_page - 10, 0)
                    use JK_IconButton(icon="\ueac3", action=SetField(view_model, "current_page", prev_jump_page), tt=str(prev_jump_page + 1), disabled=view_model.current_page < 1)
                    use JK_IconButton(icon="\ue5cb", action=SetField(view_model, "current_page", view_model.current_page - 1), disabled=view_model.current_page < 1)

                hbox yalign 0.5:
                    python:
                        def paginate(selected_page, total_pages):
                            visible_pages=10
                            offset = selected_page // (visible_pages - 1)

                            start_page = max(0, offset * (visible_pages - 1))
                            end_page = min(start_page + visible_pages - 1, total_pages)

                            return list(range(start_page, end_page))

                        def paginate_seamlessly(selected_page, total_pages):
                            visible_pages = 9
                            half_visible = visible_pages // 2

                            # Adjust start and end to ensure exactly `visible_pages` items if possible
                            start_page = max(0, selected_page - half_visible)
                            end_page = start_page + visible_pages - 1

                            # If end_page exceeds total_pages, shift the range back
                            if end_page >= total_pages:
                                end_page = total_pages - 1
                                start_page = max(0, end_page - visible_pages + 1)

                            return list(range(start_page, end_page + 1))

                    for page in (paginate_seamlessly(view_model.current_page, len(view_model.pages)) if JK.Settings.seamlessPagination else paginate(view_model.current_page, len(view_model.pages))):
                        button:
                            style_prefix ("JK_PaginationButton_active" if page == view_model.current_page else "JK_PaginationButton")
                            text str(page + 1)
                            action SetField(view_model, "current_page", page)

                hbox yalign 0.5:
                    use JK_IconButton(icon="\ue5cc", action=SetField(view_model, "current_page", view_model.current_page + 1), disabled=view_model.current_page == len(view_model.pages) - 1)

                    $ next_jump_page = min(view_model.current_page + (10 if view_model.current_page > 0 else 9), len(view_model.pages) - 1)
                    use JK_IconButton(icon="\ueac9", action=SetField(view_model, "current_page", next_jump_page), tt=str(next_jump_page + 1), disabled=view_model.current_page == len(view_model.pages) - 1)

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
                        use JK_IconButton(icon="\ue92b", text="Delete all saves", action=[JK.Playthroughs.ConfirmDeleteAllSavesAction(playthrough), Hide("JK_SavesList")], color=JK.Colors.danger, key="alt_K_d")

                    # Close
                    hbox:
                        use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_SavesList"))
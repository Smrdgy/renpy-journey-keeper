screen JK_SavesList(playthrough):
    layer "JK_Overlay"
    style_prefix "JK"
    modal True

    default view_model = JK.SavesListViewModel(playthrough)
    default last_selected_save = None
    default selection_mode = "PER_SAVE" # "PER_SAVE"|"PER_DIRECTORY"
    default show_thumbnails = False
    default saves_vlist = JK.VirtualListState()

    # Move/copy sub-flow, entered from the toolbar once saves are selected
    default move_copy_mode = None # None|"MOVE"|"COPY"
    default move_copy_saves = []
    default move_copy_destination_playthrough = None
    default move_copy_view_model = None

    python:
        if move_copy_mode:
            dialog_title = ("Move" if move_copy_mode == "MOVE" else "Copy") + " saves"
        else:
            dialog_title = "Saves list"

    use JK_Dialog(title=dialog_title, close_action=Hide("JK_SavesList")):
        if move_copy_mode:
            if move_copy_view_model:
                if move_copy_view_model.processing:
                    use JK_MoveCopySavesProcessing(move_copy_view_model, view_model)
                elif move_copy_view_model.error:
                    use JK_MoveCopySavesError(move_copy_view_model, view_model)
                elif move_copy_view_model.success:
                    use JK_MoveCopySavesSuccess(view_model)
            else:
                use JK_MoveCopySavesSelectDestination(playthrough, move_copy_mode, move_copy_saves)
        elif len(view_model.all_saves) > 0:
            if view_model.processing:
                use JK_SavesListProcessing(view_model)
            elif view_model.error:
                use JK_SavesListError(view_model)
            elif view_model.success:
                use JK_SavesListSuccess(view_model)
            elif view_model.screen == "SELECTION":
                use JK_SavesListSelectSaves(playthrough, view_model, last_selected_save, selection_mode, show_thumbnails, saves_vlist)
            elif view_model.screen == "PENDING":
                use JK_SavesListProcessing(view_model)
        else:
            use JK_SavesListNoSaves()
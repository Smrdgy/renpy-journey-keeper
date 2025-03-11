screen JK_SavesList(playthrough):
    layer "JK_Overlay"
    style_prefix "JK"
    modal True

    default view_model = JK.SavesListViewModel(playthrough)
    default hovered_button = None
    default last_selected_save = None
    default selection_mode = "PER_SAVE" # "PER_SAVE"|"PER_DIRECTORY"
    default show_thumbnails = False

    use JK_Dialog(title="Saves list", close_action=Hide("JK_SavesList")):
        if len(view_model.all_saves) > 0:
            if view_model.processing:
                use JK_SavesListProcessing(view_model)
            elif view_model.error:
                use JK_SavesListError(view_model)
            elif view_model.success:
                use JK_SavesListSuccess(view_model)
            elif view_model.screen == "SELECTION":
                use JK_SavesListSelectSaves(playthrough, view_model, hovered_button, last_selected_save, selection_mode, show_thumbnails)
            elif view_model.screen == "PENDING":
                use JK_SavesListProcessing(view_model)
        else:
            use JK_SavesListNoSaves()
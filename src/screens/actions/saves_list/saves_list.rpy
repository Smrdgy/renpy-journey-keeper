screen JK_SavesList(playthrough):
    layer "JK_Overlay"
    style_prefix "JK"
    modal True

    default viewModel = JK.SavesListViewModel(playthrough)
    default hovered_button = None
    default last_selected_save = None
    default selection_mode = "PER_SAVE" # "PER_SAVE"|"PER_DIRECTORY"
    default show_thumbnails = False

    use JK_Dialog(title="Saves list", closeAction=Hide("JK_SavesList")):
        if len(viewModel.all_saves) > 0:
            if viewModel.processing:
                use JK_SavesListProcessing(viewModel)
            elif viewModel.error:
                use JK_SavesListError(viewModel)
            elif viewModel.success:
                use JK_SavesListSuccess(viewModel)
            elif viewModel.screen == "SELECTION":
                use JK_SavesListSelectSaves(playthrough, viewModel, hovered_button, last_selected_save, selection_mode, show_thumbnails)
            elif viewModel.screen == "PENDING":
                use JK_SavesListProcessing(viewModel)
        else:
            use JK_SavesListNoSaves()
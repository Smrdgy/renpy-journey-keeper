screen SSSSS_SavesList(playthrough):
    layer "SSSSSoverlay"
    style_prefix "SSSSS"
    modal True

    default viewModel = SSSSS.SavesListViewModel(playthrough)
    default hovered_button = None
    default last_selected_save = None
    default selection_mode = "PER_SAVE" # "PER_SAVE"|"PER_DIRECTORY"
    default show_thumbnails = False

    use SSSSS_Dialog(title="Saves list", closeAction=Hide("SSSSS_SavesList")):
        if len(viewModel.all_saves) > 0:
            if viewModel.processing:
                use SSSSS_SavesListProcessing(viewModel)
            elif viewModel.error:
                use SSSSS_SavesListError(viewModel)
            elif viewModel.success:
                use SSSSS_SavesListSuccess(viewModel)
            elif viewModel.screen == "SELECTION":
                use SSSSS_SavesListSelectSaves(playthrough, viewModel, hovered_button, last_selected_save, selection_mode, show_thumbnails)
            elif viewModel.screen == "PENDING":
                use SSSSS_SavesListProcessing(viewModel)
        else:
            use SSSSS_SavesListNoSaves()
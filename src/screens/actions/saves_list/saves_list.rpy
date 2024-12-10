screen URPS_SavesList(playthrough):
    layer "URPS_Overlay"
    style_prefix "URPS"
    modal True

    default viewModel = URPS.SavesListViewModel(playthrough)
    default hovered_button = None
    default last_selected_save = None
    default selection_mode = "PER_SAVE" # "PER_SAVE"|"PER_DIRECTORY"
    default show_thumbnails = False

    use URPS_Dialog(title="Saves list", closeAction=Hide("URPS_SavesList")):
        if len(viewModel.all_saves) > 0:
            if viewModel.processing:
                use URPS_SavesListProcessing(viewModel)
            elif viewModel.error:
                use URPS_SavesListError(viewModel)
            elif viewModel.success:
                use URPS_SavesListSuccess(viewModel)
            elif viewModel.screen == "SELECTION":
                use URPS_SavesListSelectSaves(playthrough, viewModel, hovered_button, last_selected_save, selection_mode, show_thumbnails)
            elif viewModel.screen == "PENDING":
                use URPS_SavesListProcessing(viewModel)
        else:
            use URPS_SavesListNoSaves()
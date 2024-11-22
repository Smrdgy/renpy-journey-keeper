screen SSSSS_MoveCopySaves(playthrough):
    layer "SSSSSoverlay"
    style_prefix 'SSSSS'
    modal True

    default source_playthrough = playthrough
    default destination_playthrough = None
    default saves_to_process = []
    default show_thumbnails = False
    default last_selected_save = None

    default viewModel = None

    use SSSSS_Dialog(title="Move/Copy saves" if destination_playthrough else "Select other playthrough", message=None if destination_playthrough else "Select the playthrough you want to move/copy saves into.", closeAction=Hide("SSSSS_MoveCopySaves")):
        style_prefix "SSSSS"

        if source_playthrough and destination_playthrough:
            $ viewModel = viewModel or SSSSS.MoveCopySavesViewModel(source_playthrough, destination_playthrough)

            if viewModel.processing:
                # Processing
                use SSSSS_MoveCopySavesProcessing(viewModel)
            elif viewModel.error:
                # Error
                use SSSSS_MoveCopySavesError(viewModel)
            elif viewModel.success:
                # Success
                use SSSSS_MoveCopySavesSuccess()
            else:
                # Saves selection
                use SSSSS_MoveCopySavesSelectSaves(viewModel, saves_to_process, show_thumbnails, last_selected_save)
        else:
            # Destination playthrough selection
            use SSSSS_MoveCopySavesSelectOtherPlaythrough(source_playthrough, destination_playthrough)
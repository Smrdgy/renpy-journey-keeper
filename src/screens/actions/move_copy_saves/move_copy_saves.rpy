screen JK_MoveCopySaves(playthrough):
    layer "JK_Overlay"
    style_prefix 'JK'
    modal True

    default source_playthrough = playthrough
    default destination_playthrough = None
    default saves_to_process = []
    default show_thumbnails = False
    default last_selected_save = None

    default viewModel = None

    use JK_Dialog(title="Move/Copy saves" if destination_playthrough else "Select other playthrough", message=None if destination_playthrough else "Select the playthrough you want to move/copy saves into.", closeAction=Hide("JK_MoveCopySaves")):
        style_prefix "JK"

        if source_playthrough and destination_playthrough:
            $ viewModel = viewModel or JK.MoveCopySavesViewModel(source_playthrough, destination_playthrough)

            if viewModel.processing:
                # Processing
                use JK_MoveCopySavesProcessing(viewModel)
            elif viewModel.error:
                # Error
                use JK_MoveCopySavesError(viewModel)
            elif viewModel.success:
                # Success
                use JK_MoveCopySavesSuccess()
            else:
                # Saves selection
                use JK_MoveCopySavesSelectSaves(viewModel, saves_to_process, show_thumbnails, last_selected_save)
        else:
            # Destination playthrough selection
            use JK_MoveCopySavesSelectOtherPlaythrough(source_playthrough, destination_playthrough)
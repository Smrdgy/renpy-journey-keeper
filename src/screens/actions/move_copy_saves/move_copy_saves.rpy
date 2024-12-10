screen URPS_MoveCopySaves(playthrough):
    layer "URPS_Overlay"
    style_prefix 'URPS'
    modal True

    default source_playthrough = playthrough
    default destination_playthrough = None
    default saves_to_process = []
    default show_thumbnails = False
    default last_selected_save = None

    default viewModel = None

    use URPS_Dialog(title="Move/Copy saves" if destination_playthrough else "Select other playthrough", message=None if destination_playthrough else "Select the playthrough you want to move/copy saves into.", closeAction=Hide("URPS_MoveCopySaves")):
        style_prefix "URPS"

        if source_playthrough and destination_playthrough:
            $ viewModel = viewModel or URPS.MoveCopySavesViewModel(source_playthrough, destination_playthrough)

            if viewModel.processing:
                # Processing
                use URPS_MoveCopySavesProcessing(viewModel)
            elif viewModel.error:
                # Error
                use URPS_MoveCopySavesError(viewModel)
            elif viewModel.success:
                # Success
                use URPS_MoveCopySavesSuccess()
            else:
                # Saves selection
                use URPS_MoveCopySavesSelectSaves(viewModel, saves_to_process, show_thumbnails, last_selected_save)
        else:
            # Destination playthrough selection
            use URPS_MoveCopySavesSelectOtherPlaythrough(source_playthrough, destination_playthrough)
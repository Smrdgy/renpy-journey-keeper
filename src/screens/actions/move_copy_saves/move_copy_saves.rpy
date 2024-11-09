style SSSSS_row_button is SSSSS_button:
    selected_background "#7ff98172"
    hover_background "#abe9ff6c"
    selected_hover_background "#abffe76c"

style SSSSS_row_odd_button is SSSSS_row_button:
    background "#ffffff11"
    selected_background "#7ff98172"
    hover_background "#abe9ff6c"
    selected_hover_background "#abffe76c"

screen SSSSS_MoveCopySaves(playthrough):
    layer "SSSSSoverlay"
    style_prefix 'SSSSS'
    modal True

    default source_playthrough = playthrough
    default destination_playthrough = None
    default saves_to_process = []
    default show_thumbnails = False

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
                use SSSSS_MoveCopySavesSuccess(viewModel)
            else:
                # Saves selection
                use SSSSS_MoveCopySavesSelectSaves(viewModel, saves_to_process, show_thumbnails)
        else:
            # Destination playthrough selection
            use SSSSS_MoveCopySavesSelectOtherPlaythrough(source_playthrough, destination_playthrough)
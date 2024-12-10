screen URPS_ChoicesTimeline(playthrough):
    layer "URPS_Overlay"
    style_prefix "URPS"
    modal True

    default show_thumbnails = False
    default search = ""

    default viewModel = URPS.ChoicesTimelineViewModel(playthrough)

    use URPS_Dialog(title="Choices timeline", closeAction=Hide("URPS_ChoicesTimeline")):
        if viewModel.loading:
            use URPS_ChoicesTimelineLoading(viewModel)
        elif viewModel.error:
            use URPS_ChoicesTimelineError(viewModel)
        else:
            use URPS_ChoicesTimelineList(viewModel, show_thumbnails, search)
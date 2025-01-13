screen JK_ChoicesTimeline(playthrough):
    layer "JK_Overlay"
    style_prefix "JK"
    modal True

    default show_thumbnails = False
    default search = ""

    default viewModel = JK.ChoicesTimelineViewModel(playthrough)

    use JK_Dialog(title="Choices timeline", closeAction=Hide("JK_ChoicesTimeline")):
        if viewModel.loading:
            use JK_ChoicesTimelineLoading(viewModel)
        elif viewModel.error:
            use JK_ChoicesTimelineError(viewModel)
        else:
            use JK_ChoicesTimelineList(viewModel, show_thumbnails, search)
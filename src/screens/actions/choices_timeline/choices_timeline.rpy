screen SSSSS_ChoicesTimeline(playthrough):
    layer "SSSSSoverlay"
    style_prefix "SSSSS"
    modal True

    default show_thumbnails = False
    default search = ""
    default __activeTextInput__ = None

    default viewModel = SSSSS.ChoicesTimelineViewModel(playthrough)

    use SSSSS_Dialog(title="Choices timeline", closeAction=Hide("SSSSS_ChoicesTimeline")):
        if viewModel.loading:
            use SSSSS_ChoicesTimelineLoading(viewModel)
        elif viewModel.error:
            use SSSSS_ChoicesTimelineError(viewModel)
        else:
            use SSSSS_ChoicesTimelineList(viewModel, show_thumbnails, search, activeTextInput=__activeTextInput__)
screen JK_ChoicesTimeline(playthrough):
    layer "JK_Overlay"
    style_prefix "JK"
    modal True

    default show_thumbnails = False
    default search = ""

    default view_model = JK.ChoicesTimelineViewModel(playthrough)

    use JK_Dialog(title="Choices timeline", close_action=Hide("JK_ChoicesTimeline")):
        if view_model.loading:
            use JK_ChoicesTimelineLoading(view_model)
        elif view_model.error:
            use JK_ChoicesTimelineError(view_model)
        else:
            use JK_ChoicesTimelineList(view_model, show_thumbnails, search)
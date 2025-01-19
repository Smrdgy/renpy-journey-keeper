screen JK_Pagination():
    style_prefix 'JK'

    default estimatedPaginationSize = (950, 80)

    python:
        import math

        try:
            currentPage = persistent._file_page
            if(currentPage == "quick" or currentPage == "auto"):
                currentPage = 0

            currentPage = int(currentPage)
            pageOffset = math.floor(currentPage / 10)
        except:
            currentPage = 1
            pageOffset = 0

        paginationPos = store.persistent.JK_PaginationPos or (int(renpy.config.screen_width / 2 - estimatedPaginationSize[0] / 2), int(renpy.config.screen_height - estimatedPaginationSize[1] - 15))

        def pagination_dragged(drags, drop):
            renpy.store.persistent.JK_PaginationPos = (drags[0].x, drags[0].y)

        pagination_button_size = renpy.style.Style("JK_PaginationButton_text").size

    if JK.Settings.debugEnabled:
        frame:
            background "#ff0000cc"
            xysize estimatedPaginationSize
            xpos paginationPos[0]
            ypos paginationPos[1]

    drag:
        draggable True
        drag_handle (0, 0, 1.0, 1.0)
        xpos paginationPos[0]
        ypos paginationPos[1]
        droppable False
        dragged pagination_dragged

        frame:
            background "#000000fc"

            hbox yalign 0.5:
                hbox yalign 0.5:
                    use JK_IconButton('\ue8a0', tt="Go to page", action=JK.Pagination.ToggleGoToPage(), size=JK.scaled(30))

                use JK_XSpacer()

                hbox yalign 0.5:
                    use JK_IconButton(text="A", action=FilePage("auto"), toggled=persistent._file_page == "auto", toggledColor=JK.Colors.selected, tt="Native autosaves", size=pagination_button_size)
                    use JK_IconButton(text="Q", action=FilePage("quick"), toggled=persistent._file_page == "quick", toggledColor=JK.Colors.selected, tt="Quick saves", size=pagination_button_size)

                use JK_XSpacer()

                hbox yalign 0.5:
                    use JK_IconButton(icon="\ueac3", action=FilePage(max(currentPage - 10, 1)), tt=str(max(currentPage - 10, 1)), disabled=currentPage < 2)
                    use JK_IconButton(icon="\ue5cb", action=FilePage(max(currentPage - 1, 1)), disabled=currentPage < 2)

                hbox yalign 0.5:
                    for page in range(int(pageOffset * 10), int(pageOffset * 10 + 10)):
                        button:
                            style_prefix ("JK_PaginationButton_active" if page == currentPage else "JK_PaginationButton")
                            text (str(page) if page > 0 else "")

                            if page > 0:
                                action FilePage(page)

                hbox yalign 0.5:
                    use JK_IconButton(icon="\ue5cc", action=FilePageNext())
                    use JK_IconButton(icon="\ueac9", action=FilePage(currentPage + 10), tt=str(currentPage + 10))
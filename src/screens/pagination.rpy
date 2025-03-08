screen JK_Pagination():
    style_prefix 'JK'

    default estimated_pagination_size = JK.scaled((880, 80))

    python:
        try:
            currentPage = persistent._file_page
            if(currentPage == "quick" or currentPage == "auto"):
                currentPage = 0

            currentPage = int(currentPage)
        except:
            currentPage = 1

        paginationPos = store.persistent.JK_PaginationPos or (int(renpy.config.screen_width / 2 - estimated_pagination_size[0] / 2), int(renpy.config.screen_height - estimated_pagination_size[1] - 15))

        def pagination_dragged(drags, drop):
            renpy.store.persistent.JK_PaginationPos = (drags[0].x, drags[0].y)

        def paginate(selected_page, visible_pages=10):
            offset = selected_page // visible_pages

            return list(range(offset * visible_pages, offset * visible_pages + visible_pages))

        def paginate_seamlessly(selected_page, visible_pages=9):
            half_visible = visible_pages // 2

            start_page = max(1, selected_page - half_visible)
            end_page = start_page + visible_pages - 1

            return list(range(start_page, end_page + 1))

    if JK.Settings.debugEnabled:
        frame:
            background "#ff0000cc"
            xysize estimated_pagination_size
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
            background "#000000{:02X}".format(int(JK.Settings.paginationOpacity * 255))

            hbox yalign 0.5:
                hbox yalign 0.5:
                    use JK_IconButton('\ue8a0', tt="Go to page", action=JK.Pagination.ToggleGoToPageAction(), size=30)

                use JK_XSpacer()

                hbox yalign 0.5:
                    use JK_IconButton(text="A", action=FilePage("auto"), toggled=persistent._file_page == "auto", toggled_color=JK.Colors.selected, tt="Native automatic saves", size=25)
                    use JK_IconButton(text="Q", action=FilePage("quick"), toggled=persistent._file_page == "quick", toggled_color=JK.Colors.selected, tt="Native quick saves", size=25)

                use JK_XSpacer()

                hbox yalign 0.5:
                    use JK_IconButton(icon="\ueac3", action=FilePage(max(currentPage - 10, 1)), tt=str(max(currentPage - 10, 1)), disabled=currentPage < 2)
                    use JK_IconButton(icon="\ue5cb", action=FilePage(max(currentPage - 1, 1)), disabled=currentPage < 2)

                hbox yalign 0.5:
                    for page in (paginate_seamlessly(currentPage) if JK.Settings.seamlessPagination else paginate(currentPage)):
                        button:
                            style_prefix ("JK_PaginationButton_active" if page == currentPage else "JK_PaginationButton")
                            text (str(page) if page > 0 else "")

                            if page > 0:
                                action FilePage(page)

                hbox yalign 0.5:
                    use JK_IconButton(icon="\ue5cc", action=FilePageNext())

                    $ next_jump_page = currentPage + (10 if currentPage > 1 else 9)
                    use JK_IconButton(icon="\ueac9", action=FilePage(next_jump_page), tt=str(next_jump_page))
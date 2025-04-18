screen JK_Pagination():
    style_prefix 'JK'

    python:
        pagination_content = JK.Pagination.get_content()
        pagination_size = (JK.Pagination.get_content_width(pagination_content), JK.scaled(80))
        paginationPos = store.persistent.JK_PaginationPos or (int(renpy.config.screen_width / 2 - pagination_size[0] / 2), int(renpy.config.screen_height - pagination_size[1] - 15))

        def pagination_dragged(drags, drop):
            renpy.store.persistent.JK_PaginationPos = (drags[0].x, drags[0].y)

    if JK.Settings.debugEnabled:
        frame:
            background "#ff0000cc"
            xysize pagination_size
            xpos paginationPos[0]
            ypos paginationPos[1]

    drag:
        draggable True
        drag_handle (0, 0, 1.0, 1.0)
        xpos paginationPos[0]
        ypos paginationPos[1]
        droppable False
        dragged pagination_dragged

        use JK_PaginationContent(pagination_content)
screen SSSSS_Pagination():
    style_prefix 'SSSSS'

    default estimatedPaginationSize = (950, 80)

    python:
        import math

        currentPage = persistent._file_page
        if(currentPage == "quick" or currentPage == "auto"):
            currentPage = 1
        
        currentPage = int(currentPage)

        pageOffset = math.floor(currentPage / 10)

        paginationPos = store.persistent.SSSSS_PaginationPos or (int(renpy.config.screen_width / 2 - estimatedPaginationSize[0] / 2), int(renpy.config.screen_height - estimatedPaginationSize[1] - 15))

        def pagination_dragged(drags, drop):
            renpy.store.persistent.SSSSS_PaginationPos = (drags[0].x, drags[0].y)

    if renpy.config.developer:
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
            background "#000000ee"

            ## Buttons to access other pages.
            hbox:
                yalign 0.5
                spacing 10

                hbox at left:
                    use sssss_iconButton('\uf045', tt="Go to page", action=SSSSS.Pagination.ToggleGoToPage())
                    if SSSSS.Pagination.showGoTo:
                        use SSSSS_GoToPage()

                hbox:
                    yalign 0.5
                    spacing 10

                    hbox at left:
                        spacing 10

                        textbutton "<<" action FilePage(max(currentPage - 10, 1)) style "SSSSS_pagination_textbutton"
                        textbutton "<" action FilePage(max(currentPage - 1, 1)) style "SSSSS_pagination_textbutton"

                    grid 10 1 at center:
                        spacing 10
                        
                        if pageOffset == 0:
                            hbox

                        for page in range(max(int(pageOffset * 10), 1), int(pageOffset * 10 + 10)):
                            hbox:
                                xsize 55

                                textbutton "[page]":
                                    action FilePage(page)
                                    style ("SSSSS_pagination_textbutton_active" if page == currentPage else "SSSSS_pagination_textbutton")
                                    at center

                    hbox at right:
                        spacing 10

                        textbutton ">" action FilePageNext() style "SSSSS_pagination_textbutton"
                        textbutton ">>" action FilePage(currentPage + 10) style "SSSSS_pagination_textbutton"
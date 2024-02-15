screen SSSSS_Pagination():
    style_prefix 'SSSSS'

    default paginationSize = (1000, 80)

    python:
        import math
        import sys

        isPython2 = sys.version_info[0] == 2

        currentPage = persistent._file_page
        if(currentPage == "quick" or currentPage == "auto"):
            currentPage = 1
        
        currentPage = int(currentPage)

        pageOffset = math.floor(currentPage / 10)

        paginationPos = store.persistent.SSSSS_PaginationPos or (renpy.config.screen_width / 2 - paginationSize[0] / 2, renpy.config.screen_height - paginationSize[1] - 15)

        def pagination_dragged(drags, drop):
            renpy.store.persistent.SSSSS_PaginationPos = (drags[0].x, drags[0].y)

    drag:
        draggable True
        drag_handle (-10, -10, paginationSize[0] + 20, paginationSize[1] + 20)
        xpos paginationPos[0]
        ypos paginationPos[1]
        droppable False
        dragged pagination_dragged

        frame:
            style_prefix "SSSSS"
            background None
            xysize paginationSize

            frame:
                background "gui/pagination.png"
                offset (-20, -21)

            ## Buttons to access other pages.
            grid 3 1:
                xfill True
                yalign 1.0
                spacing 10

                hbox at left:
                    spacing 10

                    use sssss_iconButton('\uf045', tt=_("Go to page"), action=SSSSS.Pagination.ToggleGoToPage())
                    if SSSSS.Pagination.showGoTo:
                        use SSSSS_GoToPage()

                    textbutton _("<<") action FilePage(max(currentPage - 10, 1)) style "SSSSS_pagination_textbutton"
                    textbutton _("<") action FilePagePrevious() style "SSSSS_pagination_textbutton"

                grid 10 1 at center:
                    spacing 10

                    for page in range(max(int(pageOffset * 10), 1), int(pageOffset * 10 + 10)):
                        textbutton "[page]" action FilePage(page) style ("SSSSS_pagination_textbutton_active" if page == int(renpy.store.persistent._file_page) else "SSSSS_pagination_textbutton")

                    if(pageOffset == 0):
                        text ""

                hbox at right:
                    spacing 10

                    textbutton _(">") action FilePageNext() style "SSSSS_pagination_textbutton"
                    textbutton _(">>") action FilePage(currentPage + 10) style "SSSSS_pagination_textbutton"
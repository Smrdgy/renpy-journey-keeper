screen SSSSS_Pagination():
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

    drag:
        draggable True
        drag_handle (-10, -10, paginationSize[0] + 20, paginationSize[1] + 20)
        align (.5, .999999) # For some reason (.5, 1) aligns it to the top...

        frame:
            background '#000000ee'
            xysize paginationSize

            ## Buttons to access other pages.
            grid 3 1:
                xfill True
                yalign 1.0
                spacing gui.page_spacing

                hbox at left:
                    spacing gui.page_spacing

                    textbutton _("⇇") action FilePage(max(currentPage - 10, 1))
                    hbox xsize 5
                    textbutton _("←") action FilePagePrevious()

                grid 10 1 at center:
                    spacing gui.page_spacing

                    for page in range(max(int(pageOffset * 10), 1), int(pageOffset * 10 + 10)):
                        textbutton "[page]" action FilePage(page)

                    if(pageOffset == 0):
                        text ""

                hbox at right:
                    spacing gui.page_spacing

                    textbutton _("→") action FilePageNext()
                    hbox xsize 5
                    textbutton _("⇉") action FilePage(currentPage + 10)
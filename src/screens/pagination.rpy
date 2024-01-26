screen SSSSS_Pagination():
    python:
        import math
        import sys

        isPython2 = sys.version_info[0] == 2

        currentPage = persistent._file_page
        if(currentPage == "quick" or currentPage == "auto"):
            currentPage = 1
        
        currentPage = int(currentPage)

        pageOffset = math.floor(currentPage / 10)

    fixed:
        ## Buttons to access other pages.
        grid 3 1:
            style_prefix "page"

            xfill True
            yalign 1.0
            spacing gui.page_spacing

            hbox at left:
                spacing gui.page_spacing

                textbutton _("<<") action FilePage(max(currentPage - 10, 1))
                if(isPython2):
                    textbutton _("<") action FilePagePrevious(max=1)
                else:
                    textbutton _("<") action FilePagePrevious(max=1, auto=False, quick=False)

            grid 10 1 at center:
                spacing gui.page_spacing

                for page in range(max(int(pageOffset * 10), 1), int(pageOffset * 10 + 10)):
                    textbutton "[page]" action FilePage(page)

                if(pageOffset == 0):
                    text ""

            hbox at right:
                spacing gui.page_spacing

                if(isPython2):
                    textbutton _(">") action FilePageNext()
                else:
                    textbutton _(">") action FilePageNext(auto=False, quick=False)
                textbutton _(">>") action FilePage(currentPage + 10)
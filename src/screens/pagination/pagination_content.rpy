screen JK_PaginationContent(content):
    python:
        try:
            currentPage = persistent._file_page
            if(currentPage == "quick" or currentPage == "auto"):
                currentPage = 0

            currentPage = int(currentPage)
        except:
            currentPage = 1

    frame:
        background "#000000{:02X}".format(int(JK.Settings.paginationOpacity * 255))

        hbox yalign 0.5:
            # Go-to
            if "GO_TO" in content:
                hbox yalign 0.5:
                    use JK_IconButton('\ue8a0', tt="Go to page", action=JK.Pagination.ToggleGoToPageAction(), size=30)

                use JK_XSpacer()

            # Quick & auto saves
            if "QUICK_SAVES" in content or "AUTOSAVES" in content:
                hbox yalign 0.5:
                    # Autosaves
                    if "AUTOSAVES" in content:
                        use JK_IconButton(text="A", action=FilePage("auto"), toggled=persistent._file_page == "auto", toggled_color=JK.Colors.selected, tt="Native automatic saves", size=25)

                    # Quick saves
                    if "QUICK_SAVES" in content:
                        use JK_IconButton(text="Q", action=FilePage("quick"), toggled=persistent._file_page == "quick", toggled_color=JK.Colors.selected, tt="Native quick saves", size=25)

                use JK_XSpacer()

            # |<, << and < buttons
            hbox yalign 0.5:
                # |<
                if "FIRST_PAGE" in content:
                    use JK_IconButton(icon="\ue045", action=FilePage(1), tt="First page", disabled=currentPage == 1)
                
                # <<
                if "BIG_JUMP" in content:
                    use JK_IconButton(icon="\ueac3", action=FilePage(max(currentPage - 10, 1)), tt=str(max(currentPage - 10, 1)), disabled=currentPage < 2)

                # <
                use JK_IconButton(icon="\ue5cb", action=FilePage(max(currentPage - 1, 1)), disabled=currentPage < 2)

            # Page numbers
            if "PAGE_NUMBERS" in content:
                hbox yalign 0.5:
                    for page in JK.Pagination.paginate(currentPage):
                        button:
                            style_prefix ("JK_PaginationButton_active" if page == currentPage else "JK_PaginationButton")
                            text (str(page) if page > 0 else "")

                            if page > 0:
                                action FilePage(page)

            # >, >> and >| buttons
            hbox yalign 0.5:
                # >
                use JK_IconButton(icon="\ue5cc", action=FilePageNext())

                # >>
                if "BIG_JUMP" in content:
                    $ next_jump_page = currentPage + (10 if currentPage > 1 else 9)
                    use JK_IconButton(icon="\ueac9", action=FilePage(next_jump_page), tt=str(next_jump_page))

                # >|
                if "LAST_PAGE" in content:
                    $ last_page = JK.SaveSystem.get_last_page()
                    use JK_IconButton(icon="\ue044", action=FilePage(last_page), tt="Last page ({})".format(last_page), disabled=last_page == None or currentPage == last_page)
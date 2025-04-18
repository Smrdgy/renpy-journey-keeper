init python in JK:
    _constant = True

    class PaginationClass(x52NonPicklable):
        @property
        def is_showing_pagination(self):
            return renpy.store.persistent.JK_ShowPagination or False

        @property
        def last_page(self):
            return SaveSystem.get_last_page()

        def get_content(self):
            content = []

            if Settings.paginationGoTo:
                content.append("GO_TO")
            if Settings.paginationQuickSaves:
                content.append("QUICK_SAVES")
            if Settings.paginationAutoSaves:
                content.append("AUTOSAVES")
            if Settings.paginationFirstPage:
                content.append("FIRST_PAGE")
            if Settings.paginationBigJump:
                content.append("BIG_JUMP")
            
            content.append("PREVIOUS_PAGE")
            if Settings.paginationNumbers:
                content.append("PAGE_NUMBERS")
            content.append("NEXT_PAGE")

            if Settings.paginationBigJump:
                content.append("BIG_JUMP")

            if Settings.paginationLastPage:
                content.append("LAST_PAGE")

            return content

        def get_content_width(self, content=None):
            item_size = 50
            width = 0

            content = content or self.get_content()

            for item in content:
                if item == "QUICK_SAVE" or item == "AUTO_SAVE":
                    width += scaled(30)
                elif item == "PAGE_NUMBERS":
                    width += scaled(60) * (9 if Settings.seamlessPagination else 10)
                else:
                    width += scaled(item_size)

            return width

        def paginate(self, current_page):
            if Settings.seamlessPagination:
                return self._paginate_seamlessly(current_page)

            return self._paginate_statically(current_page)

        def _paginate_statically(self, selected_page, visible_pages=10):
            offset = selected_page // visible_pages

            return list(range(offset * visible_pages, offset * visible_pages + visible_pages))

        def _paginate_seamlessly(self, selected_page, visible_pages=9):
            half_visible = visible_pages // 2

            start_page = max(1, selected_page - half_visible)
            end_page = start_page + visible_pages - 1

            return list(range(start_page, end_page + 1))

        class TogglePaginationAction(renpy.ui.Action):
            def __call__(self):
                renpy.store.persistent.JK_ShowPagination = not renpy.store.persistent.JK_ShowPagination
                renpy.restart_interaction()

        class ToggleGoToPageAction(renpy.ui.Action):
            def __call__(self):
                if renpy.get_screen("JK_GoToPage"):
                    renpy.hide_screen("JK_GoToPage")
                else:
                    renpy.show_screen("JK_GoToPage")

                renpy.restart_interaction()

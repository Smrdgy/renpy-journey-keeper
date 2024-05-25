init 1 python in SSSSS:
    _constant = True

    class PaginationClass(x52NonPicklable):
        showGoTo = False

        @property
        def isShowingPagination(self):
            return renpy.store.persistent.SSSSS_ShowPagination or False

        class TogglePagination(renpy.ui.Action):
            def __call__(self):
                if(Pagination.isShowingPagination):
                    renpy.hide_screen("SSSSS_Pagination")
                else:
                    renpy.show_screen("SSSSS_Pagination")

                renpy.store.persistent.SSSSS_ShowPagination = not renpy.store.persistent.SSSSS_ShowPagination
                renpy.restart_interaction()

        class ToggleGoToPage(renpy.ui.Action):
            def __call__(self):
                Pagination.showGoTo = not Pagination.showGoTo

                renpy.restart_interaction()

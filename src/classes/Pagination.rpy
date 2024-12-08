init 1 python in SSSSS:
    _constant = True

    class PaginationClass(x52NonPicklable):
        @property
        def isShowingPagination(self):
            return renpy.store.persistent.SSSSS_ShowPagination or False

        class TogglePagination(renpy.ui.Action):
            def __call__(self):
                renpy.store.persistent.SSSSS_ShowPagination = not renpy.store.persistent.SSSSS_ShowPagination
                renpy.restart_interaction()

        class ToggleGoToPage(renpy.ui.Action):
            def __call__(self):
                if renpy.get_screen("SSSSS_GoToPage"):
                    renpy.hide_screen("SSSSS_GoToPage")
                else:
                    renpy.show_screen("SSSSS_GoToPage")

                renpy.restart_interaction()

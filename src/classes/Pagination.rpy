init 1 python in URPS:
    _constant = True

    class PaginationClass(x52NonPicklable):
        @property
        def isShowingPagination(self):
            return renpy.store.persistent.URPS_ShowPagination or False

        class TogglePagination(renpy.ui.Action):
            def __call__(self):
                renpy.store.persistent.URPS_ShowPagination = not renpy.store.persistent.URPS_ShowPagination
                renpy.restart_interaction()

        class ToggleGoToPage(renpy.ui.Action):
            def __call__(self):
                if renpy.get_screen("URPS_GoToPage"):
                    renpy.hide_screen("URPS_GoToPage")
                else:
                    renpy.show_screen("URPS_GoToPage")

                renpy.restart_interaction()

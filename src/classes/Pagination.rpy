init python in JK:
    _constant = True

    class PaginationClass(x52NonPicklable):
        @property
        def isShowingPagination(self):
            return renpy.store.persistent.JK_ShowPagination or False

        class TogglePagination(renpy.ui.Action):
            def __call__(self):
                renpy.store.persistent.JK_ShowPagination = not renpy.store.persistent.JK_ShowPagination
                renpy.restart_interaction()

        class ToggleGoToPage(renpy.ui.Action):
            def __call__(self):
                if renpy.get_screen("JK_GoToPage"):
                    renpy.hide_screen("JK_GoToPage")
                else:
                    renpy.show_screen("JK_GoToPage")

                renpy.restart_interaction()

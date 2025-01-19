screen JK_GoToPage():
    layer "JK_Overlay"
    style_prefix 'JK'

    python:
        class Value(InputValue):
            def __init__(self):
                self.page = ""

            def get_text(self):
                return self.page

            def set_text(self, page):
                if(page.isdigit() or page == ""):
                    self.page = str(page)

                    page = int(page or 1)

                    if(page != renpy.store.persistent._file_page):
                        renpy.store.persistent._file_page = str(page)

                        renpy.restart_interaction()

    default page_input = JK.TextInput("page", value=Value(), auto_focus=True, allowed_characters="0123456789", max_length=6)

    use JK_TooltipDialog(follow_mouse=False):
        frame style "JK_default":
            xysize JK.scaled((90, 25))

            add page_input.displayable(placeholder=renpy.store.persistent._file_page)

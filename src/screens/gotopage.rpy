screen URPS_GoToPage():
    layer "URPS_Overlay"
    style_prefix 'URPS'

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

    default page_input = URPS.TextInput("page", value=Value(), auto_focus=True, allowed_characters="0123456789", max_length=6)

    use URPS_TooltipDialog():
        frame style "URPS_default":
            xysize adjustable((90, 25))

            add page_input.displayable(placeholder=renpy.store.persistent._file_page)

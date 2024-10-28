screen SSSSS_GoToPage():
    style_prefix 'SSSSS'
    modal True

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

    default value = Value()

    frame:
        xysize (0, 0)
        padding (0, 0, 0, 0)
        background None

        frame:
            style "SSSSS_frame"
            xysize adjustable((90, 40))
            xalign 0.5 yalign 1
            offset adjustable((-40, -60))
            background "#000000cc"

            use SSSSS_TextInput(placeholder=renpy.store.persistent._file_page, value=value, editable=True, layout="nobreak", offset=(-10, -15))

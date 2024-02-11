screen SSSSS_GoToPage():
    python:
        def setPage(page):
            if(page.isdigit() or page == ""):
                page = int(page or 1)

                if(page != renpy.store.persistent._file_page):
                    renpy.store.persistent._file_page = page

        page = renpy.store.persistent._file_page

    default inputs = x52URM.InputGroup(
        [
            ('page', x52URM.Input(text="", updateScreenVariable="page", onInput=setPage)),
        ],
        focusFirst=True,
    )

    frame:
        xysize (0, 0)
        background None

        frame:
            xysize (70, 40)
            xalign 0.5 yalign 1
            offset (-20, -40)
            background None

            frame:
                background "gui/goto.png"
                offset (-14, -7)

            button:
                style_prefix "" # Have to override some other styles that are applying for some reson...

                key_events True
                action inputs.page.Enable()

                input value inputs.page color '#fff'

                if(str(inputs.page) == ""):
                    text "[page]" color '#707070'

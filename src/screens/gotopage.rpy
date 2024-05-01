screen SSSSS_GoToPage():
    style_prefix 'SSSSS'

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
        padding (0, 0, 0, 0)
        background None

        frame:
            style "SSSSS_frame"
            xysize (90, 60)
            xalign 0.5 yalign 1
            offset (-40, -60)
            background "#000000cc"

            button:
                style_prefix "" # Have to override some other styles that are applying for some reson...

                key_events True
                action inputs.page.Enable()

                input value inputs.page color '#fff'

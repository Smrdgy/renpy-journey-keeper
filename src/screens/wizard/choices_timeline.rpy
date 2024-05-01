screen SSSSS_ChoicesTimeline(timeline):
    layer "SSSSSoverlay"
    style_prefix "SSSSS"

    use SSSSS_Dialog(title="Choices timeline", closeAction=Hide("SSSSS_ChoicesTimeline")):
        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            pagekeys True

            vbox:
                $ i = 1
                for entry in timeline:
                    hbox:
                        text "[i]." color "#bbe4ff"

                        text entry[1]

                        text "([entry[0]])" size 10 color "#4b4b4b"

                    $ i += 1
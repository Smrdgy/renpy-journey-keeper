screen SSSSS_ChoicesTimeline(timeline):
    use SSSSS_Dialog(title="Choices timeline", closeAction=Hide("SSSSS_ChoicesTimeline"), background="gui/select_playthrough_dialog_background.png", size=(x52URM.scalePxInt(581), x52URM.scalePxInt(623))):
        style_prefix "SSSSS"

        viewport:
            mousewheel True
            draggable
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
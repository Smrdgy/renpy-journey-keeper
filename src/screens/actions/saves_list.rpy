screen SSSSS_SavesList(saves=[]):
    layer "SSSSSoverlay"
    style_prefix "SSSSS"
    modal True

    $ savesLen = len(saves)

    use SSSSS_Dialog(title="Saves list", closeAction=Hide("SSSSS_SavesList")):
        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            pagekeys True

            vbox:
                text "{b}{color=#70bde6}[savesLen]{/c}{/b} saves found."
                
                hbox ysize 10

                for save_name in saves:
                    $ page, slot = SSSSS.Utils.splitSavename(save_name)

                    hbox:
                        button:
                            key_events True

                            action [FileLoad(slot, confirm=True, page=page), Hide("SSSSS_SavesList")]

                            text "[save_name]"
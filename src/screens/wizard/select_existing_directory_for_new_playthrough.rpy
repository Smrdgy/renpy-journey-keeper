screen URPS_SelectExistingDirectoryForNewPlaythrough():
    layer "URPS_Overlay"
    style_prefix 'URPS'
    modal True

    default directories = URPS.Playthroughs.list_available_directories_to_create_playthrough_from()

    use URPS_Dialog(title="Select directory", closeAction=Hide("URPS_SelectExistingDirectoryForNewPlaythrough")):
        style_prefix "URPS"

        if len(directories) > 0:
            viewport:
                mousewheel True
                draggable True
                scrollbars "vertical"
                pagekeys True
                ymaximum 0.85

                vbox:
                    $ i = 0
                    for dirname in directories:
                        $ i += 1

                        button style ("URPS_row_button" if i % 2 == 0 else "URPS_row_odd_button"):
                            xfill True

                            action [Hide("URPS_SelectExistingDirectoryForNewPlaythrough"), URPS.Playthroughs.ShowCreatePlaythroughFromDirname(dirname)]

                            text dirname

        else:
            hbox:
                xfill True
                yfill True
            
                hbox xalign 0.5 yalign 0.5:
                    use URPS_Title("No directories found.", color=URPS.Colors.error)
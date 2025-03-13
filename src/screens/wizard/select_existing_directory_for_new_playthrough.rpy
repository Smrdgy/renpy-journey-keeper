screen JK_SelectExistingDirectoryForNewPlaythrough():
    layer "JK_Overlay"
    style_prefix 'JK'
    modal True

    default directories = JK.Playthroughs.list_available_directories_to_create_playthrough_from()

    use JK_Dialog(title="Select directory", close_action=Hide("JK_SelectExistingDirectoryForNewPlaythrough")):
        style_prefix "JK"

        if len(directories) > 0:
            viewport:
                mousewheel True
                draggable True
                scrollbars "vertical"
                vscrollbar_unscrollable "hide"
                pagekeys True
                ymaximum 0.85

                vbox:
                    $ i = 0
                    for dirname in directories:
                        $ i += 1

                        button style ("JK_row_button" if i % 2 == 0 else "JK_row_odd_button"):
                            xfill True

                            action [Hide("JK_SelectExistingDirectoryForNewPlaythrough"), JK.Playthroughs.ShowCreatePlaythroughFromDirnameAction(dirname)]

                            text dirname

        else:
            hbox:
                xfill True
                yfill True
            
                hbox xalign 0.5 yalign 0.5:
                    use JK_Title("No directories found.", color=JK.Colors.error)
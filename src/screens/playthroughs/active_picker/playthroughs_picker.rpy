screen JK_PlaythroughsPicker():
    layer "JK_Overlay"
    style_prefix 'JK'
    modal True

    default reorder_source = None

    $ playthroughs = JK.Playthroughs.get_filtered_playthroughs()

    use JK_Dialog(title="Select a playthrough", close_action=Hide("JK_PlaythroughsPicker")):
        style_prefix "JK"

        hbox:
            xfill True

            # View mode buttons
            hbox:
                spacing 10
                xalign 0.5

                use JK_IconButton(icon="\ue5c3", text="Grid", action=JK.Settings.SetAction("playthroughsViewMode", "grid"), toggled=JK.Settings.playthroughsViewMode == "grid", toggled_color=JK.Colors.selected)
                use JK_IconButton(icon="\ue8e9", text="Rows", action=JK.Settings.SetAction("playthroughsViewMode", "rows"), toggled=JK.Settings.playthroughsViewMode == "rows", toggled_color=JK.Colors.selected)

        use JK_YSpacer(2)

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            vscrollbar_unscrollable "hide"
            pagekeys True
            ymaximum 0.9

            if JK.Settings.playthroughsViewMode == "grid":
                use JK_PlaythroughsGridPicker(playthroughs, reorder_source)
            elif JK.Settings.playthroughsViewMode == "rows":
                use JK_PlaythroughsTablePicker(playthroughs, reorder_source)            

        # Dialog footer
        hbox:
            xfill True
            yfill True

            style_prefix "JK_dialog_action_buttons"

            vbox xalign 0.0:
                # Overwrite
                hbox:
                    if JK.UserDir.is_available:
                        use JK_IconButton(icon="\ue884", text="Import from another game", action=Show("JK_ImportPlaythroughs"))

            vbox xalign 1.0:
                # Close
                hbox:
                    use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_PlaythroughsPicker"))
screen URPS_Sidepanel():
    style_prefix 'URPS'
    default estimatedPanelSize = URPS.adjustable((80, 350))

    python:
        _constant = True

        playthrough = URPS.Playthroughs.activePlaythrough
        noPlaythrough = playthrough == None
        autosave_on_choices_enabled = playthrough and playthrough.autosaveOnChoices
        custom_pagination_enabled = renpy.store.persistent.URPS_ShowPagination
        sidepanelPos = store.persistent.URPS_sidepanelPos or (int(renpy.config.screen_width - estimatedPanelSize[0] - 15), int(renpy.config.screen_height / 2 - estimatedPanelSize[1] / 2))
        tooltip_side = "left" if sidepanelPos[0] > renpy.config.screen_width / 2 else "right"
        amount_of_playthroughs = len(URPS.Playthroughs.playthroughs) - 1

        def sidepanel_dragged(drags, drop):
            renpy.store.persistent.URPS_sidepanelPos = (drags[0].x, drags[0].y)

    if URPS.Settings.debugEnabled:
        frame:
            background "#ff0000cc"
            xysize estimatedPanelSize
            xpos sidepanelPos[0]
            ypos sidepanelPos[1]

    drag:
        draggable True
        drag_handle (0, 0, 1.0, 1.0)
        xpos sidepanelPos[0]
        ypos sidepanelPos[1]
        droppable False
        dragged sidepanel_dragged

        frame:
            background "#000000cc"

            vbox:
                use URPS_IconButton('\ueb73', tt="Select playthrough", ttSide=tooltip_side, action=Show("URPS_PlaythroughsPicker")):
                    frame xysize (0, 0) offset URPS.adjustable((-10, -5)) style "URPS_default":
                        if amount_of_playthroughs > 1:
                            text "{b}[amount_of_playthroughs]{/b}" size URPS.adjustable(15) outlines [(5, "#000000", 0, 0)] color URPS.Colors.theme

                use URPS_IconButton('\uea20', tt="New playthrough", ttSide=tooltip_side, action=Show("URPS_EditPlaythrough", playthrough=None))
                use URPS_IconButton('\ue02c', tt="Open memories", ttSide=tooltip_side, action=Show("URPS_MemoriesLibrary"), disabled=not URPS.Settings.memoriesEnabled)

                use URPS_Divider(sizeX=40)

                use URPS_IconButton('\ue3c9', tt="Edit playthrough", ttSide=tooltip_side, action=Show("URPS_EditPlaythrough", playthrough=playthrough.copy(), isEdit=True), disabled=noPlaythrough)
                use URPS_IconButton('\ue4f9', toggled=autosave_on_choices_enabled, toggledIcon='\ue167', tt=("Disable autosave on choices" if autosave_on_choices_enabled else "Enable autosave on choices"), ttSide=tooltip_side, action=URPS.Playthroughs.ToggleAutosaveOnChoicesOnActive(), disabled=noPlaythrough or not URPS.Utils.hasColsAndRowsConfiguration(), toggledColor=URPS.Colors.selected)
                use URPS_IconButton('\ue2e6', tt="Playthrough actions", ttSide=tooltip_side, action=Show("URPS_PlaythroughActions", playthrough=playthrough))

                use URPS_Divider(sizeX=40)

                use URPS_IconButton('\ue666', tt=("Hide custom pagination" if custom_pagination_enabled else "Show custom pagination"), ttSide=tooltip_side, action=URPS.Pagination.TogglePagination(), toggled=custom_pagination_enabled, toggledColor=URPS.Colors.selected)
                use URPS_IconButton('\ue8b8', tt="Open settings", ttSide=tooltip_side, action=Show("URPS_Settings"))


screen URPS_SidepanelHolder():
    layer "URPS_Sidepanel"

    key URPS.Settings.changeSidepanelVisibilityKey action URPS.ToggleSidepanel()

    python:
        isSaveLoadScreen = URPS.Utils.is_save_load_screen()
        visibilityMode = renpy.config.URPS_sidepanelVisibilityMode if hasattr(renpy.config, "URPS_sidepanelVisibilityMode") else isSaveLoadScreen
        sidepanelShouldBeVisible = isSaveLoadScreen if visibilityMode == None else visibilityMode
        preventSidepanel = URPS.Memories.memoryInProgress
        showSidepanel = not preventSidepanel and sidepanelShouldBeVisible

    if showSidepanel:
        use URPS_Sidepanel()

    if(showSidepanel and isSaveLoadScreen and URPS.Pagination.isShowingPagination):
        use URPS_Pagination()
    else:
        $ renpy.hide_screen("URPS_GoToPage")
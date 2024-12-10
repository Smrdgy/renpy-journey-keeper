screen URPS_Sidepanel():
    style_prefix 'URPS'
    default estimatedPanelSize = adjustable((80, 350))

    python:
        _constant = True

        playthrough = URPS.Playthroughs.activePlaythrough
        noPlaythrough = playthrough == None
        sidepanelPos = store.persistent.URPS_sidepanelPos or (int(renpy.config.screen_width - estimatedPanelSize[0] - 15), int(renpy.config.screen_height / 2 - estimatedPanelSize[1] / 2))

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
                use URPS_IconButton('\ueb73', tt="Select playthrough", ttSide="left", action=Show("URPS_PlaythroughsPicker"))
                use URPS_IconButton('\uea20', tt="New playthrough", ttSide="left", action=Show("URPS_EditPlaythrough", playthrough=None))
                use URPS_IconButton('\ue02c', tt="Open memories", ttSide="left", action=Show("URPS_MemoriesLibrary"), disabled=not URPS.Settings.memoriesEnabled)

                use URPS_Divider(sizeX=40)

                use URPS_IconButton('\ue3c9', tt="Edit playthrough", ttSide="left", action=Show("URPS_EditPlaythrough", playthrough=playthrough.copy(), isEdit=True), disabled=noPlaythrough)
                use URPS_IconButton('\ue4f9', toggled=playthrough and playthrough.autosaveOnChoices, toggledIcon='\ue167', tt="Autosave on choices", ttSide="left", action=URPS.Playthroughs.ToggleAutosaveOnChoicesOnActive(), disabled=noPlaythrough or not URPS.Utils.hasColsAndRowsConfiguration())
                use URPS_IconButton('\ue2e6', tt="Playthrough actions", ttSide="left", action=Show("URPS_PlaythroughActions", playthrough=playthrough))

                use URPS_Divider(sizeX=40)

                use URPS_IconButton('\ue666', tt="Custom pagination", ttSide="left", action=URPS.Pagination.TogglePagination(), toggled=renpy.store.persistent.URPS_ShowPagination, toggledColor=URPS.Colors.selected)
                use URPS_IconButton('\ue8b8', tt="Settings", ttSide="left", action=Show("URPS_Settings"))


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
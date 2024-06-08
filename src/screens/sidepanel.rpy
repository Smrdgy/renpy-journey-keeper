screen SSSSS_Sidepanel():
    style_prefix 'SSSSS'
    default estimatedPanelSize = (80, 350)

    python:
        _constant = True

        playthrough = SSSSS.Playthroughs.activePlaythrough
        noPlaythrough = playthrough == None
        sidepanelPos = store.persistent.SSSSS_sidepanelPos or (int(renpy.config.screen_width - estimatedPanelSize[0] - 15), int(renpy.config.screen_height / 2 - estimatedPanelSize[1] / 2))

        def sidepanel_dragged(drags, drop):
            renpy.store.persistent.SSSSS_sidepanelPos = (drags[0].x, drags[0].y)

    if renpy.config.developer:
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
                use sssss_iconButton('\ueb73', tt="Open list of playthroughs", action=Show("SSSSS_PlaythroughsPicker"))
                use sssss_iconButton('\uea20', tt="New playthrough", action=Show("SSSSS_EditPlaythrough", playthrough=None))
                use sssss_iconButton('\ue02c', tt="Open memories", action=Show("SSSSS_MemoriesLibrary"))

                use SSSSS_Divider(sizeX=40)

                use sssss_iconButton('\ue3c9', tt="Edit playthrough", action=Show("SSSSS_EditPlaythrough", playthrough=playthrough.copy(), isEdit=True), disabled=noPlaythrough)
                use sssss_iconButton('\ue4f9', toggled=playthrough and playthrough.autosaveOnChoices, toggledIcon='\ue167', tt="Autosave on choices", action=SSSSS.Playthroughs.ToggleAutosaveOnChoicesOnActive(), disabled=noPlaythrough or not SSSSS.hasColsAndRowsConfiguration)
                use sssss_iconButton('\ue2e6', tt="Actions", action=Show("SSSSS_PlaythroughActions", playthrough=playthrough))

                use SSSSS_Divider(sizeX=40)

                use sssss_iconButton('\ue666', tt="Custom pagination", action=SSSSS.Pagination.TogglePagination())
                # use sssss_iconButton('\ue8b8', tt="Settings", action=Show("SSSSS_Settings"), disabled=True)


screen SSSSS_SidepanelHolder():
    layer "SSSSSsidepanel"

    key "alt_K_p" action SSSSS.ToggleSidepanel()

    python:
        isSaveLoadScreen = renpy.get_screen("load") != None or renpy.get_screen("save") != None
        visibilityMode = renpy.config.SSSSS_sidepanelVisibilityMode if hasattr(renpy.config, "SSSSS_sidepanelVisibilityMode") else isSaveLoadScreen
        sidepanelShouldBeVisible = isSaveLoadScreen if visibilityMode == None else visibilityMode
        preventSidepanel = SSSSS.Memories.memoryInProgress
        showSidepanel = not preventSidepanel and sidepanelShouldBeVisible

    if(showSidepanel):
        use SSSSS_Sidepanel()
    else:
        $ SSSSS.Pagination.showGoTo = False

    if(showSidepanel and isSaveLoadScreen and SSSSS.Pagination.isShowingPagination):
        use SSSSS_Pagination()
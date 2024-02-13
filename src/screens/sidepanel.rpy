screen SSSSS_Sidepanel():
    default panelSize = (60, 366)

    python:
        _constant = True

        newPlaythrough = SSSSS.Playthroughs.PlaythroughClass()
        playthrough = SSSSS.Playthroughs.activePlaythrough
        noPlaythrough = playthrough == None
        sidepanelPos = store.persistent.SSSSS_sidepanelAlign or (renpy.config.screen_width - panelSize[0] - 15, renpy.config.screen_height / 2 - panelSize[1] / 2)

        def sidepanel_dragged(drags, drop):
            renpy.store.persistent.SSSSS_sidepanelAlign = (drags[0].x, drags[0].y)

    drag:
        draggable True
        drag_handle (0, -20, 1.0, panelSize[1])
        xpos sidepanelPos[0]
        ypos sidepanelPos[1]
        droppable False
        dragged sidepanel_dragged

        frame:
            xysize panelSize
            background None

            frame:
                background "gui/sidepanel.png"
                xfill True
                yfill True
                offset (-15, -20)

            vbox:
                use sssss_iconButton('\ueb73', tt=_("Open list of playthroughs"), action=Show("SSSSS_PlaythroughsPicker"))
                use sssss_iconButton('\uea20', tt=_("New playthrough"), action=Show("SSSSS_EditPlaythrough", playthrough=newPlaythrough))
                use sssss_iconButton('\ue02c', tt=_("Open memories"), action=Show("SSSSS_MemoriesList"), disabled=True)

                use SSSSS_Divider(sizeX=panelSize[0] - 10)

                use sssss_iconButton('\ue3c9', tt=_("Edit playthrough"), action=Show("SSSSS_EditPlaythrough", playthrough=playthrough, isEdit=True), disabled=noPlaythrough)
                use sssss_iconButton('\ue4f9', toggled=playthrough and playthrough.autosaveOnChoices, toggledIcon='\ue167', tt=_("Autosave on choices"), action=SSSSS.Playthroughs.ToggleAutosaveOnChoicesOnActive(), disabled=noPlaythrough)
                use sssss_iconButton('\ue2e6', tt=_("Actions"), action=Show("SSSSS_PlaythroughActions", playthrough=playthrough))

                use SSSSS_Divider(sizeX=panelSize[0] - 10)

                use sssss_iconButton('\ue666', tt=_("Custom pagination"), action=SSSSS.Pagination.TogglePagination())
                # use sssss_iconButton('\ue8b8', tt="Settings", action=Show("SSSSS_Settings"), disabled=True)


screen SSSSS_SidepanelHolder():
    layer "SSSSSsidepanel"

    key "K_SCROLLOCK" action SSSSS.ToggleSidepanel()

    python:
        isSaveLoadScreen = renpy.get_screen("load") != None or renpy.get_screen("save") != None or (hasattr(renpy.config, "SSSSS_show_sidepanel") and renpy.config.SSSSS_show_sidepanel)

    # if is in save/load menu
    if(isSaveLoadScreen):
        use SSSSS_Sidepanel()

    if(isSaveLoadScreen and SSSSS.Pagination.isShowingPagination):
        use SSSSS_Pagination()
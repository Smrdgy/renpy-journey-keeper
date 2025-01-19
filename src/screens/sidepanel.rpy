screen JK_Sidepanel():
    style_prefix 'JK'
    default estimatedPanelSize = JK.scaled((80, 350))

    python:
        _constant = True

        playthrough = JK.Playthroughs.activePlaythrough
        noPlaythrough = playthrough == None
        autosave_on_choices_enabled = playthrough and playthrough.autosaveOnChoices
        custom_pagination_enabled = renpy.store.persistent.JK_ShowPagination
        sidepanelPos = store.persistent.JK_SidepanelPos or (int(renpy.config.screen_width - estimatedPanelSize[0] - 15), int(renpy.config.screen_height / 2 - estimatedPanelSize[1] / 2))
        tooltip_side = "left" if sidepanelPos[0] > renpy.config.screen_width / 2 else "right"
        amount_of_playthroughs = len(JK.Playthroughs.playthroughs) - 1

        def sidepanel_dragged(drags, drop):
            renpy.store.persistent.JK_SidepanelPos = (drags[0].x, drags[0].y)

    if JK.Settings.debugEnabled:
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
                use JK_IconButton('\ueb73', tt="Select playthrough", ttSide=tooltip_side, action=Show("JK_PlaythroughsPicker")):
                    frame xysize (0, 0) offset JK.scaled((-10, -5)) style "JK_default":
                        if amount_of_playthroughs > 1:
                            text "{b}[amount_of_playthroughs]{/b}" size JK.scaled(15) outlines [(JK.scaled(5), "#000000", 0, 0)] color JK.Colors.theme

                use JK_IconButton('\uea20', tt="New playthrough", ttSide=tooltip_side, action=Show("JK_EditPlaythrough", playthrough=None))
                use JK_IconButton('\ue02c', tt="Open memories", ttSide=tooltip_side, action=Show("JK_MemoriesLibrary"), disabled=not JK.Settings.memoriesEnabled)

                use JK_Divider(sizeX=40)

                use JK_IconButton('\ue3c9', tt="Edit playthrough", ttSide=tooltip_side, action=Show("JK_EditPlaythrough", playthrough=playthrough.copy(), isEdit=True), disabled=noPlaythrough)
                use JK_IconButton('\ue4f9', toggled=autosave_on_choices_enabled, toggledIcon='\ue167', tt=("Disable autosave on choices" if autosave_on_choices_enabled else "Enable autosave on choices"), ttSide=tooltip_side, action=JK.Playthroughs.ToggleAutosaveOnChoicesOnActive(), disabled=noPlaythrough or not JK.Utils.hasColsAndRowsConfiguration(), toggledColor=JK.Colors.selected)
                use JK_IconButton('\ue2e6', tt="Playthrough actions", ttSide=tooltip_side, action=Show("JK_PlaythroughActions", playthrough=playthrough))

                use JK_Divider(sizeX=40)

                use JK_IconButton('\ue666', tt=("Hide custom pagination" if custom_pagination_enabled else "Show custom pagination"), ttSide=tooltip_side, action=JK.Pagination.TogglePagination(), toggled=custom_pagination_enabled, toggledColor=JK.Colors.selected)
                use JK_IconButton('\ue8b8', tt="Open settings", ttSide=tooltip_side, action=Show("JK_Settings"))


screen JK_SidepanelHolder():
    layer "JK_Sidepanel"

    key JK.Settings.changeSidepanelVisibilityKey action JK.ToggleSidepanel()

    python:
        isSaveLoadScreen = JK.Utils.is_save_load_screen()
        visibilityMode = renpy.config.JK_sidepanelVisibilityMode if hasattr(renpy.config, "JK_sidepanelVisibilityMode") else isSaveLoadScreen
        sidepanelShouldBeVisible = isSaveLoadScreen if visibilityMode == None else visibilityMode
        preventSidepanel = JK.Memories.memoryInProgress
        showSidepanel = not preventSidepanel and sidepanelShouldBeVisible

    if showSidepanel:
        use JK_Sidepanel()

    if(showSidepanel and isSaveLoadScreen and JK.Pagination.isShowingPagination):
        use JK_Pagination()
    else:
        $ renpy.hide_screen("JK_GoToPage")
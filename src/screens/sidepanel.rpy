screen JK_Sidepanel():
    style_prefix 'JK'

    python:
        _constant = True

        structure = ["PLAYTHROUGHS", "NEW_PLAYTHROUG", "MEMORIES", "DIVIDER", "EIDT_PLAYTHROUGH", "TOGGLE_AUTOSAVE", "PLAYTHROUGH_ACTIONS", "DIVIDER", "PAGINATION", "SETTINGS"]

        if not JK.Settings.memoriesEnabled:
            structure.remove("MEMORIES")

        horizontal = JK.Settings.sidepanelHorizontal

        def calculate_structure_size(structure):
            item_size = 40
            divider_size = 17

            size = 0
            for item in structure:
                if item == "DIVIDER":
                    size += JK.scaled(divider_size)
                else:
                    size += JK.scaled(item_size)
            
            return size

        playthrough = JK.Playthroughs.active_playthrough
        noPlaythrough = playthrough == None
        autosave_on_choices_enabled = playthrough and playthrough.autosaveOnChoices
        custom_pagination_enabled = renpy.store.persistent.JK_ShowPagination
        playthroughs = JK.Playthroughs.get_filtered_playthroughs()
        amount_of_playthroughs = len(playthroughs)
        amount_of_custom_playthroughs = len([p for p in playthroughs if not p.native])

        if horizontal:
            estimatedPanelSize = (calculate_structure_size(structure), JK.scaled(70))
            sidepanelPos = store.persistent.JK_SidepanelPos or (int(renpy.config.screen_width / 2 - estimatedPanelSize[0] / 2), 15)
            tooltip_side = "top" if sidepanelPos[1] > renpy.config.screen_height / 2 else "bottom"            
        else:
            estimatedPanelSize = (JK.scaled(70), calculate_structure_size(structure))
            sidepanelPos = store.persistent.JK_SidepanelPos or (int(renpy.config.screen_width - estimatedPanelSize[0] - 15), int(renpy.config.screen_height / 2 - estimatedPanelSize[1] / 2))
            tooltip_side = "left" if sidepanelPos[0] > renpy.config.screen_width / 2 else "right"

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
            background "#000000{:02X}".format(int(JK.Settings.sidepanelOpacity * 255))

            use JK_AnyDirectionBox(horizontal):
                use JK_IconButton('\ueb73', tt="Select playthrough", tt_side=tooltip_side, action=Show("JK_PlaythroughsPicker")):
                    frame xysize (0, 0) offset JK.scaled((-10, -5)) style "JK_default":
                        if amount_of_custom_playthroughs > 0:
                            text "{b}[amount_of_playthroughs]{/b}" size JK.scaled(15) outlines [(JK.scaled(5), "#000000", 0, 0)] color JK.Colors.theme

                use JK_IconButton('\uea20', tt="New playthrough", tt_side=tooltip_side, action=Show("JK_EditPlaythrough", playthrough=None))

                if "MEMORIES" in structure:
                    use JK_IconButton('\ue02c', tt="Open memories", tt_side=tooltip_side, action=Show("JK_MemoriesLibrary"))

                use JK_Divider(sizeX=(2 if horizontal else 40), sizeY=(40 if horizontal else 2))

                use JK_IconButton('\ue3c9', tt="Edit playthrough", tt_side=tooltip_side, action=Show("JK_EditPlaythrough", playthrough=playthrough.copy(), isEdit=True), disabled=noPlaythrough)
                use JK_IconButton('\ue4f9', toggled=autosave_on_choices_enabled, toggled_icon='\ue167', tt=("Disable autosave on choices" if autosave_on_choices_enabled else "Enable autosave on choices"), tt_side=tooltip_side, action=JK.Playthroughs.ToggleAutosaveOnChoicesForActiveAction(), disabled=noPlaythrough or not JK.Utils.has_cols_and_rows_configuration(), toggled_color=JK.Colors.selected)
                use JK_IconButton('\ue2e6', tt="Playthrough actions", tt_side=tooltip_side, action=Show("JK_PlaythroughActions", playthrough=playthrough))

                use JK_Divider(sizeX=(2 if horizontal else 40), sizeY=(40 if horizontal else 2))

                use JK_IconButton('\uf045', tt=("Hide custom pagination" if custom_pagination_enabled else "Show custom pagination"), tt_side=tooltip_side, action=JK.Pagination.TogglePaginationAction(), toggled=custom_pagination_enabled, toggled_color=JK.Colors.selected)
                use JK_IconButton('\ue8b8', tt="Open settings", tt_side=tooltip_side, action=Show("JK_Settings"))

screen JK_SidepanelHolder():
    layer "JK_Sidepanel"

    if JK.Settings.changeSidepanelVisibilityKey:
        key JK.Settings.changeSidepanelVisibilityKey action JK.ToggleSidepanel()

    python:
        isSaveLoadScreen = JK.Utils.is_save_load_screen()
        visibilityMode = renpy.config.JK_sidepanelVisibilityMode if hasattr(renpy.config, "JK_sidepanelVisibilityMode") else isSaveLoadScreen
        sidepanelShouldBeVisible = isSaveLoadScreen if visibilityMode == None else visibilityMode
        preventSidepanel = JK.Memories.memoryInProgress
        showSidepanel = not preventSidepanel and sidepanelShouldBeVisible

    if showSidepanel:
        use JK_Sidepanel()

        # Allow search only inside save/load screens
        if JK.Settings.searchPlaythroughKey and isSaveLoadScreen:
            key JK.Settings.searchPlaythroughKey action Show("JK_SearchPlaythrough")

        if JK.Settings.searchPlaythroughsKey and isSaveLoadScreen:
            key JK.Settings.searchPlaythroughsKey action Show("JK_SearchPlaythrough", search_all=True)

    if(showSidepanel and isSaveLoadScreen and JK.Pagination.is_showing_pagination):
        use JK_Pagination()
    else:
        $ renpy.hide_screen("JK_GoToPage")

init python in JK:
    _constant = True

    class ToggleSidepanel(renpy.ui.Action):
        def __call__(self):
            if not hasattr(renpy.config, "JK_sidepanelVisibilityMode") or renpy.config.JK_sidepanelVisibilityMode == None:
                # Visible at all times
                SetSidepanelVisibilityAction(visibility=True)()
            elif renpy.config.JK_sidepanelVisibilityMode == True:
                # Hidden at all times
                SetSidepanelVisibilityAction(visibility=False)()
            elif renpy.config.JK_sidepanelVisibilityMode == False:
                # Visible only in save/load screen
                SetSidepanelVisibilityAction(visibility=None)()
            else:
                # Visible at all times
                SetSidepanelVisibilityAction(visibility=True)()

            renpy.restart_interaction()
        
    class SetSidepanelVisibilityAction(renpy.ui.Action):
        def __init__(self, visibility):
            self.visibility = visibility # True/False/None

        def __call__(self):
            renpy.config.JK_sidepanelVisibilityMode = self.visibility

            if renpy.config.JK_sidepanelVisibilityMode == True:
                renpy.notify("Sidepanel is now visible at all times")
            elif renpy.config.JK_sidepanelVisibilityMode == False:
                renpy.notify("Sidepanel is now hidden at all times")
            elif renpy.config.JK_sidepanelVisibilityMode == None:
                renpy.notify("Sidepanel is now visible only on the save/load screen")
            else:
                renpy.notify("Sidepanel is now visible at all times")

            renpy.restart_interaction()
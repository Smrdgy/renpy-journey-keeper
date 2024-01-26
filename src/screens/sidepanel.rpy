screen SSSSS_Sidepanel():
    default panelSize = (60, 366)

    python:
        newPlaythrough = SSSSS.Playthroughs.PlaythroughClass()
        playthrough = SSSSS.Playthroughs.activePlaythrough
        noPlaythrough = playthrough == None

    drag:
        draggable True
        drag_handle (0, -20, 1.0, panelSize[1])
        align (.99999999,.5) # For some reason (1, .5) aligns it to the left...

        frame:
            xysize panelSize
            background None

            frame:
                background "assets/gui/sidepanel.png"
                xfill True
                yfill True
                offset (-15, -20)

            vbox:
                use sssss_iconButton('\ueb73', tt="Open list of playthroughs", action=Show("SSSSS_PlaythroughsPicker"))
                use sssss_iconButton('\ue02c', tt="Open memories", action=Show("SSSSS_MemoriesList"), disabled=True)
                use sssss_iconButton('\uea20', tt="New playthrough", action=Show("SSSSS_EditPlaythrough", playthrough=newPlaythrough))

                use SSSSS_Divider(sizeX=panelSize[0] - 10)

                use sssss_iconButton('\ue3c9', tt="Edit playthrough", action=Show("SSSSS_EditPlaythrough", playthrough=playthrough, isEdit=True), disabled=noPlaythrough)
                use sssss_iconButton('\ue4f9', toggled=playthrough and playthrough.autosaveOnChoices, toggledIcon='\ue167', tt="Autosave on choices", action=SSSSS.Playthroughs.ToggleAutosaveOnChoicesOnActive(), disabled=noPlaythrough)

                use SSSSS_Divider(sizeX=panelSize[0] - 10)

                use sssss_iconButton('\ue5d3', tt="Custom pagination", action=Show("SSSSS_Pagination"))
                use sssss_iconButton('\ue8b8', tt="Settings", action=Show("SSSSS_Settings"), disabled=True)


screen SSSSS_SidepanelHolder():
    layer "SSSSSsidepanel"

    python:
        print(renpy.current_screen().screen_name[0])
        isSaveLoadScreen = renpy.get_screen("load") != None or renpy.get_screen("save") != None

    # if is in save/load menu
    if(isSaveLoadScreen):
        use SSSSS_Sidepanel()
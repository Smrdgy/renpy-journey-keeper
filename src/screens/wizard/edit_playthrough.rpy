screen SSSSS_EditPlaythrough(playthrough, isEdit=False):
    layer "SSSSSoverlay"
    style_prefix 'SSSSS'
    modal True

    $ playthrough = playthrough or SSSSS.Playthroughs.PlaythroughClass()

    default name = playthrough.name or ''
    default originalname = name
    default description = playthrough.description or ''
    default storeChoices = playthrough.storeChoices
    default autosaveOnChoices = playthrough.autosaveOnChoices
    default useChoiceLabelAsSaveName = playthrough.useChoiceLabelAsSaveName
    default enabledSaveLocations = playthrough.enabledSaveLocations
    default moveSaveDirectory = True
    #MODIFY HERE

    python:
        submitAction = [
            SSSSS.Playthroughs.AddOrEdit(playthrough=playthrough, name=URMGetScreenVariable('name'), description=URMGetScreenVariable('description'), storeChoices=URMGetScreenVariable('storeChoices'), autosaveOnChoices=URMGetScreenVariable('autosaveOnChoices'), useChoiceLabelAsSaveName=URMGetScreenVariable('useChoiceLabelAsSaveName'), enabledSaveLocations=URMGetScreenVariable('enabledSaveLocations'), moveSaveDirectory=URMGetScreenVariable('moveSaveDirectory')),#MODIFY HERE
            Hide('SSSSS_EditPlaythrough')
        ]

    key 'ctrl_K_s' action submitAction
    key 'ctrl_K_DELETE' action Show("SSSSS_RemovePlaythroughConfirm", playthrough=playthrough)

    use SSSSS_Dialog(title=("Edit playthrough" if isEdit else "New playthrough"), closeAction=Hide("SSSSS_EditPlaythrough")):
        style_prefix "SSSSS"

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            pagekeys True
            ymaximum 0.85

            vbox:
                text "Name:"

                add SSSSS.TextInput(id="name", variableName="name", editable=True)

                if(name != originalname and not SSSSS.Playthroughs.isValidName(name)):
                    text "Are you sure? This name already exists." color '#ffb14c' offset (15, 2)

                if(playthrough.id != 1):
                    python:
                        computedDirectory = playthrough.directory if (playthrough.directory != None) else (SSSSS.Utils.name_to_directory_name(name) if name else None) or ""

                    text "Directory:"
                    hbox:
                        offset (15, 0)

                        text "saves/" color '#e5e5e5'
                        text "[computedDirectory]" color '#a2ebff'

                        if isEdit:
                            use sssss_iconButton(icon="\ue2c8", action=SSSSS.OpenDirectoryAction(path=computedDirectory, cwd=renpy.config.savedir), size=20)
                        else:
                            use sssss_iconButton(icon="\ue2c8", action=SSSSS.OpenDirectoryAction(path=renpy.config.savedir), size=20)

                    $ allSaveLocations = SSSSS.SaveSystem.getAllNativeSaveLocationsForOptions()

                    if(isEdit and playthrough.id > 1 and name != originalname and SSSSS.Playthroughs.isValidName(name)):
                        use SSSSS_Checkbox(checked=moveSaveDirectory, text="Rename directory as well", action=ToggleScreenVariable('moveSaveDirectory', True, False), disabled=not SSSSS.Playthroughs.isValidName(name))

                    use SSSSS_Checkbox(checked=enabledSaveLocations != None, text="Manage save locations", action=ToggleScreenVariable('enabledSaveLocations', [] + allSaveLocations, None))

                    if enabledSaveLocations != None:
                        vbox:
                            xoffset 30

                            for location in allSaveLocations:
                                python:
                                    locationType = "Extra"
                                    path = location

                                    # User savedir (appdata or library).
                                    if location == "USER":
                                        locationType = "Library" if renpy.macapp else "%APPDATA%"
                                        path = renpy.config.savedir
                                    # Game-local savedir.
                                    elif location == "GAME":
                                        locationType = "Game files"
                                        path = os.path.join(renpy.config.gamedir, "saves")

                                    fullPath = os.path.join(path, computedDirectory)

                                hbox:
                                    use SSSSS_Checkbox(checked=location in enabledSaveLocations, text=locationType + " - {color=#818181}{size=-5}" + fullPath + "{/size}{/c}", action=SSSSS.ToggleValueInArrayAction('enabledSaveLocations', location))

                                    hbox at truecenter:
                                        if isEdit:
                                            use sssss_iconButton(icon="\ue2c8", action=SSSSS.OpenDirectoryAction(path=fullPath), size=15, color="#818181")
                                        else:
                                            use sssss_iconButton(icon="\ue2c8", action=SSSSS.OpenDirectoryAction(path=path), size=15, color="#818181")

                            if len(enabledSaveLocations) == 0:
                                hbox ysize 10
                                text "At least one location must be enabled!" color '#ff4c4c' xoffset 10

                hbox ysize 10

                text "Description:"
                add SSSSS.TextInput(id="description", variableName="description", multiline=True)

                hbox ysize 10

                text "Options:"
                hbox:
                    xfill True

                    vbox:
                        use SSSSS_Checkbox(checked=autosaveOnChoices, text="Autosave on choice", action=ToggleScreenVariable('autosaveOnChoices', True, False), disabled=not SSSSS.hasColsAndRowsConfiguration)
                        if not SSSSS.hasColsAndRowsConfiguration:
                            text "{size=-10}This game uses an unusual save system, thus autosave is not possible{/size}" color "#ff4c4c" offset (35, -10)

                        hbox:
                            offset (15, 0)

                            use SSSSS_Checkbox(checked=useChoiceLabelAsSaveName, text="Use choice text as a save name\n{size=13}(Applies only for the saves created by this mod's autosave system!){/size}", action=ToggleScreenVariable('useChoiceLabelAsSaveName', True, False), disabled=not SSSSS.hasColsAndRowsConfiguration or not autosaveOnChoices)

                hbox ysize 10

                if isEdit:
                    text "Thumbnail:"
                    hbox:
                        frame:
                            xysize (160, 160)

                            if playthrough.hasThumbnail():
                                add playthrough.getThumbnail(width=150, maxHeight=150)
                            else:
                                button:
                                    style_prefix ""
                                    action None
                                    xalign 0.5
                                    yalign 0.5

                                    use sssss_icon(icon="\ue3f4", color="#333")


                        vbox:
                            # Set thumbnail
                            use sssss_iconButton(icon="\ue3f4", text="Use current scene as thumbnail", action=SSSSS.Playthroughs.SetThumbnail(playthrough=playthrough))

                            # Remove thumbnail
                            if playthrough.hasThumbnail():
                                use sssss_iconButton(icon="\ue92b", text="Remove thumbnail", action=SSSSS.Playthroughs.RemoveThumbnail(playthrough=playthrough), color="#ff0000")

        hbox:
            xfill True
            yfill True

            vbox at right:
                yalign 1.0

                if(isEdit and playthrough.id != 1):
                    # Remove
                    hbox at right:
                        use sssss_iconButton(icon="\ue92b", text="{u}R{/u}emove", action=Show("SSSSS_RemovePlaythroughConfirm", playthrough=playthrough), color="#ff0000")

                # Save
                hbox at right:
                    use sssss_iconButton(icon="\ue161", text="{u}S{/u}ave", action=submitAction, disabled=(enabledSaveLocations != None and len(enabledSaveLocations) == 0) or len(name) == 0)

                # Close
                hbox at right:
                    use sssss_iconButton(icon="\ue5cd", text="Close", action=Hide("SSSSS_EditPlaythrough"))
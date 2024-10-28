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
    default enabledSaveLocations = playthrough.enabledSaveLocations or False
    default moveSaveDirectory = True
    #MODIFY HERE

    python:
        submitAction = [
            SSSSS.Playthroughs.AddOrEdit(playthrough, name, description, storeChoices, autosaveOnChoices, useChoiceLabelAsSaveName, enabledSaveLocations, moveSaveDirectory),#MODIFY HERE
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
                use SSSSS_Title("Name")

                use SSSSS_TextInput(id="name", variableName="name", editable=True, placeholder="Click here to start writing the name")

                if(name != originalname and not SSSSS.Playthroughs.isValidName(name)):
                    text "Are you sure? This name already exists." color '#ffb14c' offset adjustable((15, 2), minValue=1)

                if(playthrough.id != 1):
                    python:
                        computedDirectory = playthrough.directory if (playthrough.directory != None) else (SSSSS.Utils.name_to_directory_name(name) if name else None) or ""

                    use SSSSS_Title("Directory", 2)
                    hbox:
                        offset adjustable((15, 0), minValue=1)

                        text "saves/" color '#e5e5e5'
                        text "[computedDirectory]" color '#a2ebff'

                        if isEdit:
                            use sssss_iconButton(icon="\ue2c8", action=SSSSS.OpenDirectoryAction(path=computedDirectory, cwd=renpy.config.savedir), size=20)
                        else:
                            use sssss_iconButton(icon="\ue2c8", action=SSSSS.OpenDirectoryAction(path=renpy.config.savedir), size=20)

                    $ allSaveLocations = SSSSS.SaveSystem.getAllNativeSaveLocationsForOptions()

                    if(isEdit and playthrough.id > 1 and name != originalname and SSSSS.Playthroughs.isValidName(name)):
                        use SSSSS_Checkbox(checked=moveSaveDirectory, text="Rename directory as well", action=ToggleScreenVariable('moveSaveDirectory', True, False), disabled=not SSSSS.Playthroughs.isValidName(name))

                    use SSSSS_Checkbox(checked=enabledSaveLocations != False, text="Manage save locations", action=ToggleScreenVariable('enabledSaveLocations', allSaveLocations, False))

                    if enabledSaveLocations != False:
                        hbox:
                            use SSSSS_XSpacer()

                            vbox:
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

                                        hbox:
                                            xpos 0.5
                                            xanchor 0.5
                                            ypos 0.5
                                            yanchor 0.5

                                            if isEdit:
                                                use sssss_iconButton(icon="\ue2c8", action=SSSSS.OpenDirectoryAction(path=fullPath), size=15, color="#818181")
                                            else:
                                                use sssss_iconButton(icon="\ue2c8", action=SSSSS.OpenDirectoryAction(path=path), size=15, color="#818181")

                                if len(enabledSaveLocations) == 0:
                                    use SSSSS_YSpacer(3)

                                    text "At least one location must be enabled!" color '#ff4c4c' xoffset adjustable(10)

                use SSSSS_YSpacer()

                use SSSSS_Title("Description")
                use SSSSS_TextInput(id="description", variableName="description", multiline=True, placeholder="Click here to start writing the description")

                use SSSSS_YSpacer()

                use SSSSS_Title("Options")
                hbox:
                    xfill True

                    vbox:
                        use SSSSS_Checkbox(checked=autosaveOnChoices, text="Autosave on choice", action=ToggleScreenVariable('autosaveOnChoices', True, False), disabled=not SSSSS.Utils.hasColsAndRowsConfiguration())
                        if not SSSSS.Utils.hasColsAndRowsConfiguration():
                            text "{size=-10}This game uses an unusual save system, thus autosave is not possible{/size}" color "#ff4c4c" offset adjustable((35, -10), minValue=1)

                        hbox:
                            offset adjustable((15, 0), minValue=1)

                            use SSSSS_Checkbox(checked=useChoiceLabelAsSaveName, text="Use choice text as a save name\n{size=-7}(Applies only for the saves created by this mod's autosave system!){/size}", action=ToggleScreenVariable('useChoiceLabelAsSaveName', True, False), disabled=not SSSSS.Utils.hasColsAndRowsConfiguration() or not autosaveOnChoices)

                use SSSSS_YSpacer()

                if isEdit:
                    use SSSSS_Title("Thumbnail")
                    hbox:
                        frame:
                            xysize adjustable((160, 160))

                            if playthrough.hasThumbnail():
                                add playthrough.getThumbnail(width=adjustable(150), maxHeight=adjustable(150))
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

            style_prefix "SSSSS_dialog_action_buttons"

            vbox:
                if(isEdit and playthrough.id != 1):
                    # Remove
                    hbox:
                        use sssss_iconButton(icon="\ue92b", text="{u}R{/u}emove", action=Show("SSSSS_RemovePlaythroughConfirm", playthrough=playthrough), color="#ff0000")

                # Save
                hbox:
                    use sssss_iconButton(icon="\ue161", text="{u}S{/u}ave", action=submitAction, disabled=(enabledSaveLocations != False and len(enabledSaveLocations) == 0) or len(name) == 0)

                # Close
                hbox:
                    use sssss_iconButton(icon="\ue5cd", text="Close", action=Hide("SSSSS_EditPlaythrough"))
screen URPS_EditPlaythrough(playthrough, isEdit=False, editing_template=False):
    layer "URPS_Overlay"
    style_prefix 'URPS'
    modal True

    $ playthrough = playthrough or URPS.Playthroughs.get_instance_for_edit()

    default name = playthrough.name or ''
    default originalname = name
    default description = playthrough.description or ''
    default storeChoices = playthrough.storeChoices
    default autosaveOnChoices = playthrough.autosaveOnChoices
    default useChoiceLabelAsSaveName = playthrough.useChoiceLabelAsSaveName
    default enabledSaveLocations = playthrough.enabledSaveLocations or False
    default moveSaveDirectory = True
    #MODIFY HERE

    default name_input = URPS.TextInput("name", auto_focus=True)
    default description_input = URPS.TextInput("description", multiline=True)

    python:
        if editing_template:
            submitAction = [
                URPS.Settings.SaveDefaultPlaythroughTemplate(playthrough, name, description, storeChoices, autosaveOnChoices, useChoiceLabelAsSaveName, enabledSaveLocations),#MODIFY HERE
                Hide('URPS_EditPlaythrough')
            ]
        else:
            submitAction = [
                URPS.Playthroughs.AddOrEdit(playthrough, name, description, storeChoices, autosaveOnChoices, useChoiceLabelAsSaveName, enabledSaveLocations, moveSaveDirectory),#MODIFY HERE
                Hide('URPS_EditPlaythrough')
            ]

    key 'ctrl_K_DELETE' action Show("URPS_RemovePlaythroughConfirm", playthrough=playthrough)

    use URPS_Dialog(title=("Edit default template" if editing_template else ("Edit playthrough" if isEdit else "New playthrough")), closeAction=Hide("URPS_EditPlaythrough")):
        style_prefix "URPS"

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            pagekeys True
            ymaximum 0.85

            vbox:
                use URPS_Title("Name")

                add name_input.displayable(placeholder="Click here to start writing the name")

                if(name != originalname and not URPS.Playthroughs.isValidName(name)):
                    text "Are you sure? This name already exists." color URPS.Colors.warning offset URPS.adjustable((15, 2), minValue=1)

                if(playthrough.id != 1 and not editing_template):
                    python:
                        computedDirectory = playthrough.directory if (playthrough.directory != None) else (URPS.Utils.name_to_directory_name(name) if name else None) or ""

                    use URPS_Title("Directory", 2)
                    hbox:
                        offset URPS.adjustable((15, 0), minValue=1)

                        text "saves/" color '#e5e5e5'
                        text "[computedDirectory]" color URPS.Colors.theme

                        if isEdit:
                            use URPS_IconButton(icon="\ue2c8", action=URPS.OpenDirectoryAction(path=computedDirectory, cwd=renpy.config.savedir), size=20, tt="Open playthrough directory", ttSide="right")
                        else:
                            use URPS_IconButton(icon="\ue2c8", action=URPS.OpenDirectoryAction(path=renpy.config.savedir), size=20, tt="Open a directory where this playthrough will be created", ttSide="right")

                    $ allSaveLocations = URPS.SaveSystem.getAllNativeSaveLocationsForOptions()

                    if(isEdit and playthrough.id > 1 and name != originalname and URPS.Playthroughs.isValidName(name)):
                        use URPS_Checkbox(checked=moveSaveDirectory, text="Rename the directory as well", action=ToggleScreenVariable('moveSaveDirectory', True, False), disabled=not URPS.Playthroughs.isValidName(name))

                    hbox:
                        use URPS_Checkbox(checked=enabledSaveLocations != False, text="Manage save locations", action=ToggleScreenVariable('enabledSaveLocations', allSaveLocations, False))
                        use URPS_Helper("Here, you can manage where saves are stored. By default, Ren'Py saves are kept in two locations: the game directory and the user directory. If you want to disable one of these locations, for example, to save storage space, you can do that here.")

                    if enabledSaveLocations != False:
                        hbox:
                            use URPS_XSpacer()

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
                                        use URPS_Checkbox(checked=location in enabledSaveLocations, text=locationType + " - {color=#818181}{size=-5}" + fullPath + "{/size}{/c}", action=ToggleSetMembership(enabledSaveLocations, location))

                                        hbox:
                                            xpos 0.5
                                            xanchor 0.5
                                            ypos 0.5
                                            yanchor 0.5

                                            if isEdit:
                                                use URPS_IconButton(icon="\ue2c8", action=URPS.OpenDirectoryAction(path=fullPath), size=15, color="#818181", tt="Open directory", hover_color=URPS.Colors.hover)
                                            else:
                                                use URPS_IconButton(icon="\ue2c8", action=URPS.OpenDirectoryAction(path=path), size=15, color="#818181", tt="Open directory", hover_color=URPS.Colors.hover)

                                if len(enabledSaveLocations) == 0:
                                    use URPS_YSpacer(3)

                                    text "At least one location must be enabled!" color URPS.Colors.error xoffset URPS.adjustable(10)

                use URPS_YSpacer()

                use URPS_Title("Description")
                add description_input.displayable(placeholder="Click here to start writing the description")

                use URPS_YSpacer()

                use URPS_Title("Options")
                hbox:
                    xfill True

                    vbox:
                        hbox:
                            use URPS_Checkbox(checked=autosaveOnChoices, text="Autosave on choice", action=ToggleScreenVariable('autosaveOnChoices', True, False), disabled=not URPS.Utils.hasColsAndRowsConfiguration())
                            use URPS_Helper("This system automatically saves your progress (not to be confused with Ren'Py's autosave) right before you make a choice in the game, making it easier to back up and track your progress.")
                        if not URPS.Utils.hasColsAndRowsConfiguration():
                            text "{size=-7}{color=[URPS.Colors.error]}This game uses an unconventional save configuration, so the autosave feature requires a manual adjustment to be enabled.{/color}" offset URPS.adjustable((35, -10), minValue=1)
                            hbox offset URPS.adjustable((35, -10), minValue=1):
                                button style "URPS_default":
                                    action None

                                    use URPS_Icon('\ue88e', color = URPS.Colors.info, size=13)

                                hbox xsize URPS.adjustable(5)

                                text "{size=-7}{color=[URPS.Colors.info]}For manual adjustment, count the number of columns and rows, then go to the settings and find {color=[URPS.Colors.theme]}\"Custom slots grid\"{/color}. There, enter the numbers accordingly.{/color}{/size}"

                        hbox:
                            offset URPS.adjustable((15, 0), minValue=1)

                            use URPS_Checkbox(checked=useChoiceLabelAsSaveName, text="Use the choice text as a save name\n{size=-7}(Applies only for the saves created by this mod's autosave system enabled above){/size}", action=ToggleScreenVariable('useChoiceLabelAsSaveName', True, False), disabled=not URPS.Utils.hasColsAndRowsConfiguration() or not autosaveOnChoices)

                use URPS_YSpacer()

                if isEdit:
                    use URPS_Title("Thumbnail")
                    hbox:
                        frame:
                            xysize URPS.adjustable((160, 160))

                            if playthrough.hasThumbnail():
                                add playthrough.getThumbnail(width=URPS.adjustable(150), maxHeight=URPS.adjustable(150))
                            else:
                                button:
                                    style_prefix ""
                                    action None
                                    xalign 0.5
                                    yalign 0.5

                                    use URPS_Icon(icon="\ue3f4", color="#333")


                        vbox:
                            # Set thumbnail
                            use URPS_IconButton(icon="\ue3f4", text="Set the current scene as the thumbnail", action=URPS.Playthroughs.SetThumbnail(playthrough=playthrough))

                            # Remove thumbnail
                            if playthrough.hasThumbnail():
                                use URPS_IconButton(icon="\ue92b", text="Remove thumbnail", action=URPS.Playthroughs.RemoveThumbnail(playthrough=playthrough), color=URPS.Colors.danger)

        hbox:
            xfill True
            yfill True

            style_prefix "URPS_dialog_action_buttons"

            if not isEdit and not editing_template:
                vbox xalign 0.0:
                    hbox:
                        use URPS_IconButton(icon="\uead3", text="Edit default values", action=Show("URPS_EditPlaythrough", playthrough=None, editing_template=True), tt="Click here to edit the default values for new playthroughs")

            vbox:
                if(isEdit and playthrough.id != 1):
                    # Remove
                    hbox:
                        use URPS_IconButton(icon="\ue92b", text="Remove", action=Show("URPS_RemovePlaythroughConfirm", playthrough=playthrough), color=URPS.Colors.danger, key="ctrl_K_r")

                # Save
                hbox:
                    use URPS_IconButton(icon="\ue161", text="Save" + (" template" if editing_template else ""), action=submitAction, disabled=(enabledSaveLocations != False and len(enabledSaveLocations) == 0) or len(name) == 0, key="ctrl_K_s")

                if not isEdit:
                    hbox:
                        use URPS_IconButton(icon="\uebbd", text="Create from existing directory", action=Show("URPS_SelectExistingDirectoryForNewPlaythrough"), tt="You can use already existing directory to create a playthrough. It will fill out the name and set the directory for you.", ttSide="left")

                # Close
                hbox:
                    use URPS_IconButton(icon="\ue5cd", text="Close", action=Hide("URPS_EditPlaythrough"))
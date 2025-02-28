screen JK_EditPlaythrough(playthrough, isEdit=False, editing_template=False):
    layer "JK_Overlay"
    style_prefix 'JK'
    modal True

    $ playthrough = playthrough or JK.Playthroughs.get_instance_for_edit()

    default name = playthrough.name or ''
    default originalname = name if isEdit else ''
    default description = playthrough.description or ''
    default storeChoices = playthrough.storeChoices
    default autosaveOnChoices = playthrough.autosaveOnChoices
    default useChoiceLabelAsSaveName = playthrough.useChoiceLabelAsSaveName
    default enabledSaveLocations = playthrough.enabledSaveLocations or False
    default moveSaveDirectory = True
    #MODIFY HERE

    default name_input = JK.TextInput("name", auto_focus=True)
    default description_input = JK.TextInput("description", multiline=True)

    python:
        if editing_template:
            submitAction = [
                JK.Settings.SaveDefaultPlaythroughTemplate(playthrough, name, description, storeChoices, autosaveOnChoices, useChoiceLabelAsSaveName, enabledSaveLocations),#MODIFY HERE
                Hide('JK_EditPlaythrough')
            ]
        else:
            submitAction = [
                JK.Playthroughs.AddOrEdit(playthrough, name, description, storeChoices, autosaveOnChoices, useChoiceLabelAsSaveName, enabledSaveLocations, moveSaveDirectory),#MODIFY HERE
                Hide('JK_EditPlaythrough')
            ]

        name_conflicting = not editing_template and name != originalname and not JK.Playthroughs.isValidName(name)
        name_invalid = name_conflicting or len(name) == 0

    key 'ctrl_K_DELETE' action Show("JK_RemovePlaythroughConfirm", playthrough=playthrough)

    use JK_Dialog(title=("Edit default template" if editing_template else ("Edit playthrough" if isEdit else "New playthrough")), closeAction=Hide("JK_EditPlaythrough")):
        style_prefix "JK"

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            pagekeys True
            ymaximum 0.85

            vbox:
                button:
                    action name_input.get_enable_action()
                    key_events True

                    vbox:
                        use JK_Title("Name")
                        add name_input.displayable(placeholder="Click here to start writing")
                        frame style "JK_default" background "#ffffff22" hover_background JK.Colors.hover ysize 2 offset JK.scaled((0, 2))

                text "{size=-5}This name already exists.{/size}" color (JK.Colors.error if name_conflicting else "#00000000") offset JK.scaled((10, 2))

                use JK_YSpacer(2)

                if(playthrough.id != 1 and not editing_template):
                    python:
                        computedDirectory = playthrough.directory if (playthrough.directory != None) else (JK.Utils.name_to_directory_name(name) if name else None) or ""

                    use JK_Title("Directory", 2)
                    hbox:
                        offset JK.scaled((15, 0))

                        text "saves/" color '#e5e5e5'
                        text "[computedDirectory]" color JK.Colors.theme

                        if isEdit:
                            use JK_IconButton(icon="\ue2c8", action=JK.OpenDirectoryAction(path=computedDirectory, cwd=renpy.config.savedir), size=20, tt="Open playthrough directory", ttSide="right")
                        else:
                            use JK_IconButton(icon="\ue2c8", action=JK.OpenDirectoryAction(path=renpy.config.savedir), size=20, tt="Open a directory where this playthrough will be created", ttSide="right")

                    $ allSaveLocations = JK.SaveSystem.getAllNativeSaveLocationsForOptions()

                    if isEdit and playthrough.id > 1 and name != originalname and not name_invalid:
                        use JK_Checkbox(checked=moveSaveDirectory, text="Rename the directory as well", action=ToggleScreenVariable('moveSaveDirectory', True, False))

                    hbox:
                        use JK_Checkbox(checked=enabledSaveLocations != False, text="Manage save locations", action=ToggleScreenVariable('enabledSaveLocations', allSaveLocations, False))
                        use JK_Helper("Here, you can manage where saves are stored. By default, Ren'Py saves are kept in two locations: the game directory and the user directory. If you want to disable one of these locations, for example, to save storage space, you can do that here.")

                    if enabledSaveLocations != False:
                        hbox:
                            use JK_XSpacer()

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
                                        use JK_Checkbox(checked=location in enabledSaveLocations, text=locationType + " - {color=#818181}{size=-5}" + fullPath + "{/size}{/c}", action=ToggleSetMembership(enabledSaveLocations, location))

                                        hbox:
                                            xpos 0.5
                                            xanchor 0.5
                                            ypos 0.5
                                            yanchor 0.5

                                            if isEdit:
                                                use JK_IconButton(icon="\ue2c8", action=JK.OpenDirectoryAction(path=fullPath), size=15, color="#818181", tt="Open directory", hover_color=JK.Colors.hover)
                                            else:
                                                use JK_IconButton(icon="\ue2c8", action=JK.OpenDirectoryAction(path=path), size=15, color="#818181", tt="Open directory", hover_color=JK.Colors.hover)

                                if len(enabledSaveLocations) == 0:
                                    use JK_YSpacer(3)

                                    text "At least one location must be enabled!" color JK.Colors.error xoffset JK.scaled(10)

                use JK_YSpacer()

                button:
                    action description_input.get_enable_action()
                    key_events True

                    vbox:
                        use JK_Title("Description")
                        add description_input.displayable(placeholder="Click here to start writing")
                        frame style "JK_default" background "#ffffff22" hover_background JK.Colors.hover ysize 2 offset JK.scaled((0, 2))

                use JK_YSpacer()

                use JK_Title("Options")
                hbox:
                    xfill True

                    vbox:
                        hbox:
                            use JK_Checkbox(checked=autosaveOnChoices, text="Autosave on choice", action=ToggleScreenVariable('autosaveOnChoices', True, False), disabled=not JK.Utils.hasColsAndRowsConfiguration())
                            use JK_Helper("This system automatically saves your progress (not to be confused with Ren'Py's autosave) right before you make a choice in the game, making it easier to back up and track your progress.")
                        if not JK.Utils.hasColsAndRowsConfiguration():
                            text "{size=-7}{color=[JK.Colors.error]}This game uses an unconventional save configuration, so the autosave feature requires a manual adjustment to be enabled.{/color}" offset JK.scaled((35, -10))
                            hbox offset JK.scaled((35, -10)):
                                button style "JK_default":
                                    action None

                                    use JK_Icon('\ue88e', color = JK.Colors.info, size=13)

                                hbox xsize JK.scaled(5)

                                text "{size=-7}{color=[JK.Colors.info]}For manual adjustment, count the number of columns and rows, then go to the settings and find {color=[JK.Colors.theme]}\"Custom slots grid\"{/color}. There, enter the numbers accordingly.{/color}{/size}"

                        hbox:
                            offset JK.scaled((15, 0))

                            use JK_Checkbox(checked=useChoiceLabelAsSaveName, text="Use the choice text as a save name\n{size=-7}(Applies only for the saves created by this mod's autosave system enabled above){/size}", action=ToggleScreenVariable('useChoiceLabelAsSaveName', True, False), disabled=not JK.Utils.hasColsAndRowsConfiguration() or not autosaveOnChoices)

                use JK_YSpacer()

                if isEdit:
                    use JK_Title("Thumbnail")
                    hbox:
                        frame:
                            xysize JK.scaled((160, 160))

                            if playthrough.hasThumbnail():
                                add playthrough.getThumbnail(width=JK.scaled(150), maxHeight=JK.scaled(150))
                            else:
                                button:
                                    style_prefix ""
                                    action None
                                    xalign 0.5
                                    yalign 0.5

                                    use JK_Icon(icon="\ue3f4", color="#333")


                        vbox:
                            # Set thumbnail
                            use JK_IconButton(icon="\ue3f4", text="Set the current scene as the thumbnail", action=JK.Playthroughs.SetThumbnail(playthrough=playthrough))

                            # Remove thumbnail
                            if playthrough.hasThumbnail():
                                use JK_IconButton(icon="\ue92b", text="Remove thumbnail", action=JK.Playthroughs.RemoveThumbnail(playthrough=playthrough), color=JK.Colors.danger)

        hbox:
            xfill True
            yfill True

            style_prefix "JK_dialog_action_buttons"

            if not isEdit and not editing_template:
                vbox xalign 0.0:
                    hbox:
                        use JK_IconButton(icon="\uead3", text="Edit default values", action=Show("JK_EditPlaythrough", playthrough=None, editing_template=True), tt="Click here to edit the default values for new playthroughs")

            vbox:
                if(isEdit and playthrough.id != 1):
                    # Remove
                    hbox:
                        use JK_IconButton(icon="\ue92b", text="Remove", action=Show("JK_RemovePlaythroughConfirm", playthrough=playthrough), color=JK.Colors.danger, key="ctrl_K_r")

                # Save
                hbox:
                    if editing_template:
                        use JK_IconButton(icon="\ue161", text="Save template", action=submitAction, key="ctrl_K_s")
                    else:
                        use JK_IconButton(icon="\ue161", text="Save", action=submitAction, disabled=(enabledSaveLocations != False and len(enabledSaveLocations) == 0) or name_invalid, key="ctrl_K_s")

                if not isEdit and not editing_template:
                    hbox:
                        use JK_IconButton(icon="\uebbd", text="Create from existing directory", action=Show("JK_SelectExistingDirectoryForNewPlaythrough"), tt="You can use already existing directory to create a playthrough. It will fill out the name and set the directory for you.", ttSide="left")

                # Close
                hbox:
                    use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_EditPlaythrough"))
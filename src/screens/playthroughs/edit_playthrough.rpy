screen JK_EditPlaythrough(playthrough, isEdit=False, editing_template=False, duplicating=False):
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
                JK.Settings.SaveDefaultPlaythroughTemplateAction(playthrough, name, description, storeChoices, autosaveOnChoices, useChoiceLabelAsSaveName, enabledSaveLocations)#MODIFY HERE
            ]
        elif duplicating:
            submitAction = [
                JK.Playthroughs.DuplicatePlaythroughAction(playthrough, name, description, storeChoices, autosaveOnChoices, useChoiceLabelAsSaveName, enabledSaveLocations, moveSaveDirectory)#MODIFY HERE
            ]
        else:
            submitAction = [
                JK.Playthroughs.AddOrEditAction(playthrough, name, description, storeChoices, autosaveOnChoices, useChoiceLabelAsSaveName, enabledSaveLocations, moveSaveDirectory)#MODIFY HERE
            ]

        submitAction.append(Hide('JK_EditPlaythrough'))

        name_conflicting = not editing_template and name != originalname and not JK.Playthroughs.is_valid_name(name)
        name_invalid = name_conflicting or len(name) == 0

        is_save_disabled = enabledSaveLocations != False and len(enabledSaveLocations) == 0
        if not editing_template:
            is_save_disabled = is_save_disabled or name_invalid

        title = ""
        if editing_template:
            title = "Edit default template"
        elif isEdit:
            title = "Edit playthrough"
        elif duplicating:
            title = "Duplicate \"" + playthrough.name + "\""
        else:
            title = "New playthrough"

    key 'ctrl_K_DELETE' action Show("JK_RemovePlaythroughConfirm", playthrough=playthrough)

    if not is_save_disabled:
        key "ctrl_K_s" action submitAction

    use JK_Dialog(title=title, close_action=Hide("JK_EditPlaythrough")):
        style_prefix "JK"

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            vscrollbar_unscrollable "hide"
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

                if not playthrough.directory_immovable:
                    python:
                        allSaveLocations = JK.SaveSystem.get_all_native_save_locations_for_options()
                        computedDirectory = "[[Playthrough name]"

                    if not editing_template:
                        python:
                            computedDirectory = playthrough.directory if playthrough.directory and (not moveSaveDirectory or name == playthrough.name) else (JK.Utils.name_to_directory_name(name) if name else None) or ""

                        use JK_Title("Directory", 2)
                        hbox:
                            offset JK.scaled((15, 0))

                            text "saves/" color '#e5e5e5'
                            text "[computedDirectory]" color JK.Colors.theme

                            hbox yalign 0.5 xoffset JK.scaled(5):
                                if isEdit:
                                    use JK_IconButton(icon="\ue2c8", action=JK.OpenDirectoryAction(path=computedDirectory, cwd=renpy.config.savedir), size=20, tt="Open playthrough directory", tt_side="right")
                                else:
                                    use JK_IconButton(icon="\ue2c8", action=JK.OpenDirectoryAction(path=renpy.config.savedir), size=20, tt="Open a directory where this playthrough will be created", tt_side="right")

                        if isEdit and playthrough.id > 1 and name != originalname and not name_invalid:
                            use JK_Checkbox(checked=moveSaveDirectory, text="Rename the directory as well", action=ToggleScreenVariable('moveSaveDirectory', True, False))

                    if len(allSaveLocations) > 1:
                        hbox:
                            use JK_Checkbox(checked=enabledSaveLocations != False, text="Manage save locations", action=ToggleScreenVariable('enabledSaveLocations', allSaveLocations, False))
                            use JK_Helper("Here, you can configure where your saves for this playthrough are stored.\nBy default, Ren'Py saves are kept in two {color=[JK.Colors.warning]}(varies by platform){/color} locations: the game directory and the user directory. If you want to disable one of these locations, for example, to save storage space, you can do that here.")

                        if enabledSaveLocations != False:
                            hbox:
                                use JK_XSpacer()

                                $ platform_specific_library_name = "Library" if renpy.macintosh else ("%APPDATA%" if renpy.windows else "Home")

                                vbox:
                                    for location in allSaveLocations:
                                        python:
                                            locationType = "Extra"
                                            path = location

                                            # User savedir (appdata or library).
                                            if location == "USER":
                                                locationType = platform_specific_library_name
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

                                    if "USER" not in enabledSaveLocations and len(enabledSaveLocations) == 1:
                                        use JK_YSpacer(3)

                                        text "Warning: If you don't use [platform_specific_library_name], your save files are going to be stored only with the game. Uninstalling the game will {u}delete your progress{/u} as well." color JK.Colors.warning xoffset JK.scaled(10)

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
                            use JK_Checkbox(checked=autosaveOnChoices, text="Autosave on choice", action=ToggleScreenVariable('autosaveOnChoices', True, False), disabled=not JK.Utils.has_cols_and_rows_configuration())
                            use JK_Helper("This system automatically saves your progress right before you make a choice in the game, making it easier to back up and track your progress.\n\n{color=[JK.Colors.warning]}Not to be confused with the native Ren'Py \"Autosave\" feature.{/color}")

                        if not JK.Utils.has_cols_and_rows_configuration():
                            text "{size=-7}{color=[JK.Colors.error]}This game uses an unconventional save configuration, so autosave won't work out of the box.{/color}\n{color=[JK.Colors.text_primary]}To enable this option, follow these steps:\n  1) count the columns and rows in your save grid\n  2) go to settings, locate {color=[JK.Colors.theme]}\"Custom slots grid\"{/color} and enable it. (When enabled, this message will disappear)\n  3) Set the values accordingly.\nIf this option is enabled and the autosave still won't work, visit {a=[JK.DISCORD_URL]}Discord{/a} or {a=https://github.com/[JK.MOD_GITHUB_OWNER]/[JK.MOD_GITHUB_REPO]/issues}https://github.com/[JK.MOD_GITHUB_OWNER]/[JK.MOD_GITHUB_REPO]/issues{/a} for troubleshooting or an assistance.\n\n{color=[JK.Colors.info]}To quickly access the relevant settings page {a=JK_Run:JK.Settings.ShowSaveLoadAction()}click here{/a}.{/color}{/color}{/size}" offset JK.scaled((35, -5))

                        hbox:
                            offset JK.scaled((15, 0))

                            use JK_Checkbox(checked=useChoiceLabelAsSaveName, text="Use the choice text as the save name\n{size=-7}(Only applies to saves created by this mod's autosave system){/size}", action=ToggleScreenVariable('useChoiceLabelAsSaveName', True, False), disabled=not JK.Utils.has_cols_and_rows_configuration() or not autosaveOnChoices)

                use JK_YSpacer()

                if isEdit or duplicating:
                    use JK_Title("Thumbnail")
                    hbox:
                        frame style "JK_default":
                            xysize JK.scaled((350, 250))

                            if playthrough.hasThumbnail():
                                image playthrough.getThumbnail(width=JK.scaled(350), height=JK.scaled(350))
                            else:
                                button:
                                    style_prefix ""
                                    action None
                                    xalign 0.5
                                    yalign 0.5

                                    use JK_Icon(icon="\ue3f4", color="#333")

                        use JK_XSpacer(3)

                        vbox:
                            # Set thumbnail
                            use JK_IconButton(icon="\ue3f4", text="Set the current scene as the thumbnail", action=JK.Playthroughs.SetThumbnail(playthrough=playthrough))

                            # Remove thumbnail
                            if playthrough.hasThumbnail():
                                use JK_IconButton(icon="\ue92b", text="Remove thumbnail", action=Function(playthrough.removeThumbnail, _update_screens=True), color=JK.Colors.danger)

        hbox:
            xfill True
            yfill True

            style_prefix "JK_dialog_action_buttons"

            if not isEdit and not editing_template and not duplicating:
                vbox xalign 0.0:
                    hbox:
                        use JK_IconButton(icon="\uead3", text="Edit default values", action=Show("JK_EditPlaythrough", playthrough=None, editing_template=True), tt="Click here to edit the default values for new playthroughs")

            vbox:
                if isEdit and playthrough.deletable:
                    # Remove
                    hbox:
                        use JK_IconButton(icon="\ue92b", text="Remove", action=Show("JK_RemovePlaythroughConfirm", playthrough=playthrough), color=JK.Colors.danger, key="alt_K_r")

                # Save
                hbox:
                    if editing_template:
                        use JK_IconButton(icon="\ue161", text="Save template", action=submitAction, key="alt_K_s", disabled=is_save_disabled)
                    else:
                        use JK_IconButton(icon="\ue161", text="Save", action=submitAction, disabled=is_save_disabled, key="alt_K_s")

                if not isEdit and not editing_template and not duplicating:
                    hbox:
                        use JK_IconButton(icon="\uebbd", text="Create from existing directory", action=Show("JK_SelectExistingDirectoryForNewPlaythrough"), tt="You can use already existing directory to create a playthrough. It will fill out the name and set the directory for you.", tt_side="left")

                # Close
                hbox:
                    use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_EditPlaythrough"))
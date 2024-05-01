screen SSSSS_EditPlaythrough(playthrough, isEdit=False):
    layer "SSSSSoverlay"
    style_prefix 'SSSSS'

    $ playthrough = playthrough or SSSSS.Playthroughs.PlaythroughClass()

    default name = playthrough.name or ''
    default originalname = name
    default storeChoices = playthrough.storeChoices
    default autosaveOnChoices = playthrough.autosaveOnChoices
    default useChoiceLabelAsSaveName = playthrough.useChoiceLabelAsSaveName
    #MODIFY HERE

    default inputs = x52URM.InputGroup(
        [
            ('name', x52URM.Input(text=name, updateScreenVariable="name")),
        ],
        focusFirst=True,
        onSubmit=[
            SSSSS.Playthroughs.AddOrEdit(playthrough=playthrough, name=x52URM.GetScreenInput('name', 'inputs'), storeChoices=URMGetScreenVariable('storeChoices'), autosaveOnChoices=URMGetScreenVariable('autosaveOnChoices'), useChoiceLabelAsSaveName=URMGetScreenVariable('useChoiceLabelAsSaveName')),#MODIFY HERE
            Hide('SSSSS_EditPlaythrough')
        ]
    )

    key 'K_TAB' action inputs.NextInput()
    key 'shift_K_TAB' action inputs.PreviousInput()

    use SSSSS_Dialog(title=("Edit playthrough" if isEdit else "New playthrough"), closeAction=Hide("SSSSS_EditPlaythrough")):
        style_prefix "SSSSS"

        vbox:
            text "Name:"
            frame:
                button:
                    style_prefix "" # Have to override some other styles that are applying for some reson...

                    key_events True
                    action inputs.name.Enable()

                    input value inputs.name:
                        style "SSSSS_input_input"

            if(name != originalname and not SSSSS.Playthroughs.isValidName(name)):
                text "Are you sure? This name already exists." color '#ffb14c' offset (15, 2)

            if(playthrough.id != 1):
                python:
                    computedDirectory = playthrough.directory if (playthrough.directory != None) else (SSSSS.Utils.name_to_directory_name(name) if name else None)

                text "Directory:"
                hbox:
                    offset (15, 0)

                    text "saves/" color '#e5e5e5'
                    text "[computedDirectory]" color '#a2ebff'

            hbox ysize 10

            text "Options:"
            hbox:
                xfill True

                vbox:
                    # use SSSSS_Checkbox(checked=storeChoices, text="Store choices", action=ToggleScreenVariable('storeChoices', True, False)) #TODO: Implement
                    use SSSSS_Checkbox(checked=autosaveOnChoices, text="Autosave on choice", action=ToggleScreenVariable('autosaveOnChoices', True, False))
                    use SSSSS_Checkbox(checked=useChoiceLabelAsSaveName, text="Use choice text as a save name", action=ToggleScreenVariable('useChoiceLabelAsSaveName', True, False))

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
                            use sssss_iconButton(icon="\ue92b", text="Remove thumbnail", action=SSSSS.Playthroughs.RemoveThumbnail(playthrough=playthrough), textColor="#ff0000")

        hbox:
            xfill True
            yfill True

            vbox at right:
                yalign 1.0

                if(isEdit and playthrough.id != 1):
                    # Remove
                    hbox at right:
                        use sssss_iconButton(icon="\ue92b", text="Remove", action=Show("SSSSS_RemovePlaythroughConfirm", playthrough=playthrough), textColor="#ff0000")

                # Save
                hbox at right:
                    use sssss_iconButton(icon="\ue161", text="Save", action=inputs.onSubmit)

                # Close
                hbox at right:
                    use sssss_iconButton(icon="\ue5cd", text="Close", action=Hide("SSSSS_EditPlaythrough"))
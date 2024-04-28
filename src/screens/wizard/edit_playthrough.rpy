screen SSSSS_EditPlaythrough(playthrough, isEdit=False):
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

    use SSSSS_Dialog(title=("Edit playthrough" if isEdit else "New playthrough"), closeAction=Hide("SSSSS_EditPlaythrough"), background="gui/edit_playthrough_dialog_background.png", size=(x52URM.scalePxInt(1000), x52URM.scalePxInt(600))):
        style_prefix "SSSSS"

        vbox:
            yfill True

            vbox:
                text "Name:"
                frame:
                    style "SSSSS_input_frame"

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

                hbox:
                    xfill True

                    vbox:
                        # use SSSSS_Checkbox(checked=storeChoices, text="Store choices", action=ToggleScreenVariable('storeChoices', True, False)) #TODO: Implement
                        use SSSSS_Checkbox(checked=autosaveOnChoices, text="Autosave on choice", action=ToggleScreenVariable('autosaveOnChoices', True, False))
                        use SSSSS_Checkbox(checked=useChoiceLabelAsSaveName, text="Use choice text as a save name", action=ToggleScreenVariable('useChoiceLabelAsSaveName', True, False))

                    hbox:
                        hbox xsize 160:
                            add playthrough.getThumbnail(width=150, maxHeight=150)

                        button:
                            style "SSSSS_textbutton_medium_gray"
                            key_events True
                            action [SSSSS.Playthroughs.SetThumbnail(playthrough=playthrough)]

                            text "Set current scene as thumbnail" yalign .5 xalign 0.5 size 24

        hbox:
            xfill True
            offset (0, -50)

            if(isEdit):
                button:
                    style "SSSSS_textbutton_medium_red"
                    key_events True
                    xalign 0.5
                    action Show("SSSSS_RemovePlaythroughConfirm", playthrough=playthrough)

                    text "Remove" yalign .5 xalign 0.5 size 28

            button:
                style "SSSSS_textbutton_medium_green"
                key_events True # We need this to still trigger key events defined inside of this button
                xalign 0.5

                action inputs.onSubmit
                
                text "Save" yalign .5 xalign 0.5 size 28
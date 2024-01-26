screen SSSSS_PlaythroughsPicker():
    use SSSSS_Dialog(title="Select a playthrough", closeAction=Hide("SSSSS_PlaythroughsPicker"), background="assets/gui/select_playthrough_dialog_background.png", size=(x52URM.scalePxInt(581), x52URM.scalePxInt(623))):
        style_prefix "SSSSS"

        use SSSSS_PlaythroughsList(itemAction=SSSSS.Playthroughs.ActivatePlaythrough, hideTarget="SSSSS_PlaythroughsPicker", canEdit=True)

screen SSSSS_EditPlaythrough(playthrough, isEdit=False):
    default name = playthrough.name or ''
    default originalname = name
    default storeChoices = playthrough.storeChoices
    default autosaveOnChoices = playthrough.autosaveOnChoices
    #MODIFY HERE

    default inputs = x52URM.InputGroup(
        [
            ('name', x52URM.Input(text=name, updateScreenVariable="name")),
        ],
        focusFirst=True,
        onSubmit=[
            SSSSS.Playthroughs.AddOrEdit(playthrough=playthrough, name=x52URM.GetScreenInput('name', 'inputs'), storeChoices=URMGetScreenVariable('storeChoices'), autosaveOnChoices=URMGetScreenVariable('autosaveOnChoices')),#MODIFY HERE
            Hide('SSSSS_EditPlaythrough')
        ]
    )

    key 'K_TAB' action inputs.NextInput()
    key 'shift_K_TAB' action inputs.PreviousInput()

    use SSSSS_Dialog(title=("Edit playthrough" if isEdit else "New playthrough"), closeAction=Hide("SSSSS_EditPlaythrough"), background="assets/gui/edit_playthrough_dialog_background.png", size=(x52URM.scalePxInt(1000), x52URM.scalePxInt(600))):
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

                python:
                    computedDirectory = playthrough.directory or SSSSS.Playthroughs.name_to_directory_name(name)

                text "Directory:"

                hbox:
                    offset (15, 0)

                    text "saves/" color '#e5e5e5'
                    text "[computedDirectory]" color '#a2ebff'

                use SSSSS_Checkbox(checked=storeChoices, text="Store choices", action=ToggleScreenVariable('storeChoices', True, False))
                use SSSSS_Checkbox(checked=autosaveOnChoices, text="Autosave on choice", action=ToggleScreenVariable('autosaveOnChoices', True, False))

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

screen SSSSS_RemovePlaythroughConfirm(playthrough):
    default deleteFiles = False

    use SSSSS_Dialog(title="Delete playthrough", closeAction=Hide("SSSSS_RemovePlaythroughConfirm"), background="assets/gui/dialog/confirm_dialog_background.png", size=(x52URM.scalePxInt(922), x52URM.scalePxInt(400))):
        style_prefix "SSSSS"

        text "Are you sure you want to remove \"[playthrough.name]\"?" xalign .5

        frame:
            background None
            xalign 0.5
            padding (0, 10, 0, 0)

            use SSSSS_Checkbox(checked=deleteFiles, text="Delete files", action=ToggleScreenVariable('deleteFiles', True, False))

        frame:
            background None
            padding (0, 0, 10, 0)
            xalign 0.5

            hbox:
                use sssss_icon('\ue88e')
                hbox xsize 10
                text "If you choose to delete the files, you won't be able to recover the playthrough." yalign .5

        hbox:
            xfill True

            python:
                removeText = "Remove & delete files" if deleteFiles else "Remove"

            button:
                style "SSSSS_textbutton_medium_red"
                action [SSSSS.Playthroughs.Remove(playthrough.name, deleteFiles), Hide("SSSSS_RemovePlaythroughConfirm"), Hide("SSSSS_EditPlaythrough")]
                key_events True # We need this to still trigger key events defined inside of this button
                xalign 0.5

                text "[removeText]" yalign .5 xalign 0.5 size (20 if deleteFiles else 28)

            button:
                style "SSSSS_textbutton_medium_gray"
                action Hide("SSSSS_RemovePlaythroughConfirm")
                key_events True # We need this to still trigger key events defined inside of this button
                xalign 0.5
                
                text "Close" yalign .5 xalign 0.5 size 28

screen SSSSS_PlaythroughsList(itemAction=None, hideTarget=None, canEdit=False):
    viewport:
        mousewheel True
        draggable
        scrollbars "vertical"
        pagekeys True

        vbox:
            xfill True

            for playthrough in SSSSS.Playthroughs.playthroughs:
                button:
                    xfill True

                    if(hideTarget):
                        action [itemAction(playthrough), Hide(hideTarget)]
                    else:
                        action itemAction(playthrough)

                    hbox:
                        xfill True

                        add playthrough.getThumbnail()

                        label "[playthrough.name]" xfill True

                        if(canEdit):
                            hbox:
                                offset (-100, 0)

                                use sssss_iconButton('\ue872', tt="Remove playthrough", action=Show("SSSSS_RemovePlaythroughConfirm", playthrough=playthrough))
                                use sssss_iconButton('\ue3c9', tt="Edit playthrough", action=Show("SSSSS_EditPlaythrough", playthrough=playthrough, isEdit=True))
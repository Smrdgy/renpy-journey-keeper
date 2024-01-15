screen SSSSS_PlaythroughMenu(save):
    python:
        playthrough = SSSSS.Playthroughs.activePlaythrough

    use game_menu(_("Save" if save else "Load")):
        fixed:
            # This ensures the input will get the enter event before any of the
            # buttons do.
            order_reverse True

            vbox:
                xfill True

                #action buttons
                hbox:
                    xfill True

                    hbox at left:
                        use sssss_iconButton('\ue7a2', tt="Open native save menu", action=[SSSSS.Playthroughs.ActivateNative(), Show("SSSSS_NativeSaveMenu", save=save)])
                        use sssss_iconButton('\ueb73', tt="Open list of playthroughs", action=Show("SSSSS_PlaythroughsPicker"))
                        use sssss_iconButton('\ue02c', tt="Open memories", action=Show("SSSSS_MemoriesList"))
                        use sssss_iconButton('\uea20', tt="New playthrough", action=Show("SSSSS_EditPlaythrough"))

                    hbox at right:
                        if(playthrough != None):
                            use sssss_iconButton('\ue4f9', toggled=playthrough.get("autosaveOnChoices"), toggledIcon='\ue167', tt="Autosave on choices", action=SSSSS.Playthroughs.ToggleAutosaveOnChoicesOnActive())

            if(playthrough != None):
                # The playthrough name, the playthrough can be edited by clicking on this button.
                button:
                    style "page_label"

                    xalign 0.5

                    action Show("SSSSS_EditPlaythrough", directory=playthrough.get("directory"), name=playthrough.get("name"), thumbnail=playthrough.get("thumbnail"), storeChoices=playthrough.get("storeChoices"), layout=playthrough.get("layout"), autosaveOnChoices=playthrough.get("autosaveOnChoices"), selectedPage=playthrough.get("selectedPage"))#MODIFY HERE

                    vbox:
                        style "page_label_text"

                        label playthrough.get("name")

            if(playthrough != None):
                use SSSSS_PlaythroughFileGrid()
            else:
                vbox:
                    yalign 0.5
                    xalign 0.5

                    textbutton "Click here to setup playthrough":
                        xalign 0.5

                        action Show("SSSSS_EditPlaythrough")
                    
                    button:
                        xalign 0.5

                        action Show("SSSSS_NativeSaveMenu", save=save)

                        vbox:
                            text "Or here":
                                xalign 0.5
                            text "to use the vanilla system":
                                xalign 0.5

screen SSSSS_PlaythroughFileGrid():
    python:
        import math

        currentPage = persistent._file_page
        if(currentPage == "quick" or currentPage == "auto"):
            currentPage = 1
        
        currentPage = int(currentPage)

        pageOffset = math.floor(currentPage / 10)

    fixed:
        ## The grid of file slots.
        grid gui.file_slot_cols gui.file_slot_rows:
            style_prefix "slot"

            xalign 0.5
            yalign 0.5

            spacing gui.slot_spacing

            for i in range(gui.file_slot_cols * gui.file_slot_rows):

                $ slot = i + 1

                button:
                    action FileAction(slot)

                    has vbox

                    add FileScreenshot(slot) xalign 0.5

                    text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                        style "slot_time_text"

                    text FileSaveName(slot):
                        style "slot_name_text"

                    key "save_delete" action FileDelete(slot)

        ## Buttons to access other pages.
        grid 3 1:
            style_prefix "page"

            xfill True
            yalign 1.0
            spacing gui.page_spacing

            hbox at left:
                spacing gui.page_spacing

                textbutton _("<<") action FilePage(max(currentPage - 10, 1))
                textbutton _("<") action FilePagePrevious(max=1, auto=False, quick=False)

            grid 10 1 at center:
                spacing gui.page_spacing

                for page in range(max(pageOffset * 10, 1), pageOffset * 10 + 10):
                    textbutton "[page]" action FilePage(page)

            hbox at right:
                spacing gui.page_spacing

                textbutton _(">") action FilePageNext(auto=False, quick=False)
                textbutton _(">>") action FilePage(currentPage + 10)

screen SSSSS_PlaythroughsPicker():
    frame:
        use SSSSS_PlaythroughsList(itemAction=SSSSS.Playthroughs.ActivatePlaythrough, hideTarget="SSSSS_PlaythroughsPicker")

screen SSSSS_EditPlaythrough(directory=None, name='', thumbnail=None, storeChoices=False, layout="normal", autosaveOnChoices=True, selectedPage=1):#MODIFY HERE
    default nameValue = name
    default storeChoicesValue = storeChoices
    default originalName = name
    python:
        print(name, "expects", autosaveOnChoices)
    default autosaveOnChoicesValue = autosaveOnChoices
    #MODIFY HERE
    default inputs = x52URM.InputGroup(
        [
            ('name', x52URM.Input(text=nameValue, updateScreenVariable="nameValue")),
        ],
        focusFirst=True,
        onSubmit=[
            SSSSS.Playthroughs.AddOrEdit(directory, x52URM.GetScreenInput('name', 'inputs'), originalName, thumbnail, URMGetScreenVariable('storeChoicesValue'), layout, URMGetScreenVariable('autosaveOnChoicesValue'), selectedPage),#MODIFY HERE
            Hide('SSSSS_EditPlaythrough')
        ]
    )

    key 'K_TAB' action inputs.NextInput()
    key 'shift_K_TAB' action inputs.PreviousInput()

    frame:
        xfill True
        yfill True
        background '#000'

        vbox:
            hbox:
                xfill True

                hbox spacing 4 yalign .5:
                    label "Edit playthrough" yalign .5

                button at right:
                    text 'x' size 24 yalign .5 color '#f00'
                    action Hide("SSSSS_EditPlaythrough")

            frame:
                background None
                yminimum x52URM.scalePxInt(450)
                padding (4, 0)

                vbox:
                    text "Name:"
                    button:
                        xminimum x52URM.scalePxInt(450)
                        key_events True
                        action inputs.name.Enable()
                        input value inputs.name

                    python:
                        computedDirectory = directory or SSSSS.Playthroughs.name_to_directory_name(nameValue)

                    text "Directory:"
                    text "saves/[computedDirectory]"

                    use x52URM_checkbox(checked=storeChoicesValue, text="Store choices", action=ToggleScreenVariable('storeChoicesValue', True, False))
                    use x52URM_checkbox(checked=autosaveOnChoicesValue, text="Autosave on choice", action=ToggleScreenVariable('autosaveOnChoicesValue', True, False))

            hbox:
                if(originalName):
                    button:
                        key_events True
                        xalign 0.5
                        action Show("SSSSS_RemovePlaythroughConfirm", playthroughName=originalName)

                        text "Remove"

                    button:
                        key_events True
                        xalign 0.5
                        action SSSSS.Playthroughs.SetThumbnailForActive()

                        text "Set current scene as thumbnail"

                button:
                    key_events True # We need this to still trigger key events defined inside of this button
                    transclude
                    xalign 0.5

                    action inputs.onSubmit
                    
                    text "Save"

screen SSSSS_RemovePlaythroughConfirm(playthroughName):
    default deleteFiles = False

    frame:
        xfill True
        yfill True
        background '#000'

        vbox:
            text "Delete playthrough [playthroughName]?"

            use x52URM_checkbox(checked=deleteFiles, text="Delete files", action=ToggleScreenVariable('deleteFiles', True, False))
            text "If you chose to delete files, you won't be able to recover the playthrough."

            hbox:
                python:
                    removeText = "Remove & delete files" if deleteFiles else "Remove"

                textbutton removeText:
                    action [SSSSS.Playthroughs.Remove(playthroughName, deleteFiles), Hide("SSSSS_RemovePlaythroughConfirm"), Hide("SSSSS_EditPlaythrough")]

                textbutton "Close":
                    action Hide("SSSSS_RemovePlaythroughConfirm")

screen SSSSS_PlaythroughsList(itemAction=None, hideTarget=None):
    vbox:
        for (playthroughName, playthrough) in SSSSS.Playthroughs.playthroughs.items():
            python:
                name = playthrough.get("name")

            button:
                action [itemAction(name), Hide(hideTarget)]

                hbox:
                    add SSSSS.Playthroughs.getThumbnailFromName(playthroughName)

                    label "[name]"
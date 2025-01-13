screen JK_DuplicatePlaythrough(playthrough):
    layer "JK_Overlay"
    style_prefix 'JK'
    modal True

    default name = ""
    default description = playthrough.description
    
    default name_input = JK.TextInput("name", auto_focus=True)
    default description_input = JK.TextInput("description", multiline=True)

    python:
        submitAction = JK.Playthroughs.DuplicatePlaythroughAction(playthrough=playthrough, name=name, description=description)

    use JK_Dialog(title="Duplicate \"" + playthrough.name + "\"", closeAction=Hide("JK_DuplicatePlaythrough")):
        style_prefix "JK"

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            pagekeys True
            ymaximum 0.85

            vbox:
                use JK_Title("Name")

                add name_input.displayable(placeholder="Click here to start writing the name")

                if(not JK.Playthroughs.isValidName(name)):
                    vbox offset JK.adjustable((15, 2), minValue=1):
                        text "Are you sure? This name already exists." color JK.Colors.warning
                        use JK_InfoBox("All existing saves of \"" + name + "\" will be deleted. This action {u}{color=[JK.Colors.error]}is irreversible{/color}{/u}!")

                use JK_YSpacer()

                use JK_Title("Description")
                add description_input.displayable(placeholder="Click here to start writing the description")

        hbox:
            xfill True
            yfill True

            style_prefix "JK_dialog_action_buttons"

            vbox:
                # Save
                hbox:
                    use JK_IconButton(icon="\ue161", text="Save", action=submitAction, key="ctrl_K_s")
                # Close
                hbox:
                    use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_DuplicatePlaythrough"))
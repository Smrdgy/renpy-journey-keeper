screen URPS_DuplicatePlaythrough(playthrough):
    layer "URPS_Overlay"
    style_prefix 'URPS'
    modal True

    default name = ""
    default description = playthrough.description
    
    default name_input = URPS.TextInput("name", auto_focus=True)
    default description_input = URPS.TextInput("description", multiline=True)

    python:
        submitAction = URPS.Playthroughs.DuplicatePlaythroughAction(playthrough=playthrough, name=name, description=description)

    use URPS_Dialog(title="Duplicate \"" + playthrough.name + "\"", closeAction=Hide("URPS_DuplicatePlaythrough")):
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

                if(not URPS.Playthroughs.isValidName(name)):
                    vbox offset URPS.adjustable((15, 2), minValue=1):
                        text "Are you sure? This name already exists." color URPS.Colors.warning
                        use URPS_InfoBox("All existing saves of \"" + name + "\" will be deleted. This action {u}{color=[URPS.Colors.error]}is irreversible{/color}{/u}!")

                use URPS_YSpacer()

                use URPS_Title("Description")
                add description_input.displayable(placeholder="Click here to start writing the description")

        hbox:
            xfill True
            yfill True

            style_prefix "URPS_dialog_action_buttons"

            vbox:
                # Save
                hbox:
                    use URPS_IconButton(icon="\ue161", text="Save", action=submitAction, key="ctrl_K_s")
                # Close
                hbox:
                    use URPS_IconButton(icon="\ue5cd", text="Close", action=Hide("URPS_DuplicatePlaythrough"))
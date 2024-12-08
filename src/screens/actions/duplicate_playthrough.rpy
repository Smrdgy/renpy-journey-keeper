screen SSSSS_DuplicatePlaythrough(playthrough):
    layer "SSSSSoverlay"
    style_prefix 'SSSSS'
    modal True

    default name = ""
    default description = playthrough.description
    
    default name_input = SSSSS.TextInput("name", auto_focus=True)
    default description_input = SSSSS.TextInput("description", multiline=True)

    python:
        submitAction = SSSSS.Playthroughs.DuplicatePlaythroughAction(playthrough=playthrough, name=name, description=description)

    key 'ctrl_K_s' action submitAction

    use SSSSS_Dialog(title="Duplicate \"" + playthrough.name + "\"", closeAction=Hide("SSSSS_DuplicatePlaythrough")):
        style_prefix "SSSSS"

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            pagekeys True
            ymaximum 0.85

            vbox:
                use SSSSS_Title("Name")

                add name_input.displayable(placeholder="Click here to start writing the name")

                if(not SSSSS.Playthroughs.isValidName(name)):
                    vbox offset adjustable((15, 2), minValue=1):
                        text "Are you sure? This name already exists." color SSSSS.Colors.warning
                        use SSSSS_InfoBox("All existing saves of \"" + name + "\" will be deleted. This action {u}{color=[SSSSS.Colors.error]}is irreversible{/color}{/u}!")

                use SSSSS_YSpacer()

                use SSSSS_Title("Description")
                add description_input.displayable(placeholder="Click here to start writing the description")

        hbox:
            xfill True
            yfill True

            style_prefix "SSSSS_dialog_action_buttons"

            vbox:
                # Save
                hbox:
                    use sssss_iconButton(icon="\ue161", text="{u}S{/u}ave", action=submitAction)
                # Close
                hbox:
                    use sssss_iconButton(icon="\ue5cd", text="Close", action=Hide("SSSSS_DuplicatePlaythrough"))
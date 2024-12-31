screen URPS_SaveMemory():
    layer "URPS_Overlay"
    style_prefix 'URPS'
    modal True

    default name = ''

    default name_input = URPS.TextInput("name", auto_focus=True)

    python:
        submitAction = [
            URPS.Memories.CreateMemory(name=name),
            Hide('URPS_SaveMemory')
        ]

    use URPS_Dialog(title="Save memory", closeAction=Hide("URPS_SaveMemory")):
        style_prefix "URPS"

        vbox:
            text "Name:"
            add name_input.displayable(placeholder="Enter name or leave blank to generate one")

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
                    use URPS_IconButton(icon="\ue5cd", text="Close", action=Hide("URPS_SaveMemory"))
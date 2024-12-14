screen URPS_SaveMemory():
    layer "URPS_Overlay"
    style_prefix 'URPS'
    modal True

    default name = ''

    python:
        submitAction = [
            URPS.Memories.CreateMemory(name=name),
            Hide('URPS_SaveMemory')
        ]

    use URPS_Dialog(title="Save memory", closeAction=Hide("URPS_SaveMemory")):
        style_prefix "URPS"

        vbox:
            text "Name:"
            add URPS.TextInput(variableName="name", editable=True)

        hbox:
            xfill True
            yfill True

            style_prefix "URPS_dialog_action_buttons"

            vbox:
                # Save
                hbox:
                    use URPS_IconButton(icon="\ue161", text="Save", action=submitAction, disabled=not name, key="ctrl_K_s")

                # Close
                hbox:
                    use URPS_IconButton(icon="\ue5cd", text="Close", action=Hide("URPS_SaveMemory"))
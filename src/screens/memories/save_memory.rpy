screen JK_SaveMemory():
    layer "JK_Overlay"
    style_prefix 'JK'
    modal True

    default name = ''

    default name_input = JK.TextInput("name", auto_focus=True)

    python:
        submitAction = [
            JK.Memories.CreateMemory(name=name),
            Hide('JK_SaveMemory')
        ]

    use JK_Dialog(title="Save memory", close_action=Hide("JK_SaveMemory")):
        style_prefix "JK"

        vbox:
            text "Name:"
            add name_input.displayable(placeholder="Enter name or leave blank to generate one")

        hbox:
            xfill True
            yfill True

            style_prefix "JK_dialog_action_buttons"

            vbox:
                # Save
                hbox:
                    use JK_IconButton(icon="\ue161", text="Save", action=submitAction, key="alt_K_s")

                # Close
                hbox:
                    use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_SaveMemory"))
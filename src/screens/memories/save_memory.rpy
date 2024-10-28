screen SSSSS_SaveMemory():
    layer "SSSSSoverlay"
    style_prefix 'SSSSS'
    modal True

    default name = ''

    python:
        submitAction = [
            SSSSS.Memories.CreateMemory(name=GetScreenVariable('name')),
            Hide('SSSSS_SaveMemory')
        ]

    key 'ctrl_K_s' action submitAction

    use SSSSS_Dialog(title="Save memory", closeAction=Hide("SSSSS_SaveMemory")):
        style_prefix "SSSSS"

        vbox:
            text "Name:"
            add SSSSS.TextInput(variableName="name", editable=True)

        hbox:
            xfill True
            yfill True

            style_prefix "SSSSS_dialog_action_buttons"

            vbox:
                # Save
                hbox:
                    use sssss_iconButton(icon="\ue161", text="{u}S{/u}ave", action=submitAction, disabled=not name)

                # Close
                hbox:
                    use sssss_iconButton(icon="\ue5cd", text="Close", action=Hide("SSSSS_SaveMemory"))
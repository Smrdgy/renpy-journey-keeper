screen SSSSS_SaveMemory(screenshot):
    layer "SSSSSoverlay"
    style_prefix 'SSSSS'

    default name = ''

    default inputs = x52URM.InputGroup(
        [
            ('name', x52URM.Input(text=name, updateScreenVariable="name"))
        ],
        focusFirst=True,
        onSubmit=[
            SSSSS.Memories.CreateMemory(name=x52URM.GetScreenInput('name', 'inputs'), screenshot=screenshot),
            Hide('SSSSS_SaveMemory')
        ]
    )

    key 'K_TAB' action inputs.NextInput()
    key 'shift_K_TAB' action inputs.PreviousInput()

    use SSSSS_Dialog(title="Save memory", closeAction=Hide("SSSSS_SaveMemory")):
        style_prefix "SSSSS"

        vbox:
            text "Name:"
            frame:
                button:
                    style_prefix "" # Have to override some other styles that are applying for some reson...

                    key_events True
                    action inputs.name.Enable()

                    input value inputs.name:
                        style "SSSSS_input_input"

        hbox:
            xfill True
            yfill True

            vbox at right:
                yalign 1.0

                # Save
                hbox at right:
                    use sssss_iconButton(icon="\ue161", text="Save", action=inputs.onSubmit, disabled=not name)

                # Close
                hbox at right:
                    use sssss_iconButton(icon="\ue5cd", text="Close", action=Hide("SSSSS_SaveMemory"))
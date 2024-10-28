screen SSSSS_ExitMemoryConfirm():
    layer "screens"
    style_prefix "SSSSS"
    modal True

    $ returnAction = [SSSSS.Memories.ExitMemory(), MainMenu(confirm=False)] #TODO: Replace MainMenu() with Return() when the restoration of a session is figured out...

    key 'K_RETURN' action returnAction #TODO: Not wokring, not sure why...
    key 'K_KP_ENTER' action returnAction #TODO: Not wokring, not sure why...
    key 'K_e' action returnAction

    use SSSSS_Dialog(title="Exit memory", closeAction=Return()):
        vbox:
            hbox:
                xfill True

                text "Do you wish to exit the memory?" xalign 0.5 text_align 0.5

            hbox:
                xfill True
                yfill True

                style_prefix "SSSSS_dialog_action_buttons"

                vbox:
                    # Save
                    hbox:
                        use sssss_iconButton(icon="\ue9ba", text="{u}E{/u}xit memory", action=returnAction)

                    # Close
                    hbox:
                        use sssss_iconButton(icon="\ue5c4", text="Return", action=Return())
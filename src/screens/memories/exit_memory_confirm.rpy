screen JK_ExitMemoryConfirm():
    layer "screens"
    style_prefix "JK"
    modal True

    $ returnAction = [JK.Memories.ExitMemory(), MainMenu(confirm=False)] #TODO: Replace MainMenu() with Return() when the restoration of a session is figured out...

    use JK_Dialog(title="Exit memory", close_action=Return()):
        key 'K_RETURN' action returnAction
        key 'K_KP_ENTER' action returnAction
    
        vbox:
            hbox:
                xfill True

                text "Do you wish to exit the memory?" xalign 0.5 text_align 0.5

            hbox:
                xfill True
                yfill True

                style_prefix "JK_dialog_action_buttons"

                vbox:
                    # Save
                    hbox:
                        use JK_IconButton(icon="\ue9ba", text="Exit memory", action=returnAction, key="ctrl_K_e")

                    # Close
                    hbox:
                        use JK_IconButton(icon="\ue5c4", text="Return", action=Return())
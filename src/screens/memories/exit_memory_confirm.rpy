screen SSSSS_ExitMemoryConfirm():
    layer "screens"
    style_prefix "SSSSS"
    modal True

    use SSSSS_Dialog(title="Exit memory", closeAction=Return()):
        vbox:
            hbox:
                xfill True

                text "Do you wish to exit the memory?" xalign 0.5 text_align 0.5

            hbox:
                xfill True
                yfill True

                vbox at right:
                    yalign 1.0

                    # Save
                    hbox at right:
                        use sssss_iconButton(icon="\ue9ba", text="Exit memory", action=[SSSSS.Memories.ExitMemory(), MainMenu(confirm=False)]) #TODO: Replace MainMenu() with Return() when the restoration of a session is figured out...

                    # Close
                    hbox at right:
                        use sssss_iconButton(icon="\ue5c4", text="Return", action=Return())
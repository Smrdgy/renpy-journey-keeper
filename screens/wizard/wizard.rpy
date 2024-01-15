screen SSSSS_NativeSaveMenu(save):
    viewport:
        use file_slots(_("Save" if save else "Load"))

        hbox:
            xfill True
            xoffset -10
            yoffset 10

            hbox at right:
                use sssss_iconButton('\uea20', tt="New playthrough", action=Show("SSSSS_EditPlaythrough"))


screen SSSSS_Wizard(save=False):
    default usePlaythroughSystem = True #TODO: Make controllable via settings

    if(usePlaythroughSystem):
        use SSSSS_PlaythroughMenu(save=save)
    else:
        use SSSSS_NativeSaveMenu(save=save)

    
screen JK_PendingUpdateError(error):
    style_prefix 'JK'
    modal True

    vbox:
        xfill True
        yfill True
        ymaximum 0.85

        vbox align (0.5, 0.5):
            hbox xalign 0.5:
                use JK_Title("Error", color=JK.Colors.danger)

            use JK_YSpacer(offset=2)

            vbox xalign 0.5:
                text error xalign 0.5 text_align 0.5

                use JK_YSpacer(offset=2)

                if JK.Updater.rpa_locked_exception:
                    text "Ren'Py is keeping the old mod file open, which is preventing the update. This is unfortunately normal for Ren'Py 8+." text_align 0.5 xalign 0.5
                    hbox ysize JK.scaled(5)
                    text "To try and fix it, click {a=JK_Run:JK.Updater.RestartGame()}Reload and update{/a}—this will reload the game, which might release the file. If the issue persists, something else may be holding the file open." text_align 0.5 xalign 0.5
                    hbox ysize JK.scaled(5)
                    text "Alternatively, you can do this yourself by closing the game, navigating to the {a=JK_Run:JK.OpenGameDirectoryAction()}/game{/a} directory of this game and renaming the file {i}\"[JK.Updater.temp_asset_name]\"{/i} to {i}\"[JK.Updater.asset_name]\"{/i}." text_align 0.5 xalign 0.5

                    use JK_ErrorFooter("PENDING_UPDATE_ERROR_RPY8_EXPECTED")
                else:
                    use JK_ErrorFooter()

    # Dialog footer
    hbox:
        xfill True
        yfill True

        style_prefix "JK_dialog_action_buttons"

        vbox:
            if JK.Updater.rpa_locked_exception:
                # Reload and update
                hbox:
                    use JK_IconButton(icon="\ue5d5", text="Reload and update", action=JK.Updater.RestartGame())
            else:
                # Retry
                hbox:
                    use JK_IconButton(icon="\ue5d5", text="Retry", action=JK.Updater.InstallUpdateAction())

            # Close
            hbox:
                use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_PendingUpdate"))
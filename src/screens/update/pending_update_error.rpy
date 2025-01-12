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

                text "For more information check log.txt" xalign 0.5 text_align 0.5
                text "If this isn't a user error (e.g. incorrect permissions), please report it at {a=https://github.com/[JK.MOD_GITHUB_OWNER]/[JK.MOD_GITHUB_REPO]/issues}https://github.com/[JK.MOD_GITHUB_OWNER]/[JK.MOD_GITHUB_REPO]/issues{/a}" xalign 0.5 text_align 0.5

    # Dialog footer
    hbox:
        xfill True
        yfill True

        style_prefix "JK_dialog_action_buttons"

        vbox:
            # OK
            hbox:
                use JK_IconButton(icon="\ue5d5", text="Retry", action=JK.Updater.InstallUpdateAction())

            # Close
            hbox:
                use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_PendingUpdate"))
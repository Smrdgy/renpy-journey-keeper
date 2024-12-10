screen URPS_PendingUpdateError(error):
    style_prefix 'URPS'
    modal True

    vbox:
        xfill True
        yfill True
        ymaximum 0.85

        vbox align (0.5, 0.5):
            hbox xalign 0.5:
                use URPS_Title("Error", color=URPS.Colors.danger)

            use URPS_YSpacer(offset=2)

            vbox xalign 0.5:
                text error xalign 0.5 text_align 0.5

                use URPS_YSpacer(offset=2)

                text "For more information check log.txt" xalign 0.5 text_align 0.5
                text "If this isn't a user error (e.g. incorrect permissions), please report it at {a=https://github.com/[URPS.MOD_GITHUB_OWNER]/[URPS.MOD_GITHUB_REPO]/issues}https://github.com/[URPS.MOD_GITHUB_OWNER]/[URPS.MOD_GITHUB_REPO]/issues{/a}" xalign 0.5 text_align 0.5

    # Dialog footer
    hbox:
        xfill True
        yfill True

        style_prefix "URPS_dialog_action_buttons"

        vbox:
            # OK
            hbox:
                use URPS_IconButton(icon="\ue5d5", text="Retry", action=URPS.Updater.InstallUpdateAction())

            # Close
            hbox:
                use URPS_IconButton(icon="\ue5cd", text="Close", action=Hide("URPS_PendingUpdate"))
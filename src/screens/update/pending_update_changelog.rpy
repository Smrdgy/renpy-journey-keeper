screen SSSSS_PendingUpdateChangelog(version, changelog):
    style_prefix 'SSSSS'
    modal True

    viewport:
        mousewheel True
        draggable True
        scrollbars "vertical"
        pagekeys True
        ymaximum 0.85

        vbox:
            text changelog or "{i}\"Looks like I was in so much hurry that I even forgot to write a changelog entry. Sorry!\"{/i}\n -- Smrdgy"

            use SSSSS_YSpacer(offset=2)

            text "If you want to check for yourself what has changed, visit {a=https://github.com/[SSSSS.MOD_GITHUB_OWNER]/[SSSSS.MOD_GITHUB_REPO]/commits/}https://github.com/[SSSSS.MOD_GITHUB_OWNER]/[SSSSS.MOD_GITHUB_REPO]/commits/{/a}"

    hbox:
        xfill True
        yfill True

        style_prefix "SSSSS_dialog_action_buttons"

        vbox:
            # Download and install
            hbox:
                use sssss_iconButton(icon="\ue884", text="Download & install", action=SSSSS.Updater.InstallUpdateAction(version), color=SSSSS.Colors.success)

            # Skip this update
            hbox:
                use sssss_iconButton(icon="\ue14b", text="Skip this one out", action=[SSSSS.Updater.SkipUpdateAction(version), Hide("SSSSS_PendingUpdate")])

            # Disable updates
            hbox:
                use sssss_iconButton(icon="\ue888", text="Disable updates", action=[SSSSS.Updater.DisableUpdatesAction(), Hide("SSSSS_PendingUpdate")], color=SSSSS.Colors.danger)

            # Close
            hbox:
                use sssss_iconButton(icon="\ue5cd", text="Close", action=Hide("SSSSS_PendingUpdate"))
screen URPS_PendingUpdateChangelog(version, changelog):
    style_prefix 'URPS'
    modal True

    viewport:
        mousewheel True
        draggable True
        scrollbars "vertical"
        pagekeys True
        ymaximum 0.85

        vbox:
            text changelog or "{i}\"Looks like I was in so much hurry that I even forgot to write a changelog entry. Sorry!\"{/i}\n -- Smrdgy"

            use URPS_YSpacer(offset=2)

            text "If you want to check for yourself what has changed, visit {a=https://github.com/[URPS.MOD_GITHUB_OWNER]/[URPS.MOD_GITHUB_REPO]/commits/}https://github.com/[URPS.MOD_GITHUB_OWNER]/[URPS.MOD_GITHUB_REPO]/commits/{/a}"

    hbox:
        xfill True
        yfill True

        style_prefix "URPS_dialog_action_buttons"

        hbox:
            style_prefix "URPS"

            text "{a=https://github.com/[URPS.MOD_GITHUB_OWNER]/[URPS.MOD_GITHUB_REPO]/releases/latest}{color=[URPS.Colors.text_light]}For manual download, click here.{/color}{/a}" yalign 0.5
            use URPS_Icon(icon="\ue895", size=20, color=URPS.Colors.text_light, hover_color=URPS.Colors.text_light)

        vbox:
            # Download and install
            hbox:
                use URPS_IconButton(icon="\ue884", text="Download & install", action=URPS.Updater.InstallUpdateAction(), color=URPS.Colors.success)

            # Skip this update
            hbox:
                use URPS_IconButton(icon="\ue14b", text="Skip this one out", action=[URPS.Updater.SkipUpdateAction(version), Hide("URPS_PendingUpdate")])

            # Disable updates
            hbox:
                use URPS_IconButton(icon="\ue888", text="Disable updates", action=[URPS.Updater.DisableUpdatesAction(), Hide("URPS_PendingUpdate")], color=URPS.Colors.danger)

            # Close
            hbox:
                use URPS_IconButton(icon="\ue5cd", text="Close", action=Hide("URPS_PendingUpdate"))
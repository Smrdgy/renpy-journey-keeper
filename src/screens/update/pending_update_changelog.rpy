screen JK_PendingUpdateChangelog(release):
    style_prefix 'JK'
    modal True

    viewport:
        mousewheel True
        draggable True
        scrollbars "vertical"
        vscrollbar_unscrollable "hide"
        pagekeys True
        ymaximum 0.85

        vbox:
            text release.changelog or "{i}\"Looks like I was in so much hurry that I even forgot to write a changelog entry. Sorry!\"{/i}\n -- Smrdgy"

            use JK_YSpacer(offset=2)

            text "If you want to check for yourself what has changed, visit {a=https://github.com/[JK.MOD_GITHUB_OWNER]/[JK.MOD_GITHUB_REPO]/commits/}https://github.com/[JK.MOD_GITHUB_OWNER]/[JK.MOD_GITHUB_REPO]/commits/{/a}"

    hbox:
        xfill True
        yfill True

        style_prefix "JK_dialog_action_buttons"

        hbox:
            style_prefix "JK"

            text "{a=https://github.com/[JK.MOD_GITHUB_OWNER]/[JK.MOD_GITHUB_REPO]/releases/latest}{color=[JK.Colors.text_light]}For manual download, click here.{/color}{/a}" yalign 0.5
            use JK_Icon(icon="\ue895", size=20, color=JK.Colors.text_light, hover_color=JK.Colors.text_light)

        vbox:
            # Download and install
            hbox:
                use JK_IconButton(icon="\ue884", text="Download & install", action=JK.Updater.InstallUpdateAction(release), color=JK.Colors.success)

            # Skip this update
            hbox:
                use JK_IconButton(icon="\ue14b", text="Skip this one out", action=[JK.Updater.SkipUpdateAction(release.version), Hide("JK_PendingUpdate")])

            # Disable updates
            hbox:
                use JK_IconButton(icon="\ue888", text="Disable updates", action=[JK.Updater.DisableUpdatesAction(), Hide("JK_PendingUpdate")], color=JK.Colors.danger)

            # Close
            hbox:
                use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_PendingUpdate"))
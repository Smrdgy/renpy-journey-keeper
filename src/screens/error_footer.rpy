screen JK_ErrorFooter(source=None):
    default report_it_text = "{a=[JK.DISCORD_URL]}Discord{/a} or {a=https://github.com/[JK.MOD_GITHUB_OWNER]/[JK.MOD_GITHUB_REPO]/issues}https://github.com/[JK.MOD_GITHUB_OWNER]/[JK.MOD_GITHUB_REPO]/issues{/a}"

    if source == "PENDING_UPDATE_ERROR_RPY8_EXPECTED":
        text "If this isn't a user error and the problem persists even after restarting the game, please report it at " + report_it_text xalign 0.5 text_align 0.5
    else:
        text "For more information check log.txt" xalign 0.5 text_align 0.5

        use JK_YSpacer(2)

        text "If this isn't a user error (e.g. incorrect permissions, manually deleted files, etc.), please report it at " + report_it_text xalign 0.5 text_align 0.5
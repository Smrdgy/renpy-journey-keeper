screen URPS_PendingUpdate(version, changelog):
    layer "URPS_Overlay"
    style_prefix 'URPS'
    modal True

    use URPS_Dialog(title="[URPS.MOD_NAME] - Update found", message="{color=[URPS.Colors.theme]}{b}v" + version + "{/b}{/color}\n{size=-7}{color=[URPS.Colors.text_light]}(current: [URPS.MOD_VERSION]){/color}{/size}", closeAction=Hide("URPS_PendingUpdate")):
        if URPS.Updater.downloading:
            use URPS_PendingUpdateDownloading()
        elif URPS.Updater.installing:
            use URPS_PendingUpdateInstalling()
        elif URPS.Updater.error:
            use URPS_PendingUpdateError(URPS.Updater.error)
        elif URPS.Updater.installed:
            use URPS_PendingUpdateSuccess()
        else:
            use URPS_PendingUpdateChangelog(version, changelog)
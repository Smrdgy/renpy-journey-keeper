screen SSSSS_PendingUpdate(version, changelog):
    layer "SSSSSoverlay"
    style_prefix 'SSSSS'
    modal True

    use SSSSS_Dialog(title="[SSSSS.MOD_NAME] - Update found", message="{color=[SSSSS.Colors.theme]}{b}v" + version + "{/b}{/color}", closeAction=Hide("SSSSS_PendingUpdate")):
        if SSSSS.Updater.downloading:
            use SSSSS_PendingUpdateDownloading()
        elif SSSSS.Updater.installing:
            use SSSSS_PendingUpdateInstalling()
        elif SSSSS.Updater.error:
            use SSSSS_PendingUpdateError(SSSSS.Updater.error)
        elif SSSSS.Updater.installed:
            use SSSSS_PendingUpdateSuccess()
        else:
            use SSSSS_PendingUpdateChangelog(version, changelog)
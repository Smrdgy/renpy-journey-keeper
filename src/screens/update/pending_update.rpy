screen JK_PendingUpdate(release):
    layer "JK_Overlay"
    style_prefix 'JK'
    modal True

    use JK_Dialog(title="[JK.MOD_NAME] - Update found", message="{color=[JK.Colors.theme]}{b}v" + release.version + "{/b}{/color}\n{size=-4}{color=[JK.Colors.text_light]}(current: [JK.MOD_VERSION]){/color}{/size}", close_action=Hide("JK_PendingUpdate")):
        if JK.Updater.downloading:
            use JK_PendingUpdateDownloading()
        elif JK.Updater.installing:
            use JK_PendingUpdateInstalling()
        elif JK.Updater.reload_and_update:
            use JK_PendingUpdateReloadAndUpdate()
        elif JK.Updater.error:
            use JK_PendingUpdateError(release, JK.Updater.error)
        elif JK.Updater.installed:
            use JK_PendingUpdateSuccess()
        else:
            use JK_PendingUpdateChangelog(release)
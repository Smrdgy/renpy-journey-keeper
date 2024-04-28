screen SSSSS_PlaythroughsPicker():
    style_prefix 'SSSSS'
    use SSSSS_Dialog(title="Select a playthrough", closeAction=Hide("SSSSS_PlaythroughsPicker"), background="gui/select_playthrough_dialog_background.png", size=(x52URM.scalePxInt(581), x52URM.scalePxInt(623))):
        style_prefix "SSSSS"

        use SSSSS_PlaythroughsList(itemAction=SSSSS.Playthroughs.ActivatePlaythrough, hideTarget="SSSSS_PlaythroughsPicker", canEdit=True, highlightActive=True)
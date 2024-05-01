screen SSSSS_PlaythroughsPicker():
    layer "SSSSSoverlay"
    style_prefix 'SSSSS'

    use SSSSS_Dialog(title="Select a playthrough", closeAction=Hide("SSSSS_PlaythroughsPicker")):
        style_prefix "SSSSS"

        use SSSSS_PlaythroughsList(itemAction=SSSSS.Playthroughs.ActivatePlaythrough, hideTarget="SSSSS_PlaythroughsPicker", canEdit=True, highlightActive=True)
screen SSSSS_PlaythroughsList(itemAction=None, hideTarget=None, canEdit=False, highlightActive=False):
    style_prefix 'SSSSS'
    viewport:
        mousewheel True
        draggable True
        scrollbars "vertical"
        pagekeys True

        vbox:
            xfill True

            for playthrough in SSSSS.Playthroughs.playthroughs:
                button:
                    xfill True

                    if(hideTarget):
                        action [itemAction(playthrough), Hide(hideTarget)]
                    else:
                        action itemAction(playthrough)

                    hbox:
                        xfill True

                        add playthrough.getThumbnail(60, 60)

                        hbox xsize 10

                        hbox:
                            xfill True

                            text "[playthrough.name]":
                                if(highlightActive and (SSSSS.Playthroughs.activePlaythrough == playthrough or (playthrough.id == 1 and SSSSS.Playthroughs.activePlaythrough == None))):
                                    color '#abe9ff'

                        if(canEdit):
                            hbox:
                                offset (-100, 0)

                                use sssss_iconButton('\ue872', tt="Remove playthrough", action=Show("SSSSS_RemovePlaythroughConfirm", playthrough=playthrough), disabled=playthrough.id == 1)

                                use sssss_iconButton('\ue3c9', tt="Edit playthrough", action=Show("SSSSS_EditPlaythrough", playthrough=playthrough, isEdit=True))
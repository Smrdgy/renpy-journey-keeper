screen SSSSS_MemoriesLibrary():
    layer "SSSSSoverlay"
    style_prefix 'SSSSS'
    modal True

    default columns = 4
    default thumbnailSize = (int((renpy.config.screen_width - 100) / columns - renpy.config.screen_width / 20), 200)

    use SSSSS_Dialog(title="Select a memory to play", closeAction=Hide("SSSSS_MemoriesLibrary")):
        style_prefix "SSSSS"

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            pagekeys True

            python:
                memories = SSSSS.Memories.getMemories()
                totalMemories = len(memories)
                rows = totalMemories // columns
                if totalMemories % columns != 0:
                    rows += 1
                spotsToFill = rows * columns - totalMemories

            grid columns rows:
                xfill True
                spacing 20

                for slotname in memories:
                    button:
                        key_events True
                        xmaximum renpy.config.screen_width
                        ymaximum renpy.config.screen_height
                        background "#ffffff11"
                        action [Hide("SSSSS_MemoriesLibrary"), SSSSS.Memories.LoadMemoryWithConfirm(slotname)]

                        vbox at center:
                            add SSSSS.Memories.GetScreenshot(slotname) xalign 0.5

                            text slotname

                            key "save_delete" action FileDelete(slotname)

                for _ in range(0, spotsToFill):
                    text ""
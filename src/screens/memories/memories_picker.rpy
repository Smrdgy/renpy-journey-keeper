screen URPS_MemoriesLibrary():
    layer "URPS_Overlay"
    style_prefix 'URPS'
    modal True

    default columns = 4
    default thumbnailSize = (int((renpy.config.screen_width - 100) / columns - renpy.config.screen_width / 20), 200)

    use URPS_Dialog(title="Select a memory to play", closeAction=Hide("URPS_MemoriesLibrary")):
        style_prefix "URPS"

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            pagekeys True

            python:
                memories = URPS.Memories.getMemories()
                totalMemories = len(memories)
                rows = totalMemories // columns
                if totalMemories % columns != 0:
                    rows += 1
                spotsToFill = rows * columns - totalMemories

            grid columns rows:
                xfill True
                spacing 20

                for slotname in memories:
                    button style "URPS_playthrough_button":
                        xmaximum renpy.config.thumbnail_width
                        action [Hide("URPS_MemoriesLibrary"), URPS.Memories.LoadMemoryWithConfirm(slotname)]

                        vbox:
                            xpos 0.5
                            xanchor 0.5
                            ypos 1.0
                            yanchor 1.0

                            add URPS.Memories.GetScreenshot(slotname) xalign 0.5

                            text URPS.Memories.saveInstance.location.save_name(slotname) xalign 0.5 text_align 0.5

                            key "save_delete" action URPS.Memories.DeleteMemoryConfirm(slotname)

                for _ in range(0, spotsToFill):
                    text ""
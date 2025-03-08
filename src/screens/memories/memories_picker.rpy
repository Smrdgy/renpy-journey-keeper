screen JK_MemoriesLibrary():
    layer "JK_Overlay"
    style_prefix 'JK'
    modal True

    default columns = 4

    use JK_Dialog(title="Select a memory to play", close_action=Hide("JK_MemoriesLibrary")):
        style_prefix "JK"

        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            pagekeys True

            python:
                memories = JK.Memories.getMemories()
                totalMemories = len(memories)
                rows = totalMemories // columns
                if totalMemories % columns != 0:
                    rows += 1
                spotsToFill = rows * columns - totalMemories

            grid columns rows:
                xfill True
                spacing 20

                for slotname in memories:
                    button style "JK_playthrough_button":
                        xmaximum renpy.config.thumbnail_width
                        action [Hide("JK_MemoriesLibrary"), JK.Memories.LoadMemoryWithConfirm(slotname)]

                        vbox:
                            xpos 0.5
                            xanchor 0.5
                            ypos 1.0
                            yanchor 1.0

                            add JK.Memories.GetScreenshot(slotname) xalign 0.5

                            text JK.Memories.saveInstance.location.save_name(slotname) xalign 0.5 text_align 0.5

                            key "save_delete" action JK.Memories.DeleteMemoryConfirm(slotname)

                for _ in range(0, spotsToFill):
                    text ""
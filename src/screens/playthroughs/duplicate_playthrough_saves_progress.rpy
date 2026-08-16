screen JK_DuplicatePlaythroughSavesProgress(view_model):
    layer "JK_Overlay"
    style_prefix 'JK'
    modal True

    use JK_Dialog(title="Duplicating playthrough", close_action=Hide("JK_DuplicatePlaythroughSavesProgress")):
        if view_model.processing:
            python:
                processed = view_model.processed
                to_process = len(view_model.saves_to_process)

            vbox:
                xfill True
                yfill True
                ymaximum 0.85

                vbox align(0.5, 0.5):
                    xfill True
                    xmaximum 0.85

                    hbox xalign 0.5:
                        use JK_Title("Copying saves...")

                    use JK_YSpacer()

                    text "[processed]/[to_process]" xalign 0.5
                    bar value processed range to_process

            # Dialog footer
            hbox:
                xfill True
                yfill True

                style_prefix "JK_dialog_action_buttons"

                vbox:
                    hbox:
                        use JK_IconButton(icon="", text="Stop", action=[Function(view_model.process_stop), Hide("JK_DuplicatePlaythroughSavesProgress")], color=JK.Colors.danger)

        elif view_model.error:
            vbox:
                xfill True
                yfill True
                ymaximum 0.85

                vbox align (0.5, 0.5):
                    hbox xalign 0.5:
                        use JK_Title("Error", color=JK.Colors.danger)

                    use JK_YSpacer(offset=2)

                    vbox xalign 0.5:
                        text view_model.error xalign 0.5 text_align 0.5

                        use JK_YSpacer(offset=2)

                        use JK_ErrorFooter()

            # Dialog footer
            hbox:
                xfill True
                yfill True

                style_prefix "JK_dialog_action_buttons"

                vbox:
                    hbox:
                        use JK_IconButton(icon="", text="OK", action=Hide("JK_DuplicatePlaythroughSavesProgress"))

        elif view_model.success:
            vbox:
                xfill True
                yfill True
                ymaximum 0.85

                vbox align (0.5, 0.5):
                    use JK_Title("Done", color=JK.Colors.success)

            # Dialog footer
            hbox:
                xfill True
                yfill True

                style_prefix "JK_dialog_action_buttons"

                vbox:
                    hbox:
                        use JK_IconButton(icon="", text="OK", action=Hide("JK_DuplicatePlaythroughSavesProgress"))

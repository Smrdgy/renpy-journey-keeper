screen JK_MoveCopySavesOverwriteConfirm(save, viewModel):
    python:
        class SkipAction(renpy.ui.Action):
            def __init__(self, viewModel, apply_to_all):
                self.viewModel = viewModel
                self.apply_to_all = apply_to_all

            def __call__(self):
                self.viewModel.process_skip_current_save(self.apply_to_all)

        class OverwriteAction(renpy.ui.Action):
            def __init__(self, viewModel, apply_to_all):
                self.viewModel = viewModel
                self.apply_to_all = apply_to_all

            def __call__(self):
                self.viewModel.process_overwrite_current_save(self.apply_to_all)

        class CancelAction(renpy.ui.Action):
            def __init__(self, viewModel):
                self.viewModel = viewModel

            def __call__(self):
                self.viewModel.process_stop()

    layer "JK_Overlay"
    style_prefix "JK"

    modal True

    zorder 199

    default apply_to_all = False

    default thumbnail_width = renpy.config.thumbnail_width or 200 if hasattr(renpy.config, "thumbnail_width") and renpy.config.thumbnail_width < renpy.config.screen_width / 2.5 else 200
    default thumbnail_height = renpy.config.thumbnail_height or 200 if hasattr(renpy.config, "thumbnail_height") else 200

    default source_screenshot = viewModel.source_instance.location.screenshot_including_inactive(save)
    default target_screenshot = viewModel.destination_instance.location.screenshot_including_inactive(save)

    python:
        skipAction = [Hide("JK_MoveCopySavesOverwriteConfirm"), SkipAction(viewModel=viewModel, apply_to_all=apply_to_all)]
        overwriteAction = [Hide("JK_MoveCopySavesOverwriteConfirm"), OverwriteAction(viewModel=viewModel, apply_to_all=apply_to_all)]
        cancelAction = [Hide("JK_MoveCopySavesOverwriteConfirm"), CancelAction(viewModel=viewModel)]

    key 'K_RETURN' action cancelAction
    key 'K_KP_ENTER' action overwriteAction

    use JK_Dialog(title="Saves conflict!", message="Save " + save + " already exist in the target directory.\nPlease, select which action to perform.", closeAction=cancelAction):
        vbox:
            xfill True

            use JK_YSpacer()

            hbox xalign 0.5:
                grid 3 1:
                    if source_screenshot:
                        add source_screenshot size JK.Utils.getLimitedImageSizeWithAspectRatio(thumbnail_width, thumbnail_height) yalign 0.5
                    else:
                        add JK.ImagePlaceholder(width=thumbnail_width, height=thumbnail_height)

                    text "→" size JK.scaled(40) align (0.5, 0.5)

                    if target_screenshot:
                        add target_screenshot size JK.Utils.getLimitedImageSizeWithAspectRatio(thumbnail_width, thumbnail_height) yalign 0.5
                    else:
                        add JK.ImagePlaceholder(width=thumbnail_width, height=thumbnail_height)

            use JK_YSpacer()


        hbox:
            xfill True
            yfill True

            style_prefix "JK_dialog_action_buttons"

            vbox:
                use JK_Checkbox(checked=apply_to_all, text="Perform for all remaining conflicts", action=ToggleScreenVariable("apply_to_all", True, False))

                hbox:
                    use JK_IconButton(icon="\ue89c", text="Overwrite", action=overwriteAction, color=JK.Colors.danger)

                hbox:
                    use JK_IconButton(icon="\ue044", text="Skip", action=skipAction)

                hbox:
                    use JK_IconButton(icon="\ue5cd", text="Abort", action=cancelAction)

        

screen JK_MoveCopySavesOverwriteConfirm(save, view_model):
    python:
        class SkipAction(renpy.ui.Action):
            def __init__(self, view_model, apply_to_all):
                self.view_model = view_model
                self.apply_to_all = apply_to_all

            def __call__(self):
                self.view_model.process_skip_current_save(self.apply_to_all)

        class OverwriteAction(renpy.ui.Action):
            def __init__(self, view_model, apply_to_all):
                self.view_model = view_model
                self.apply_to_all = apply_to_all

            def __call__(self):
                self.view_model.process_overwrite_current_save(self.apply_to_all)

        class CancelAction(renpy.ui.Action):
            def __init__(self, view_model):
                self.view_model = view_model

            def __call__(self):
                self.view_model.process_stop()

    layer "JK_Overlay"
    style_prefix "JK"

    modal True

    zorder 199

    default apply_to_all = False

    default thumbnail_width = renpy.config.thumbnail_width or 200 if hasattr(renpy.config, "thumbnail_width") and renpy.config.thumbnail_width < renpy.config.screen_width / 2.5 else 200
    default thumbnail_height = renpy.config.thumbnail_height or 200 if hasattr(renpy.config, "thumbnail_height") else 200

    default source_screenshot = view_model.source_instance.location.screenshot_including_inactive(save)
    default target_screenshot = view_model.destination_instance.location.screenshot_including_inactive(save)

    python:
        skipAction = [Hide("JK_MoveCopySavesOverwriteConfirm"), SkipAction(view_model=view_model, apply_to_all=apply_to_all)]
        overwriteAction = [Hide("JK_MoveCopySavesOverwriteConfirm"), OverwriteAction(view_model=view_model, apply_to_all=apply_to_all)]
        cancelAction = [Hide("JK_MoveCopySavesOverwriteConfirm"), CancelAction(view_model=view_model)]

    key 'K_RETURN' action cancelAction
    key 'K_KP_ENTER' action overwriteAction

    use JK_Dialog(title="Saves conflict!", message="Save " + save + " already exist in the target directory.\nPlease, select which action to perform.", close_action=cancelAction):
        vbox:
            xfill True

            use JK_YSpacer()

            hbox xalign 0.5:
                grid 3 1:
                    if source_screenshot:
                        add source_screenshot size JK.Image.get_limited_image_size_with_preserved_aspect_ratio(thumbnail_width, thumbnail_height) yalign 0.5
                    else:
                        add JK.ImagePlaceholder(width=thumbnail_width, height=thumbnail_height)

                    text "→" size JK.scaled(40) align (0.5, 0.5)

                    if target_screenshot:
                        add target_screenshot size JK.Image.get_limited_image_size_with_preserved_aspect_ratio(thumbnail_width, thumbnail_height) yalign 0.5
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

        

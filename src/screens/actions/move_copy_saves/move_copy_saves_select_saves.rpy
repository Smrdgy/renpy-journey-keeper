screen SSSSS_MoveCopySavesSelectSaves(viewModel, saves_to_process, show_thumbnails):
    viewport:
        mousewheel True
        draggable True
        scrollbars "vertical"
        pagekeys True
        ymaximum 0.85

        python:
            source_saves = viewModel.source_saves
            other_saves = viewModel.destination_saves

            class FlipPlaythroughsAction(renpy.ui.Action):
                def __init__(self, source_playthrough, destination_playthrough):
                    self.source_playthrough = source_playthrough
                    self.destination_playthrough = destination_playthrough

                def __call__(self):
                    cs = renpy.current_screen()

                    if cs is None:
                        return

                    cs.scope["source_playthrough"] = self.destination_playthrough
                    cs.scope["destination_playthrough"] = self.source_playthrough
                    cs.scope["saves_to_process"] = []
                    cs.scope["viewModel"] = None

                    renpy.restart_interaction()

            class ClearSourcePlaythroughAction(renpy.ui.Action):
                def __call__(self):
                    cs = renpy.current_screen()

                    if cs is None:
                        return

                    cs.scope["viewModel"] = None
                    cs.scope["saves_to_process"] = []
                    cs.scope["source_playthrough"] = None

                    renpy.restart_interaction()

            class ClearDestinationPlaythroughAction(renpy.ui.Action):
                def __call__(self):
                    cs = renpy.current_screen()

                    if cs is None:
                        return

                    cs.scope["viewModel"] = None
                    cs.scope["saves_to_process"] = []
                    cs.scope["destination_playthrough"] = None

                    renpy.restart_interaction()

        vbox:
            xfill True

            grid 5 1:
                xfill True

                hbox # Dummy

                textbutton viewModel.source_playthrough.name text_color "#abe9ff":
                    action ClearSourcePlaythroughAction()

                textbutton "→" action FlipPlaythroughsAction(viewModel.source_playthrough, viewModel.destination_playthrough)

                textbutton viewModel.destination_playthrough.name text_color "#abe9ff":
                    action ClearDestinationPlaythroughAction()

                hbox # Dummy

            hbox:
                xfill True

                vbox xalign 1.0:
                    use SSSSS_Checkbox(checked=show_thumbnails, text="Show thumbnails", action=SetScreenVariable("show_thumbnails", not show_thumbnails))
                    text "{size=-5}(Might be laggy or outright crash){/size}" xalign 1.0 offset adjustable((0, -10), minValue=1)

            vbox:
                spacing 2

                # Toglle all button
                button:
                    xfill True
                    action ToggleScreenVariable("saves_to_process", [] + source_saves, [])

                    hbox:
                        xfill True
                        use SSSSS_Checkbox(checked=None if len(saves_to_process) != len(source_saves) and len(saves_to_process) > 0 else len(saves_to_process) == len(source_saves), text="")

                        text str(len(saves_to_process)) + " selected" yalign 0.5

                $ i = 0
                for save in source_saves:
                    $ i += 1

                    button style ("SSSSS_row_button" if i % 2 == 0 else "SSSSS_row_odd_button") selected save in saves_to_process:
                        xfill True
                        action ToggleSetMembership(saves_to_process, save)

                        #TODO: Add screenshots @see FileLocation:screenshot

                        grid 5 1:
                            xfill True
                            use SSSSS_Checkbox(checked=save in saves_to_process, text="")

                            # Source
                            hbox yalign 0.5:
                                if show_thumbnails:
                                    image viewModel.source_instance.location.screenshot_including_inactive(save) size SSSSS.Utils.getLimitedImageSizeWithAspectRatio(100, 80)

                                use SSSSS_XSpacer()

                                hbox yalign 0.5:
                                    if save in source_saves:
                                        text save
                                    else:
                                        text "N/A" color "#f2f2f255"

                            text "→" yalign 0.5 xsize 40

                            # Other
                            hbox yalign 0.5:
                                hbox yalign 0.5:
                                    if save in other_saves:
                                        text save
                                    else:
                                        text "N/A" color "#f2f2f255"

                                use SSSSS_XSpacer()

                                if show_thumbnails:
                                    image viewModel.destination_instance.location.screenshot_including_inactive(save) size SSSSS.Utils.getLimitedImageSizeWithAspectRatio(100, 80)

                            hbox yalign 0.5:
                                text "Conflict!" color ("#ff9100" if save in other_saves else "#ffffff00")
        
    # Dialog footer
    hbox:
        xfill True
        yfill True

        style_prefix "SSSSS_dialog_action_buttons"

        vbox:
            # Move
            hbox:
                use sssss_iconButton(icon="\ue675", text="Move", action=SSSSS.MoveCopySavesViewModel.StartProcessAction(viewModel, saves_to_process, mode="MOVE"), disabled=len(saves_to_process) == 0)

            # Copy
            hbox:
                use sssss_iconButton(icon="\ue161", text="Copy", action=SSSSS.MoveCopySavesViewModel.StartProcessAction(viewModel, saves_to_process), disabled=len(saves_to_process) == 0)

            # Close
            hbox:
                use sssss_iconButton(icon="\ue5cd", text="Close", action=Hide("SSSSS_MoveCopySaves"))
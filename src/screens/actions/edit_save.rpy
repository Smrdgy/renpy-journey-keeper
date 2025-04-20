screen JK_EditSave(slotname, location=None):
    layer "JK_Overlay"
    style_prefix 'JK'
    modal True

    default view_model = JK.EditSaveViewModel(slotname, location)

    default choice = view_model.choice
    default name = view_model.name

    default choice_input = JK.TextInput("choice")
    default name_input = JK.TextInput("name", auto_focus=True)

    if JK.TextInput.is_active("choice") or JK.TextInput.is_active("name"):
        key 'K_ESCAPE' action JK.TextInput.SetActiveAction(None)

    $ save_action = [JK.EditSaveViewModel.Save(view_model, name, choice), Hide("JK_EditSave")]

    key "ctrl_K_s" action save_action

    use JK_Dialog(title="Edit save", close_action=Hide("JK_EditSave")):
        if view_model.save_json:
            viewport:
                mousewheel True
                draggable True
                scrollbars "vertical"
                vscrollbar_unscrollable "hide"
                pagekeys True
                ymaximum 0.85

                vbox:
                    button:
                        action name_input.get_enable_action()
                        key_events True

                        vbox:
                            text "Name"
                            add name_input.displayable(placeholder="Click here to start writing")
                            frame style "JK_default" background "#ffffff22" hover_background JK.Colors.hover ysize 2 offset JK.scaled((0, 2))

                            hbox:
                                xalign 1.0

                                text str(len(name))

                    use JK_InfoBox("For a standard save slot size, you can fit 2-3 lines, each containing approximately 30 characters.")

                    use JK_YSpacer()

                    button:
                        action choice_input.get_enable_action()
                        key_events True

                        vbox:
                            text "Choice"
                            add choice_input.displayable(placeholder="Click here to start writing")
                            frame style "JK_default" background "#ffffff22" hover_background JK.Colors.hover ysize 2 offset JK.scaled((0, 2))

        else:
            hbox:
                xfill True
                yfill True

                use JK_Title("Save couldn't be loaded", color=JK.Colors.error)

        # Dialog footer
        hbox:
            style_prefix "JK_dialog_action_buttons"
            xfill True
            yfill True

            vbox xalign 1.0:
                # Save
                hbox:
                    use JK_IconButton(icon="\ue161", text="Save", action=save_action, color=JK.Colors.success, key="alt_K_s")

                # Close
                hbox:
                    use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_EditSave"))
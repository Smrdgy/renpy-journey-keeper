screen JK_MoveCopySavesError(view_model, saves_list_view_model):
    style_prefix 'JK'
    modal True

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
            # OK
            hbox:
                use JK_IconButton(icon="", text="OK", action=JK.SavesListViewModel.FinishMoveCopyAction(saves_list_view_model))

            # Close
            hbox:
                use JK_IconButton(icon="\ue5cd", text="Close", action=Hide("JK_SavesList"))
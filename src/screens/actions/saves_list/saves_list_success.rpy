screen SSSSS_SavesListSuccess(viewModel):
    style_prefix 'SSSSS'
    modal True

    vbox:
        xfill True
        yfill True
        ymaximum 0.85

        vbox align (0.5, 0.5):
            use SSSSS_Title("Done", color=SSSSS.Colors.success)

    # Dialog footer
    hbox:
        xfill True
        yfill True

        style_prefix "SSSSS_dialog_action_buttons"

        vbox:
            # Close
            hbox:
                if viewModel.return_on_success:
                    use sssss_iconButton(icon="", text="OK", action=SSSSS.SavesListViewModel.ClearSuccessAction(viewModel))
                else:
                    use sssss_iconButton(icon="", text="OK", action=Hide("SSSSS_SavesList"))
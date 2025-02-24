screen JK_SearchPlaythrough():
    layer "JK_Overlay"
    style_prefix "JK"
    modal True

    default search = ""
    default viewModel = JK.SearchPlaythroughViewModel()
    default search_input = JK.TextInput("search", auto_focus=True)
    default focused_button = None

    if JK.TextInput.is_active("search"):
        key 'K_ESCAPE' action JK.TextInput.SetActiveAction(None)

    python:
        hide_action = Hide("JK_SearchPlaythrough")

        def result_to_text(result):
            t = result[0]

            if t == "PLAYTHROUGH_NAME":
                return "Playthrough name"
            elif t == "PLAYTHROUGH_DESCRIPTION":
                return "Playthrough description"
            elif t == "FILE_PAGE_NAME":
                return "Page name"
            elif t == "SAVE_NAME":
                return "Save name"
            elif t == "SAVE_CHOICE":
                return "Choice"
        
        def result_to_action(result):
            t = result[0]

            if t == "PLAYTHROUGH_NAME":
                return None #TODO
            elif t == "PLAYTHROUGH_DESCRIPTION":
                return None #TODO
            elif t == "FILE_PAGE_NAME":
                return FilePage(result[2])
            elif t == "SAVE_NAME":
                page, _ = JK.Utils.split_slotname(result[2])
                return FilePage(page)
            elif t == "SAVE_CHOICE":
                page, _ = JK.Utils.split_slotname(result[2])
                return FilePage(page)

    use JK_Dialog(title="Seach playthrough", closeAction=Hide("JK_SearchPlaythrough")):
        button:
            action NullAction()
            key_events True

            vbox:
                add search_input.displayable(placeholder="Search")
                $ viewModel.set_search_text(search)
                frame style "JK_default" background "#ffffff22" hover_background JK.Colors.hover ysize 2 offset JK.scaled((0, 2))

        hbox:
            xalign 1.0

            # TODO: Add search in multiple playthroughs
            # use JK_Checkbox(viewModel.search_playthrough_names, text="Search playthrough names", size=JK.scaled(15), action=JK.SearchPlaythroughViewModel.SetSearchEnabled(viewModel, "search_playthrough_names"))
            # use JK_Checkbox(viewModel.search_playthrough_descriptions, text="Search playthrough descriptions", size=JK.scaled(15), action=JK.SearchPlaythroughViewModel.SetSearchEnabled(viewModel, "search_playthrough_descriptions"))
            use JK_Checkbox(viewModel.search_page_names, text="Search page names", size=JK.scaled(15), action=JK.SearchPlaythroughViewModel.SetSearchEnabled(viewModel, "search_page_names"))
            use JK_Checkbox(viewModel.search_save_names, text="Search save names", size=JK.scaled(15), action=JK.SearchPlaythroughViewModel.SetSearchEnabled(viewModel, "search_save_names"))
            use JK_Checkbox(viewModel.search_choices, text="Search choices", size=JK.scaled(15), action=JK.SearchPlaythroughViewModel.SetSearchEnabled(viewModel, "search_choices"))

        if viewModel.searching or viewModel.search_after_cache_is_built:
            text "Searching..."

        if viewModel.searched and len(viewModel.search_text) > 0:
            if len(viewModel.results) > 0:
                text "Found {}".format(len(viewModel.results))
            else:
                text "No results"

            for result in viewModel.results:
                python:
                    hovered = result == focused_button
                    i = 0

                button:
                    action [result_to_action(result), hide_action]
                    hovered SetScreenVariable("focused_button", result)
                    style ("JK_row_button" if i % 2 == 0 else "JK_row_odd_button")
                    selected False

                    $ i += 1

                    hbox:
                        xfill True
                        ysize JK.scaled(40)

                        hbox:
                            align (0.0, 0.5)
                            spacing JK.scaled(5)

                            text "{size=-5}" + result_to_text(result) + "{/size}" yalign 0.5 color JK.Colors.text_light
                            text result[1]

                            if result[0] in ("SAVE_NAME", "SAVE_CHOICE"):
                                text "{size=-5}(" + result[2] + "){/size}" yalign 0.5 color JK.Colors.text_light

                        if hovered:
                            hbox:
                                xalign 1.0

                                if result[0] in ("FILE_PAGE_NAME"):
                                    use JK_IconButton(icon="\ue8a0", tt="Show page", action=[FilePage(result[2]), hide_action])
        
                                if result[0] in ("SAVE_NAME", "SAVE_CHOICE"):
                                    $ page, slot = JK.Utils.split_slotname(result[2])
                                    use JK_IconButton(icon="\ue1c4", tt="Load save", action=[FileLoad(slot, confirm=True, page=page), hide_action])
        

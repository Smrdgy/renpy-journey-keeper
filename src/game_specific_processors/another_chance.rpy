init 1 python in JK:
    _constant = True

    if renpy.config.name == "Another Chance":
        def __callback(text, original_text, choice):
            if text is not None and "|" in original_text and original_text.startswith("?"):
                try:
                    return original_text.split("|")[-1].replace("\\\"", "")
                except:
                    pass

        before_storing_choice_text_callbacks.append(__callback)
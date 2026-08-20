init 1 python in JK.api.callbacks:
    JK = renpy.exports.store.JK

    # Called whenever a new playthrough instance is created
    new_playthrough_instance_callbacks = JK.new_playthrough_instance_callbacks

    # Called whenever the playthroughs are being collected for display, like for "Select playthrough" screen or the number on the sidepanel
    playthroughs_filter_callbacks = JK.playthroughs_filter_callbacks

    # Called right before passing the name into the pending autosave
    before_storing_choice_text_callbacks = JK.before_storing_choice_text_callbacks

    # Called while a menu is displayed and Autocomplete can't find it via the default "choice"
    # screen, so a game with a custom choice screen can supply the current options itself
    autocomplete_get_current_choices_callbacks = JK.autocomplete_get_current_choices_callbacks
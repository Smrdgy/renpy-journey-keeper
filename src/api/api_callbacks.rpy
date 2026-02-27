init 1 python in JK.api.callbacks:
    JK = renpy.exports.store.JK

    # Called whenever a new playthrough instance is created
    new_playthrough_instance_callbacks = JK.new_playthrough_instance_callbacks

    # Called whenever the playthroughs are being collected for display, like for "Select playthrough" screen or the number on the sidepanel
    playthroughs_filter_callbacks = JK.playthroughs_filter_callbacks

    # Called right before passing the name into the pending autosave
    before_storing_choice_text_callbacks = JK.before_storing_choice_text_callbacks
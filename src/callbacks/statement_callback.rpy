init 9999 python in JK:
    _constant = True

    def __wait_for_start_label_callback(statement):
        if Autosaver.prevent_autosaving and statement == "label":
            current = renpy.game.context().current
            script = renpy.game.script.lookup(current)

            if script.name == "start":
                Autosaver.prevent_autosaving = False
                renpy.store.JK_ActiveSlot = Utils.get_first_slotname()

    renpy.config.statement_callbacks.append(__wait_for_start_label_callback)
init 1 python in JK.api.autosaver:
    """
    Here you can find all the functions and actions related to the playthroughs

    Terminology:
        Autosave: Not to be confused with Ren'Py's native autosave-- this system performs a "manual save" in numbered pages when a player makes a choice.

        Active slot: A `"[page]-[slot]"` string representing the currently targeted slot for autosave or quick save.
    """

    JK = renpy.exports.store.JK

    def set_active_slot(slotname, ignore_large_jump=False):
        """
        Sets currently active slot

        Args:
            slotname (str): Ren'Py's "[page]-[slot]" slotname
            ignore_large_jump (str): When True, it will ignore big changes in page numbers (bigger than 1) instead of showing a confirmation dialog. This was needed for games that perform manual saves on some distant pages in certain parts of their story, which then confused the counter.
        """

        JK.Autosaver.set_active_slot(slotname=slotname, ignore_large_jump=ignore_large_jump)

    def get_current_slot():
        """
        Returns currently active slot (tuple):
            page (int)
            slot (int)
            slotname (str): Basically as it originally was, the whole "[page]-[slot]" string
        """
        return JK.Autosaver.get_current_slot()

    def get_next_slot():
        """
        Returns one slot after the active slot, based on the page size (tuple):
            page (int)
            slot (int)
            slotname (str): Combined "[page]-[slot]" string
        """
        return JK.Autosaver.get_next_slot()

    def use_next_slot():
        """ Uses the next slot as current """
        JK.Autosaver.set_next_slot()

    def perform_autosave(choice_label=None):
        """
        Performs an autosave

        Args:
            choice_label (str?): The label the choice button contains, this will be then stored and displayed on the timeline
        """
        JK.Autosaver.create_pending_save(choice=choice_label)
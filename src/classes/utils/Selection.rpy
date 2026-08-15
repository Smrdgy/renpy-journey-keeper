init python in JK:
    _constant = True

    import pygame_sdl2 as pygame

    class SelectionState(x52NonPicklable):
        """
        Generic Windows-Explorer-style multi-selection state: plain click
        replaces the selection, shift+click selects/toggles a contiguous
        range from the last "anchor" item, ctrl+click cherry-picks one
        item, and select_all()/toggle_all()/reset() cover the bulk cases.

        Compose this into a concrete view model (`self.selection =
        SelectionState()`) rather than reimplementing shift/ctrl-click
        bookkeeping per screen.

        `items` is kept a plain, unwrapped list so builtin actions like
        ToggleSetMembership(view_model.selection.items, id) keep working
        directly against it.
        """

        def __init__(self):
            self.items = []
            self.anchor = None

        @property
        def areAllSelected(self, total):
            return len(self.items) == total

        def select_only(self, id):
            self.items = [id]
            self.anchor = id
            renpy.restart_interaction()

        def toggle(self, id):
            if id in self.items:
                self.items.remove(id)
            else:
                self.items.append(id)
            self.anchor = id
            renpy.restart_interaction()

        def select_range(self, ordered_ids, id):
            # Returns True if a range was applied. Deliberately does NOT
            # advance self.anchor on success - repeated shift-clicks all
            # measure from the same fixed anchor.
            if not ordered_ids or self.anchor is None or self.anchor not in ordered_ids or id not in ordered_ids:
                return False

            start = ordered_ids.index(self.anchor)
            end = ordered_ids.index(id)

            new_items = []
            for item in ordered_ids[min(start, end):max(start, end) + 1]:
                if item in new_items:
                    new_items.remove(item)
                else:
                    new_items.append(item)

            self.items = new_items
            renpy.restart_interaction()
            return True

        def click(self, id, ordered_ids=None, range_eligible=True):
            mods = pygame.key.get_mods()

            if range_eligible and (mods & pygame.KMOD_SHIFT):
                if self.select_range(ordered_ids, id):
                    return

                # Shift held but no valid range (no anchor yet, or anchor/id
                # missing from ordered_ids): selection untouched, anchor
                # still relocates.
                self.anchor = id
                renpy.restart_interaction()
            elif mods & pygame.KMOD_LCTRL:
                self.toggle(id)
            else:
                self.select_only(id)

        def select_all(self, ids):
            self.items = [] + list(ids)
            renpy.restart_interaction()

        def select_none(self):
            self.items = []
            renpy.restart_interaction()

        def toggle_all(self, ids):
            if len(self.items) < len(ids):
                self.items = [] + list(ids)
            else:
                self.items = []
            renpy.restart_interaction()

        def reset(self):
            self.items = []
            self.anchor = None
            renpy.restart_interaction()

        class SelectAllAction(renpy.ui.Action):
            def __init__(self, selection, ids):
                self.selection = selection
                self.ids = ids

            def __call__(self):
                self.selection.select_all(self.ids)

        class ToggleAllAction(renpy.ui.Action):
            def __init__(self, selection, ids):
                self.selection = selection
                self.ids = ids

            def __call__(self):
                self.selection.toggle_all(self.ids)

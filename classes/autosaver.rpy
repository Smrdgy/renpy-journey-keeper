# Unfortunately this must be saved into the save game, so the system can properly recognize which slot to use next,
# especially when a manual save is made somewhere in between and then a rollback occurs.
default SSSSS_ActiveSlot = "1-1" 

init -999 python in SSSSS:
    import time

    _constant = True

    class AutosaverClass():
        suppressAutosaveConfirm = False

        @property
        def slotsPerPage(self):
            return renpy.store.gui.file_slot_cols * renpy.store.gui.file_slot_rows

        def setActiveSlot(self, slot):
            self.suppressAutosaveConfirm = False

            renpy.store.SSSSS_ActiveSlot = slot

        def getNextSlot(self):
            page, slot = renpy.store.SSSSS_ActiveSlot.split('-')
            page = int(page)
            slot = int(slot)

            slot += 1

            if(slot > self.slotsPerPage):
                slot = 1
                page += 1

            slotString = str(page) + "-" + str(slot)

            return page, slot, slotString

        def incrementActiveSlot(self):
            _, _, slotString = self.getNextSlot()

            renpy.store.SSSSS_ActiveSlot = slotString

        def handlePress(self):
            if(Choices.isDisplayingChoice and Playthroughs.activePlaythrough.autosaveOnChoices):
                #TODO: Don't take a screenshot if screenshots are disabled for the playthrough
                renpy.take_screenshot() # Must take a screenshot before anything else happens just in case the yesno_screen appears or something that might screw up the shot

                page, slot, slotString = self.getNextSlot()
                nextSlot = slotString

                # If the save slot is not bigger than the very last one, do once a confirm whether to disable autosaving
                if renpy.scan_saved_game(nextSlot) and not self.suppressAutosaveConfirm:
                    showConfirm(
                        title=("Are you sure you want to overwrite your save?"),
                        message=("By choosing \"No\", the autosave feature will disable itself until you re-enable it again."),
                        yes=[
                            Autosaver.Save(nextSlot),
                            self.IncrementActiveSlot()
                        ],
                        no=[Playthroughs.ToggleAutosaveOnChoicesOnActive()]
                    )
                    return

                renpy.save(nextSlot) # If this becomes laggy, check the ren'py's autosave system and its threading

                self.incrementActiveSlot()

        class IncrementActiveSlot():
            def __call__(self):
                Autosaver.incrementActiveSlot()

        class HandlePress(renpy.ui.Action):
            def __call__(self):
                Autosaver.handlePress()

        class Save():
            def __init__(self, nextSlot):
                self.nextSlot = nextSlot

            def __call__(self):
                renpy.save(self.nextSlot) # If this becomes laggy, check the ren'py's autosave system and its threading
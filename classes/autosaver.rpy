init -999 python in SSSSS:
    _constant = True

    class AutosaverClass():
        slotsPerPage = 6
        suppressAutosaveConfirm = False

        def setActiveSlot(self, slot):
            self.suppressAutosaveConfirm = False

            AutosaverCounter.setActiveSlot(slot)

        class HandlePress(renpy.ui.Action):
            def __init__(self, slotsPerPage):
                self.isDisplayingChoice = Choices.isDisplayingChoice
                self.slotsPerPage = slotsPerPage

            def __call__(self):
                if(self.isDisplayingChoice and Playthroughs.activePlaythrough.autosaveOnChoices):
                    #TODO: Don't take a screenshot if screenshots are disabled for the playthrough
                    renpy.exports.take_screenshot() # Must take a screenshot before anything else happens just in case the yesno_screen appears or something that might screw up the shot

                    _, _, slotString = AutosaverCounter.getNextSlot(self.slotsPerPage)
                    nextSlot = slotString
                    print(nextSlot)

                    # If the save slot is not bigger than the very last one, do once a confirm whether to disable autosaving
                    if renpy.scan_saved_game(nextSlot) and not Autosaver.suppressAutosaveConfirm:
                        renpy.display.layout.yesno_screen(
                            _("Are you sure you want to overwrite your save?"),
                            [
                                FileSave(nextSlot, False, False, page, cycle=False, slot=slot),
                                AutosaveCounter.IncrementActiveSlot(self.slotsPerPage)
                            ],
                            Playthroughs.ToggleAutosaveOnChoicesOnActive()
                        )
                        return

                    renpy.save(nextSlot) # If this becomes laggy, check the ren'py's autosave system and its threading

                    AutosaverCounter.incrementActiveSlot(self.slotsPerPage)

    class AutosaveCounterClass():
        def __init__(self):
            self.activeSlot = "1-1"

        def setActiveSlot(self, slot):
            self.activeSlot = slot

        def getNextSlot(self, slotsPerPage):
            page, slot = self.activeSlot.split('-')
            page = int(page)
            slot = int(slot)

            slot += 1

            if(slot > slotsPerPage):
                slot = 1
                page += 1

            slotString = str(page) + "-" + str(slot)

            return page, slot, slotString

        def incrementActiveSlot(self, slotsPerPage):
            _, _, slotString = self.getNextSlot(slotsPerPage)

            self.activeSlot = slotString

        class IncrementActiveSlot():
            def __init__(self, slotsPerPage):
                self.slotsPerPage = slotsPerPage

            def __call__(self):
                SSSSS.AutosaveCounter.incrementActiveSlot(self.slotsPerPage)
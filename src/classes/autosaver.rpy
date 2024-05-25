# Unfortunately this must be saved into the save game, so the system can properly recognize which slot to use next,
# especially when a manual save is made somewhere in between and then a rollback occurs.
default SSSSS_ActiveSlot = "1-1"

init -999 python in SSSSS:
    _constant = True

    import time
    from json import dumps as json_dumps
    import io
    import sys
    import re

    class AutosaverClass(x52NonPicklable):
        def __init__(self):
            self.suppressAutosaveConfirm = False
            self.pendingSave = None
            self.prevActiveSlot = "N/A"
            self.confirmDialogOpened = False
            self.afterLoadSavePositionPending = False
            self.lastChoice = None
            self.activeSlotPending = None

        @property
        def slotsPerPage(self):
            return renpy.store.gui.file_slot_cols * renpy.store.gui.file_slot_rows

        def setActiveSlot(self, slot):
            self.prevActiveSlot = renpy.store.SSSSS_ActiveSlot + "" # Copy the data, not just the pointer
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

        def getCurrentSlot(self):
            slotString = renpy.store.SSSSS_ActiveSlot
            page, slot = slotString.split('-')
            page = int(page)
            slot = int(slot)

            return page, slot, slotString

        def getPreviousSlot(self):
            page, slot = renpy.store.SSSSS_ActiveSlot.split('-')
            page = int(page)
            slot = int(slot)

            slot -= 1

            if(slot < 1):
                slot = 1
                page -= 1

            slotString = str(page) + "-" + str(slot)

            return page, slot, slotString

        def setNextSlot(self):
            _, _, slotString = Autosaver.getNextSlot()
            self.setActiveSlot(slotString)

        def setPreviousSlot(self):
            _, _, slotString = Autosaver.getPreviousSlot()
            self.setActiveSlot(slotString)

        def trySavePendingSave(self):
            if(self.pendingSave != None):
                # If the save slot is not bigger than the very last one, do once a confirm whether to disable autosaving
                if renpy.scan_saved_game(renpy.store.SSSSS_ActiveSlot) and not self.suppressAutosaveConfirm and not renpy.store.SSSSS_ActiveSlot == self.prevActiveSlot:
                    self.confirmDialogOpened = True
                    renpy.show_screen("SSSSS_AutosaveOverwriteConfirm")
                    return

                self.pendingSave.save()

        def handleChoiceSelection(self, choice):
            # Prevent making any autosave actions when viewing a memory or a replay
            if Memories.memoryInProgress or renpy.store._in_replay:
                return

            # Processes the label as Ren'Py would to remove any possible substitutions via [...] e.g. [player_name]
            textComponent = renpy.ui.text(choice.label)
            choiceText = ' '.join(textComponent.text)# .replace("[", "⟦").replace("]", "⟧") #FFS: Prepared in case [] needs to be substitued. In built games it's not a problem, but if there ever is game with these and config.developer = True, it might be a problem

            Autosaver.lastChoice = choiceText

            if(Playthroughs.activePlaythrough.autosaveOnChoices):
                self.createPendingSave(choiceText)
                self.pendingSave.takeAndSaveScreenshot()
                self.trySavePendingSave()

        # The SSSSS_ActiveSlot always equals the slot that was loaded because the saves are made right before selecting a choice for easy re-choicing.
        # However when a manual save is loaded it might not be a choice screen.
        # If so, the save slot needs to move further as to not override the manual slot with the next autosave.
        def processSlotAfterLoad(self):
            if(not Choices.isDisplayingChoice):
                self.setNextSlot()

            self.afterLoadSavePositionPending = False

        class ConfirmDialogSave(renpy.ui.Action):
            def __call__(self):
                Autosaver.suppressAutosaveConfirm = True

                if(Autosaver.pendingSave != None):
                    Autosaver.pendingSave.save()

        class ConfirmDialogClose(renpy.ui.Action):
            def __call__(self):
                Autosaver.confirmDialogOpened = False

        class MoveOneSlotOver(renpy.ui.Action):
            def __call__(self):
                Autosaver.setNextSlot()

        class TrySavePendingSave(renpy.ui.Action):
            def __call__(self):
                Autosaver.trySavePendingSave()
                renpy.restart_interaction()

        def createPendingSave(self, choice):
            self.pendingSave = AutosaverClass.PendingSaveClass(choice)

        class PendingSaveClass(x52NonPicklable):
            def __init__(self, choice):
                self.saveRecord = None
                self.choice = choice

                self.createSaveSnapshot()

            def createSaveSnapshot(self, extra_info=None):
                if(Playthroughs.activePlaythrough.useChoiceLabelAsSaveName):
                    extra_info = extra_info or self.choice

                self.saveRecord = Utils.createSaveRecord(extra_info)
                self.saveRecord.choice = self.choice

            def takeAndSaveScreenshot(self):
                renpy.take_screenshot()

                self.saveRecord.screenshot = renpy.game.interface.get_screenshot()

            # If this becomes laggy, check the ren'py's autosave system and its threading
            def save(self):
                slotname = renpy.store.SSSSS_ActiveSlot

                renpy.loadsave.location.save(slotname, self.saveRecord)
                renpy.loadsave.location.scan()
                renpy.loadsave.clear_slot(slotname)

                Autosaver.pendingSave = None

                page, _, _ = Autosaver.getCurrentSlot()
                page = int(page)

                renpy.store.persistent._file_page = page

                Autosaver.setNextSlot()
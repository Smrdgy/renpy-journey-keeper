# Unfortunately this must be saved into the save game, so the system can properly recognize which slot to use next,
# especially when a manual save is made somewhere in between and then a rollback occurs.
default JK_ActiveSlot = "1-1"

init python in JK:
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
            self.prevent_autosaving = Settings.preventAutosavingWhileNotInGame
            self.loaded_manual_save_without_choices = False

        @property
        def slotsPerPage(self):
            return Utils.getSlotsPerPage()

        def setActiveSlot(self, slotname):
            page, slot = Utils.split_slotname(slotname)

            #Last resort check to counter forced autosaves screwing up the counter (e.g. $ renpy.save("auto-1") somewhere in the dialog)
            if page != 0 and slot != 0:
                self.prevActiveSlot = renpy.store.JK_ActiveSlot + "" # Copy the data, not just the pointer
                renpy.store.JK_ActiveSlot = slotname

        def getNextSlot(self):
            page, slot = Utils.split_slotname(renpy.store.JK_ActiveSlot)

            slot += 1

            if(slot > self.slotsPerPage):
                slot = 1
                page += 1

            slotString = str(page) + "-" + str(slot)

            return page, slot, slotString

        def getCurrentSlot(self):
            slotString = renpy.store.JK_ActiveSlot
            page, slot = Utils.split_slotname(slotString)

            return page, slot, slotString

        def getPreviousSlot(self):
            page, slot = Utils.split_slotname(renpy.store.JK_ActiveSlot)

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
                if renpy.scan_saved_game(Utils.format_slotname(renpy.store.JK_ActiveSlot)) and not self.suppressAutosaveConfirm and (self.loaded_manual_save_without_choices or renpy.store.JK_ActiveSlot != self.prevActiveSlot):
                    self.confirmDialogOpened = True
                    renpy.show_screen("JK_AutosaveOverwriteConfirm")
                    return

                self.pendingSave.save()

        def handleChoiceSelection(self, choice):
            # Prevent making any autosave actions when viewing a memory or a replay
            if Memories.memoryInProgress or renpy.store._in_replay:
                return

            # Processes the label as Ren'Py would to remove any possible substitutions via [...] e.g. [player_name]
            textComponent = renpy.ui.text(choice.label)
            choiceText = Utils.replaceReservedCharacters(' '.join(textComponent.text))

            if Playthroughs.activePlaythrough.autosaveOnChoices:
                self.createPendingSave(choiceText)

        # The JK_ActiveSlot always equals the slot that was loaded because the saves are made right before selecting a choice for easy re-choicing.
        # However when a manual save is loaded it might not be a choice screen.
        # If so, the save slot needs to move further as to not override the manual slot with the next autosave.
        def processSlotAfterLoad(self):
            self.loaded_manual_save_without_choices = False

            if not Utils.isDisplayingChoices():
                if Settings.offsetSlotAfterManualSaveIsLoaded:
                    self.setNextSlot()

                self.loaded_manual_save_without_choices = True

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
            self.trySavePendingSave()

        class PendingSaveClass(x52NonPicklable):
            temp_save_slotname = "JK-temp"

            def __init__(self, choice):
                self.choice = choice

                self.early_save()

            def early_save(self):
                extra_info = ''
                if Playthroughs.activePlaythrough.useChoiceLabelAsSaveName:
                    extra_info = self.choice

                renpy.take_screenshot()
                renpy.save(self.temp_save_slotname, extra_info)

            def save(self):
                slotname = Utils.format_slotname(renpy.store.JK_ActiveSlot)

                renpy.rename_save(self.temp_save_slotname, slotname)

                if Settings.autosaveNotificationEnabled:
                    renpy.notify("Autosave created at {}".format(slotname))

                Autosaver.pendingSave = None
                Autosaver.loaded_manual_save_without_choices = False

                if Settings.pageFollowsAutoSave:
                    page, _, _ = Autosaver.getCurrentSlot()
                    renpy.store.persistent._file_page = str(page)

                Autosaver.setNextSlot()
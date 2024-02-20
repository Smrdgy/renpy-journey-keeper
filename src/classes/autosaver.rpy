# Unfortunately this must be saved into the save game, so the system can properly recognize which slot to use next,
# especially when a manual save is made somewhere in between and then a rollback occurs.
default SSSSS_ActiveSlot = "1-1"

init -999 python in SSSSS:
    import time
    from json import dumps as json_dumps
    import io
    import sys

    if(sys.version_info[0] > 2):
        from future.utils import reraise

    _constant = True

    class AutosaverClass():
        suppressAutosaveConfirm = False
        pendingSave = None
        prevActiveSlot = "1-1"
        confirmDialogOpened = False
        afterLoadSavePositionPending = False

        @property
        def slotsPerPage(self):
            return renpy.store.gui.file_slot_cols * renpy.store.gui.file_slot_rows

        def setActiveSlot(self, slot):
            self.suppressAutosaveConfirm = False

            renpy.store.SSSSS_ActiveSlot = slot
            self.prevActiveSlot = slot

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

        def handlePress(self):
            if(self.pendingSave != None):
                self.pendingSave.takeAndSaveScreenshot()
                self.pendingSave.makeReady()

        def trySavePendingSave(self):
            if(renpy.store.SSSSS_ActiveSlot == Autosaver.prevActiveSlot):
                Autosaver.pendingSave = None # Discard this save because the user has rolled back

            if(self.pendingSave != None):
                # If the save slot is not bigger than the very last one, do once a confirm whether to disable autosaving
                if renpy.scan_saved_game(renpy.store.SSSSS_ActiveSlot) and not self.suppressAutosaveConfirm:
                    self.confirmDialogOpened = True
                    renpy.show_screen("SSSSS_AutosaveOverwriteConfirm")
                    return

                self.pendingSave.save()

        # The SSSSS_ActiveSlot always equals the slot that was loaded because the saves are made right before selecting a choice for easy re-choicing.
        # However when a manual save is loaded it might not be a choice screen.
        # If so, the save slot needs to move further as to not override the manual slot with the next autosave.
        def processSlotAfterLoad(self):
            if(not Choices.isDisplayingChoice):
                _, _, slotString = self.getNextSlot()
                renpy.store.SSSSS_ActiveSlot = slotString

            self.afterLoadSavePositionPending = False

        class HandlePress(renpy.ui.Action):
            def __call__(self):
                Autosaver.handlePress()

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
                _, _, slotName = Autosaver.getNextSlot()

                renpy.store.SSSSS_ActiveSlot = slotName

        class TrySavePendingSave(renpy.ui.Action):
            def __call__(self):
                Autosaver.trySavePendingSave()
                renpy.restart_interaction()

        def registerChoices(self):
            self.prevActiveSlot = renpy.store.SSSSS_ActiveSlot

            _, _, slotString = self.getNextSlot()
            renpy.store.SSSSS_ActiveSlot = slotString

            self.pendingSave = AutosaverClass.PendingSaveClass()

        class PendingSaveClass():
            isReady = False
            choices = None
            saveRecord = None

            def __init__(self):
                self.choices = Choices.currentChoices

                self.createSaveSnapshot()

            def createSaveSnapshot(self, extra_info=""):
                roots = renpy.game.log.freeze(None)

                if renpy.config.save_dump:
                    renpy.loadsave.save_dump(roots, renpy.game.log)

                logf = io.BytesIO()

                if(sys.version_info[0] == 2):
                    try:
                        renpy.loadsave.dump((roots, renpy.game.log), logf)
                    except:

                        t, e, tb = sys.exc_info()

                        try:
                            bad = renpy.loadsave.find_bad_reduction(roots, renpy.game.log)
                        except:
                            raise t, e, tb

                        if bad is None:
                            raise t, e, tb

                        e.args = ( e.args[0] + ' (perhaps {})'.format(bad), ) + e.args[1:]
                        raise t, e, tb
                else:
                    try:
                        renpy.loadsave.dump((roots, renpy.game.log), logf)
                    except Exception:
                        t, e, tb = sys.exc_info()

                        try:
                            bad = renpy.loaadsave.find_bad_reduction(roots, renpy.game.log)
                        except Exception:
                            reraise(t, e, tb)

                        if bad is None:
                            reraise(t, e, tb)

                        if e.args:
                            e.args = (e.args[0] + ' (perhaps {})'.format(bad),) + e.args[1:]

                        reraise(t, e, tb)

                json = { "_save_name" : extra_info, "_renpy_version" : list(renpy.version_tuple), "_version" : renpy.config.version }

                for i in renpy.config.save_json_callbacks:
                    i(json)

                json = json_dumps(json)

                self.saveRecord = renpy.loadsave.SaveRecord(None, extra_info, json, logf.getvalue())

            def takeAndSaveScreenshot(self):
                renpy.take_screenshot()

                self.saveRecord.screenshot = renpy.game.interface.get_screenshot()

            def makeReady(self):
                self.isReady = True

            # If this becomes laggy, check the ren'py's autosave system and its threading
            def save(self):
                slotname = renpy.store.SSSSS_ActiveSlot

                renpy.loadsave.location.save(slotname, self.saveRecord)
                renpy.loadsave.location.scan()
                renpy.loadsave.clear_slot(slotname)

                Autosaver.pendingSave = None

                page, slot = renpy.store.SSSSS_ActiveSlot.split('-')
                page = int(page)

                renpy.store.persistent._file_page = page
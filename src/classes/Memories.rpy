init python in JK:
    _constant = True

    import time

    class MemoriesClass(x52NonPicklable):
        def __init__(self):
            self.memoryInProgress = False

            self.restoreOldLog = None
            self.restoreStoreBackup = None
            self.restoreContext = None

        @property
        def saveInstance(self):
            return SaveSystem.getPlaythroughSaveInstance(2)

        def createAutomaticMemory(self):
            pass

        def getMemories(self):
            saveInstance = self.saveInstance
            saveInstance.location.activateLocations()
            saveInstance.location.scan()
            memories = saveInstance.location.list()
            saveInstance.location.deactivateLocations()
            return memories

        def callCustomReplay(self, slotname):
            self.saveInstance.location.activateLocations()

            # Backup current session
            # TODO: Figure out session restoration #### UPDATE ##### -- maybe I've fixed it with context_clear_layers in main.rpy, but have to check this out later in the future...

            # renpy.game.log.complete()

            # self.restoreOldLog = renpy.game.log
            # renpy.game.log = renpy.python.RollbackLog()

            # self.restoreStoreBackup = renpy.python.StoreBackup()
            # renpy.python.clean_stores()

            self.restoreContext = renpy.execution.Context(True)
            renpy.game.contexts.append(self.restoreContext) # This is currently used only to prevent native autosaving

            # # This has to be here, to ensure the scope stuff works.
            # renpy.exports.execute_default_statement()

            ##############################################

            Memories.memoryInProgress = True

            roots, log = renpy.loadsave.loads(self.saveInstance.location.load(slotname))
            log.unfreeze(roots)

            # renpy.execution.run_context(False)

            self.saveInstance.location.deactivateLocations()

            # renpy.store._in_replay = True

        def exitMemoryAndTryRestoryOldGame(self):
            # Restore previous session

            if self.restoreContext != None: # This is currently used only to prevent native autosaving
                self.restoreContext.pop_all_dynamic()

                renpy.game.contexts.pop()
            
            # if self.restoreOldLog != None:
            #     renpy.game.log = self.restoreOldLog
            
            # if self.restoreStoreBackup != None:
            #     self.restoreStoreBackup.restore()

            # interface = renpy.display.core.Interface()

            # if interface and interface.restart_interaction and renpy.game.contexts:
            #     renpy.game.contexts[-1].scene_lists.focused = None

            # renpy.config.skipping = None

            # if renpy.config.after_replay_callback:
            #     renpy.config.after_replay_callback()

            #############################################

            self.memoryInProgress = False
            self.restoreOldLog = None
            self.restoreStoreBackup = None
            self.restoreContext = None

        @staticmethod
        def createSaveRecord(extra_info=None, log=None):
            log = log or renpy.game.log
            roots = log.freeze(None)

            extra_info = extra_info or ""

            if renpy.config.save_dump:
                renpy.loadsave.save_dump(roots, log)

            logf = io.BytesIO()

            try:
                renpy.loadsave.dump((roots, log), logf)
            except:
                t, e, tb = sys.exc_info()

                try:
                    bad = renpy.loadsave.find_bad_reduction(roots, log)
                except:
                    print("Memory save failure:\n", t, e, tb)
                    renpy.notify("Memory save failed. Check log.txt for more info.")
                    return

                if bad is None:
                    print("Memory save failure:\n", t, e, tb)
                    renpy.notify("Memory save failed. Check log.txt for more info.")
                    return

                if e.args:
                    e.args = (e.args[0] + ' (perhaps {})'.format(bad),) + e.args[1:]

                print("Memory save failure:\n", t, e, tb)
                renpy.notify("Memory save failed. Check log.txt for more info.")
                return

            json = { "_save_name" : extra_info, "_renpy_version" : list(renpy.version_tuple), "_version" : renpy.config.version }

            for i in renpy.config.save_json_callbacks:
                i(json)

            json = json_dumps(json)

            save_record = renpy.loadsave.SaveRecord(None, extra_info, json, logf.getvalue())
            save_record.screenshot = renpy.game.interface.get_screenshot()

            return save_record

        class OpenSaveMemory(renpy.ui.Action):
            def __call__(self):
                renpy.take_screenshot()
                renpy.show_screen("JK_SaveMemory")
                renpy.restart_interaction()

        class CreateMemory(renpy.ui.Action):
            def __init__(self, name):
                self.name = name

            def __call__(self):
                saveInstance = Memories.saveInstance
                saveRecord = MemoriesClass.createSaveRecord(extra_info=self.name)

                for location in saveInstance.location.locations:
                    location.save(str(time.time())[:-3], saveRecord)

                saveInstance.location.scan()
                
                renpy.restart_interaction()

        class LoadMemoryWithConfirm(renpy.ui.Action):
            def __init__(self, slotname):
                self.slotname = slotname

            def __call__(self):
                if renpy.context()._main_menu:
                    Memories.callCustomReplay(self.slotname)
                else:
                    showConfirm(
                        title="Load memory",
                        message="Viewing a memory will quit your current session and your current progress will be lost.\nProceed?",
                        yes=Memories.LoadMemory(self.slotname),
                    )

                renpy.restart_interaction()

        class LoadMemory(renpy.ui.Action):
            def __init__(self, slotname):
                self.slotname = slotname

            def __call__(self):
                Memories.callCustomReplay(self.slotname)

                renpy.restart_interaction()

        class ExitMemory(renpy.ui.Action):
            def __call__(self):
                Memories.exitMemoryAndTryRestoryOldGame()
                
                renpy.restart_interaction()

        def GetScreenshot(self, slotname):
            saveInstance = Memories.saveInstance

            for location in saveInstance.location.locations:
                screenshot = location.screenshot(slotname)
                break

            if screenshot is not None:
                return screenshot

            return ImagePlaceholder(width=renpy.config.thumbnail_width, height=renpy.config.thumbnail_height)

        class DeleteMemory(renpy.ui.Action):
            def __init__(self, slotname):
                self.slotname = slotname

            def __call__(self):
                Memories.saveInstance.location.unlink_save(self.slotname)
                renpy.restart_interaction()

        class DeleteMemoryConfirm(renpy.ui.Action):
            def __init__(self, slotname):
                self.slotname = slotname

            def __call__(self):
                name = Memories.saveInstance.location.save_name(self.slotname) or self.slotname

                showConfirm(
                    title="Delete memory \"{}\"".format(name),
                    message="This action {u}{color=[JK.Colors.error]}is irreversible{/c}{/u}. Do you wish to proceed?",
                    yes=Memories.DeleteMemory(self.slotname),
                    yesIcon="\ue92b",
                    yesColor=Colors.error
                )
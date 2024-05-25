init 1 python in SSSSS:
    _constant = True

    class MemoriesClass():
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

        def callCustomReplay(self, savename):
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

            roots, log = renpy.loadsave.loads(self.saveInstance.location.load(savename))
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

        class OpenSaveMemory(renpy.ui.Action):
            def __call__(self):
                renpy.take_screenshot()
                renpy.show_screen("SSSSS_SaveMemory")
                renpy.restart_interaction()

        class CreateMemory(renpy.ui.Action):
            def __init__(self, name):
                self.name = name

            def __call__(self):
                name = self.name if not callable(self.name) else self.name()

                saveInstance = Memories.saveInstance
                saveRecord = Utils.createSaveRecord()
                saveRecord.screenshot = renpy.game.interface.get_screenshot()
                
                for location in saveInstance.location.locations:
                    location.save(name, saveRecord)

                saveInstance.location.scan()
                
                renpy.restart_interaction()

        class LoadMemoryWithConfirm(renpy.ui.Action):
            def __init__(self, savename):
                self.savename = savename

            def __call__(self):
                if renpy.context()._main_menu:
                    Memories.callCustomReplay(self.savename)
                else:
                    showConfirm(
                        title="Load memory",
                        message="Viewing a memory will quit your current session and your current progress will be lost.\nProceed?",
                        yes=Memories.LoadMemory(self.savename),
                    )

                renpy.restart_interaction()

        class LoadMemory(renpy.ui.Action):
            def __init__(self, savename):
                self.savename = savename

            def __call__(self):
                Memories.callCustomReplay(self.savename)

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
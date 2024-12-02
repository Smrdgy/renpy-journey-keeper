init -1000 python in SSSSS:
    _constant = True

    import os
    import json
    import __main__
    import io

    # Main Settings class
    class SettingsClass(x52NonPicklable):
        def __init__(self):
            settings = self.loadFromUserDir()
            settings.update(self.loadFromPersistent())

            self.setSettings(settings)

        def loadFromUserDir(self):
            return UserDir.loadSettings()

        def loadFromPersistent(self):
            if renpy.store.persistent.SSSSS_Settings:
                data = json.loads(renpy.store.persistent.SSSSS_Settings)
            else:
                data = {}

            return data

        def setSettings(self, data):
            self.autosaveNotificationEnabled = data.get("autosaveNotificationEnabled", False)
            self.autosaveKey = data.get("autosaveKey", "alt_K_a")
            self.quickSaveEnabled = data.get("quickSaveEnabled", True)
            self.quickSaveNotificationEnabled = data.get("quickSaveNotificationEnabled", True)
            self.quickSaveKey = data.get("quickSaveKey", "K_F5")
            self.memoriesEnabled = data.get("memoriesEnabled", True)
            self.memoriesKey = data.get("memoriesKey", "K_BACKQUOTE")
            self.customGridEnabled = data.get("customGridEnabled", False)
            self.customGridX = data.get("customGridX", 2)
            self.customGridY = data.get("customGridY", 2)
            self.loadScreenName = data.get("loadScreenName", "load")
            self.saveScreenName = data.get("saveScreenName", "save")
            self.offsetSlotAfterManualSaveIsLoaded = data.get("offsetSlotAfterManualSaveIsLoaded", True)#TODO: Implement
            self.sizeAdjustment = data.get("sizeAdjustment", 0)
            self.changeSidepanelVisibilityKey = data.get("changeSidepanelVisibilityKey", "alt_K_p")
            self.debugEnabled = data.get("debugEnabled", False)
            self.pageFollowsQuickSave = data.get("pageFollowsQuickSave", True)
            self.pageFollowsAutoSave = data.get("pageFollowsAutoSave", True)

        def getSettingsAsJson(self):
            return json.dumps({
                'autosaveNotificationEnabled': self.autosaveNotificationEnabled,
                'autosaveKey': self.autosaveKey,
                'quickSaveEnabled': self.quickSaveEnabled,
                'quickSaveNotificationEnabled': self.quickSaveNotificationEnabled,
                'quickSaveKey': self.quickSaveKey,
                'memoriesEnabled': self.memoriesEnabled,
                'memoriesKey': self.memoriesKey,
                'customGridEnabled': self.customGridEnabled,
                'customGridX': self.customGridX,
                'customGridY': self.customGridY,
                'loadScreenName': self.loadScreenName,
                'saveScreenName': self.saveScreenName,
                'offsetSlotAfterManualSaveIsLoaded': self.offsetSlotAfterManualSaveIsLoaded,
                'sizeAdjustment': self.sizeAdjustment,
                'changeSidepanelVisibilityKey': self.changeSidepanelVisibilityKey,
                'debugEnabled': self.debugEnabled,
                'pageFollowsQuickSave': self.pageFollowsQuickSave,
                'pageFollowsAutoSave': self.pageFollowsAutoSave,
            })

        def save(self):
            self.saveToUserDir()
            self.saveToPersistent()

        def saveToUserDir(self):
            UserDir.saveSettings(self.getSettingsAsJson())

        def saveToPersistent(self):
            renpy.store.persistent.SSSSS_Settings = self.getSettingsAsJson()

            renpy.save_persistent()

        def reset(self):
            renpy.store.persistent.SSSSS_Settings = None
            UserDir.removeSettings()
            self.loadFromPersistent()

            renpy.save_persistent()

        class Reset(renpy.ui.Action):
            def __call__(self):
                Settings.reset()
                renpy.restart_interaction()

        class SetAutosaveToggleKey(SetKey):
            def __call__(self):
                Settings.autosaveKey = self.resolveKey()

                Settings.save()
                renpy.restart_interaction()

        class ToggleAutosaveNotificationEnabled(renpy.ui.Action):
            def __call__(self):
                Settings.autosaveNotificationEnabled = not Settings.autosaveNotificationEnabled
                Settings.save()
                renpy.restart_interaction()

        class ToggleQuickSaveEnabled(renpy.ui.Action):
            def __call__(self):
                Settings.quickSaveEnabled = not Settings.quickSaveEnabled
                Settings.save()
                renpy.restart_interaction()

        class ToggleQuickSaveNotificationEnabled(renpy.ui.Action):
            def __call__(self):
                Settings.quickSaveNotificationEnabled = not Settings.quickSaveNotificationEnabled
                Settings.save()
                renpy.restart_interaction()

        class SetQuickSaveKey(SetKey):
            def __call__(self):
                Settings.quickSaveKey = self.resolveKey()

                Settings.save()
                renpy.restart_interaction()

        class ToggleMemoriesEnabled(renpy.ui.Action):
            def __call__(self):
                Settings.memoriesEnabled = not Settings.memoriesEnabled
                Settings.save()
                renpy.restart_interaction()

        class SetCreateMemoryKey(SetKey):
            def __call__(self):
                Settings.memoriesKey = self.resolveKey()

                Settings.save()
                renpy.restart_interaction()

        class ToggleCustomGridEnabled(renpy.ui.Action):
            def __call__(self):
                Settings.customGridEnabled = not Settings.customGridEnabled
                Settings.save()
                renpy.restart_interaction()

        class DecrementCustomGridX(renpy.ui.Action):
            def __call__(self):
                Settings.customGridX = max(Settings.customGridX - 1, 1)
                Settings.save()
                renpy.restart_interaction()
        
        class IncrementCustomGridX(renpy.ui.Action):
            def __call__(self):
                Settings.customGridX = Settings.customGridX + 1
                Settings.save()
                renpy.restart_interaction()
        
        class DecrementCustomGridY(renpy.ui.Action):
            def __call__(self):
                Settings.customGridY = max(Settings.customGridY - 1, 1)
                Settings.save()
                renpy.restart_interaction()
        
        class IncrementCustomGridY(renpy.ui.Action):
            def __call__(self):
                Settings.customGridY = Settings.customGridY + 1
                Settings.save()
                renpy.restart_interaction()

        class SetSaveScreenName(renpy.ui.Action):
            def __init__(self, name):
                self.name = name

            def __call__(self):
                Settings.saveScreenName = self.name
                Settings.save()
                renpy.restart_interaction()

        class SetLoadScreenName(renpy.ui.Action):
            def __init__(self, name):
                self.name = name

            def __call__(self):
                Settings.loadScreenName = self.name
                Settings.save()
                renpy.restart_interaction()

        class IncrementSizeAdjustment(renpy.ui.Action):
            def __call__(self):
                Settings.sizeAdjustment = min(Settings.sizeAdjustment + 1, 100)
                Settings.save()
                renpy.restart_interaction()
        
        class DecrementSizeAdjustment(renpy.ui.Action):
            def __call__(self):
                Settings.sizeAdjustment = max(Settings.sizeAdjustment - 1, -100)
                Settings.save()
                renpy.restart_interaction()

        class ResetSizeAdjustment(renpy.ui.Action):
            def __call__(self):
                Settings.sizeAdjustment = 0
                #Also reset sidepanel and pagination positions just in case there are positioned somewhere outside of the screen
                renpy.store.persistent.SSSSS_sidepanelPos = None
                renpy.store.persistent.SSSSS_PaginationPos = None
                Settings.save()
                renpy.restart_interaction()

        class SetChangeSidepanelVisibilityKey(SetKey):
            def __call__(self):
                Settings.changeSidepanelVisibilityKey = self.resolveKey()

                Settings.save()
                renpy.restart_interaction()

        class ToggleDebugEnabled(renpy.ui.Action):
            def __call__(self):
                Settings.debugEnabled = not Settings.debugEnabled

                Settings.save()
                renpy.restart_interaction()

        class TogglePageFollowsQuickSaveEnabled(renpy.ui.Action):
            def __call__(self):
                Settings.pageFollowsQuickSave = not Settings.pageFollowsQuickSave

                Settings.save()
                renpy.restart_interaction()

        class TogglePageFollowsAutoSaveEnabled(renpy.ui.Action):
            def __call__(self):
                Settings.pageFollowsAutoSave = not Settings.pageFollowsAutoSave

                Settings.save()
                renpy.restart_interaction()
                
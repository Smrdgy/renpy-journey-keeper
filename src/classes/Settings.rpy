init -1 python in JK:
    _constant = True

    import os
    import json
    import __main__
    import io

    # Main Settings class
    class SettingsClass(x52NonPicklable):
        def __init__(self):
            global_settings = self.loadFromGlobalSettings()

            settings = {}
            settings.update(global_settings)
            settings.update(self.loadFromUserDir())
            settings.update(self.loadFromPersistent())

            # Apply globalized settings again in case some local setting is overwriting it
            for setting in settings.get("globalizedSettings", []):
                if global_settings.get(setting):
                    settings[setting] = global_settings.get(setting)

            self.setSettings(settings)

        def loadFromUserDir(self):
            return UserDir.loadSettings()

        def loadFromGlobalSettings(self):
            return UserDir.loadGlobalSettings()

        def loadFromPersistent(self):
            if renpy.store.persistent.JK_Settings:
                data = json.loads(renpy.store.persistent.JK_Settings)
            else:
                data = {}

            return data

        def setSettings(self, data):
            self.autosaveNotificationEnabled = data.get("autosaveNotificationEnabled", False)
            self.autosaveKey = data.get("autosaveKey", "alt_K_a")
            self.quickSaveEnabled = data.get("quickSaveEnabled", True)
            self.quickSaveNotificationEnabled = data.get("quickSaveNotificationEnabled", True)
            self.quickSaveKey = data.get("quickSaveKey", "K_F5")
            self.memoriesEnabled = data.get("memoriesEnabled", False)
            self.memoriesKey = data.get("memoriesKey", "K_BACKQUOTE")
            self.customGridEnabled = data.get("customGridEnabled", False)
            self.customGridX = data.get("customGridX", 2)
            self.customGridY = data.get("customGridY", 2)
            self.loadScreenName = data.get("loadScreenName", ["load"])
            self.saveScreenName = data.get("saveScreenName", ["save"])
            self.offsetSlotAfterManualSaveIsLoaded = data.get("offsetSlotAfterManualSaveIsLoaded", False)
            self.offsetSlotAfterManualSave = data.get("offsetSlotAfterManualSave", True)
            self.sizeAdjustment = data.get("sizeAdjustment", 0) or 0
            self.changeSidepanelVisibilityKey = data.get("changeSidepanelVisibilityKey", "alt_K_p")
            self.debugEnabled = data.get("debugEnabled", False)
            self.pageFollowsQuickSave = data.get("pageFollowsQuickSave", True)
            self.pageFollowsAutoSave = data.get("pageFollowsAutoSave", True)
            self.updaterEnabled = data.get("updaterEnabled", True)
            self.autoUpdateWithoutPrompt = data.get("autoUpdateWithoutPrompt", False)
            self.globalizedSettings = data.get("globalizedSettings", [])
            self.autosaveOnSingletonChoice = data.get("autosaveOnSingletonChoice", True)
            self.playthroughTemplate = data.get("playthroughTemplate", None)
            self.preventAutosavingWhileNotInGame = data.get("preventAutosavingWhileNotInGame", True)
            self.seamlessPagination = data.get("seamlessPagination", False)
            self.autosaveOnQuestion = data.get("autosaveOnQuestion", True)
            self.sidepanelHorizontal = data.get("sidepanelHorizontal", False)
            self.searchPlaythroughKey = data.get("searchPlaythroughKey", "ctrl_K_f")
            self.searchPlaythroughsKey = data.get("searchPlaythroughsKey", "ctrl_shift_K_f")
            self.showConfirmOnLargePageJump = data.get("showConfirmOnLargePageJump", True)

            # Update the old system (string only) to list #TODO: Remove at some point
            if not hasattr(self.loadScreenName, "append"):
                self.loadScreenName = ["load"]

            if not hasattr(self.saveScreenName, "append"):
                self.saveScreenName = ["save"]

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
                'offsetSlotAfterManualSave': self.offsetSlotAfterManualSave,
                'sizeAdjustment': self.sizeAdjustment,
                'changeSidepanelVisibilityKey': self.changeSidepanelVisibilityKey,
                'debugEnabled': self.debugEnabled,
                'pageFollowsQuickSave': self.pageFollowsQuickSave,
                'pageFollowsAutoSave': self.pageFollowsAutoSave,
                'autosaveOnSingletonChoice': self.autosaveOnSingletonChoice,
                'playthroughTemplate': self.playthroughTemplate,
                'preventAutosavingWhileNotInGame': self.preventAutosavingWhileNotInGame,
                'seamlessPagination': self.seamlessPagination,
                'autosaveOnQuestion': self.autosaveOnQuestion,
                'sidepanelHorizontal': self.sidepanelHorizontal,
                'searchPlaythroughKey': self.searchPlaythroughKey,
                'searchPlaythroughsKey': self.searchPlaythroughsKey,
                'showConfirmOnLargePageJump': self.showConfirmOnLargePageJump,
            })

        def getSettingsForReset(self, no_globals=False):
            if no_globals:
                return {}

            new_settings = {
                'updaterEnabled': self.updaterEnabled,
                'autoUpdateWithoutPrompt': self.autoUpdateWithoutPrompt,
                'globalizedSettings': self.globalizedSettings,
            }

            for setting_name in self.globalizedSettings:
                if hasattr(self, setting_name):
                    new_settings[setting_name] = getattr(self, setting_name)

            return new_settings

        def getGlobalSettingsAsJson(self):
            settings = {
                'updaterEnabled': self.updaterEnabled,
                'autoUpdateWithoutPrompt': self.autoUpdateWithoutPrompt,
                'globalizedSettings': self.globalizedSettings,
            }

            for setting_name in self.globalizedSettings:
                if hasattr(self, setting_name):
                    settings[setting_name] = getattr(self, setting_name)
                else:
                    print("Setting not found {}".format(setting_name))

            return json.dumps(settings)

        def save(self):
            self.saveToUserDir()
            self.saveToGlobals()
            self.saveToPersistent()

        def saveToUserDir(self):
            UserDir.saveSettings(self.getSettingsAsJson())

        def saveToGlobals(self):
            UserDir.saveGlobalSettings(self.getGlobalSettingsAsJson())

        def saveToPersistent(self):
            renpy.store.persistent.JK_Settings = self.getSettingsAsJson()

            renpy.save_persistent()

        def reset(self, include_global):
            rebuild_ui = False
            if self.sizeAdjustment != 0:
                rebuild_ui = True

            renpy.store.persistent.JK_Settings = None
            UserDir.removeSettings()

            if include_global:
                UserDir.removeGlobalSettings()
            
            self.setSettings(self.getSettingsForReset(no_globals=include_global))

            self.save()

            if rebuild_ui:
                renpy.store.gui.rebuild()

        class ConfirmReset(renpy.ui.Action):
            def __init__(self, include_global=False):
                self.include_global = include_global

            def __call__(self):
                showConfirm(
                    title="Reset settings",
                    message="Do you really wish to reset all settings into their default configuration?",
                    yes=Settings.Reset(self.include_global),
                    yesIcon="\ue8ba",
                    yesColor=Colors.danger
                )

        class Reset(renpy.ui.Action):
            def __init__(self, include_global=False):
                self.include_global = include_global

            def __call__(self):
                Settings.reset(self.include_global)
                renpy.restart_interaction()

        class ToggleEnabled(renpy.ui.Action):
            def __init__(self, attr_name):
                self.attr_name = attr_name

            def __call__(self):
                setattr(Settings, self.attr_name, not getattr(Settings, self.attr_name))

                Settings.save()
                renpy.restart_interaction()

        class Set(renpy.ui.Action):
            def __init__(self, attr_name, value):
                self.attr_name = attr_name
                self.value = value

            def __call__(self):
                setattr(Settings, self.attr_name, self.value)

                Settings.save()
                renpy.restart_interaction()

        class SetAutosaveToggleKey(SetKey):
            def __call__(self):
                Settings.autosaveKey = self.resolveKey()

                Settings.save()
                renpy.restart_interaction()

        class SetQuickSaveKey(SetKey):
            def __call__(self):
                Settings.quickSaveKey = self.resolveKey()

                Settings.save()
                renpy.restart_interaction()

        class SetCreateMemoryKey(SetKey):
            def __call__(self):
                Settings.memoriesKey = self.resolveKey()

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
                if self.name in Settings.saveScreenName:
                    Settings.saveScreenName.remove(self.name)
                else:
                    Settings.saveScreenName.append(self.name)
                Settings.save()
                renpy.restart_interaction()

        class SetLoadScreenName(renpy.ui.Action):
            def __init__(self, name):
                self.name = name

            def __call__(self):
                if self.name in Settings.loadScreenName:
                    Settings.loadScreenName.remove(self.name)
                else:
                    Settings.loadScreenName.append(self.name)
                Settings.save()
                renpy.restart_interaction()

        class IncrementSizeAdjustment(renpy.ui.Action):
            def __call__(self):
                if renpy.store.persistent.JK_SizeAdjustmentRollbackValue is None:
                    renpy.store.persistent.JK_SizeAdjustmentRollbackValue = int(Settings.sizeAdjustment)

                Settings.sizeAdjustment = min(Settings.sizeAdjustment + 1, 100)
                Settings.save()
                renpy.restart_interaction()

                if renpy.store.persistent.JK_SizeAdjustmentRollbackValue == Settings.sizeAdjustment or Settings.sizeAdjustment == 0:
                    renpy.store.persistent.JK_SizeAdjustmentRollbackValue = None
        
        class DecrementSizeAdjustment(renpy.ui.Action):
            def __call__(self):
                if renpy.store.persistent.JK_SizeAdjustmentRollbackValue is None:
                    renpy.store.persistent.JK_SizeAdjustmentRollbackValue = int(Settings.sizeAdjustment)

                Settings.sizeAdjustment = max(Settings.sizeAdjustment - 1, -100)
                Settings.save()
                renpy.restart_interaction()

                if renpy.store.persistent.JK_SizeAdjustmentRollbackValue == Settings.sizeAdjustment or Settings.sizeAdjustment == 0:
                    renpy.store.persistent.JK_SizeAdjustmentRollbackValue = None

        class ApplySizeAdjustment(renpy.ui.Action):
            def __call__(self):
                renpy.store.gui.rebuild()

                if renpy.store.persistent.JK_SizeAdjustmentRollbackValue is not None:
                    renpy.show_screen("JK_ConfirmSizeAdjustment")

        class SetSizeAdjustment(renpy.ui.Action):
            def __init__(self, value, store_rollback_value=True):
                self.store_rollback_value = store_rollback_value
                self.value = value or 0

            def __call__(self):
                if self.store_rollback_value:
                    if renpy.store.persistent.JK_SizeAdjustmentRollbackValue is None:
                        renpy.store.persistent.JK_SizeAdjustmentRollbackValue = self.value

                Settings.sizeAdjustment = self.value
                Settings.save()
                renpy.restart_interaction()

                if renpy.store.persistent.JK_SizeAdjustmentRollbackValue == Settings.sizeAdjustment or Settings.sizeAdjustment == 0:
                    renpy.store.persistent.JK_SizeAdjustmentRollbackValue = None

        class ResetSizeAdjustment(renpy.ui.Action):
            def __call__(self):
                Settings.sizeAdjustment = 0
                #Also reset sidepanel and pagination positions just in case there are positioned somewhere outside of the screen
                renpy.store.persistent.JK_SidepanelPos = None
                renpy.store.persistent.JK_PaginationPos = None
                Settings.save()
                renpy.restart_interaction()

        class SetChangeSidepanelVisibilityKey(SetKey):
            def __call__(self):
                Settings.changeSidepanelVisibilityKey = self.resolveKey()
                renpy.config.gestures['w_s_e_s_w'] = Settings.changeSidepanelVisibilityKey

                Settings.save()
                renpy.restart_interaction()

        
        class ToggleGlobalizedSetting(renpy.ui.Action):
            def __init__(self, setting_name):
                self.setting_name = setting_name

            def __call__(self):
                if self.setting_name in Settings.globalizedSettings:
                    Settings.globalizedSettings.remove(self.setting_name)
                else:
                    Settings.globalizedSettings.append(self.setting_name)

                Settings.save()
                renpy.restart_interaction()

        class SaveDefaultPlaythroughTemplate(renpy.ui.Action):
            def __init__(self, playthrough_template, name, description, storeChoices, autosaveOnChoices, useChoiceLabelAsSaveName, enabledSaveLocations):#MODIFY HERE
                self.template = playthrough_template.edit(name=name, description=description, storeChoices=storeChoices, autosaveOnChoices=autosaveOnChoices, useChoiceLabelAsSaveName=useChoiceLabelAsSaveName, enabledSaveLocations=enabledSaveLocations)#MODIFY HERE

            def __call__(self):
                Settings.playthroughTemplate = self.template.serializable_for_template()

                Settings.save()
                renpy.restart_interaction()

        class TogglePreventAutosavingWhileNotInGameEnabled(renpy.ui.Action):
            def __call__(self):
                Settings.preventAutosavingWhileNotInGame = not Settings.preventAutosavingWhileNotInGame

                Autosaver.prevent_autosaving = False

                Settings.save()
                renpy.restart_interaction()

        class ToggleSidepanelHorizontalEnabled(renpy.ui.Action):
            def __call__(self):
                Settings.sidepanelHorizontal = not Settings.sidepanelHorizontal

                Settings.save()

                Settings.ResetSidepanelPosition()()

        class ResetSidepanelPosition(renpy.ui.Action):
            def __call__(self):
                renpy.store.persistent.JK_SidepanelPos = None

                renpy.restart_interaction()

        class SetSearchPlaythroughKey(SetKey):
            def __call__(self):
                Settings.searchPlaythroughKey = self.resolveKey()

                Settings.save()
                renpy.restart_interaction()

        class SetSearchPlaythroughsKey(SetKey):
            def __call__(self):
                Settings.searchPlaythroughsKey = self.resolveKey()

                Settings.save()
                renpy.restart_interaction()
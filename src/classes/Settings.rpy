init -1 python in JK:
    _constant = True

    import os
    import json
    import __main__
    import io

    # Main Settings class
    class SettingsClass(x52NonPicklable):
        def __init__(self):
            global_settings = self.load_from_global_settings()

            settings = {}
            settings.update(global_settings)
            settings.update(self.load_from_user_dir())
            settings.update(self.load_from_persistent())

            # Apply globalized settings again in case some local setting is overwriting it
            for setting in settings.get("globalizedSettings", []):
                if global_settings.get(setting):
                    settings[setting] = global_settings.get(setting)

            self.set_settings(settings)

        def load_from_user_dir(self):
            return UserDir.load_settings()

        def load_from_global_settings(self):
            return UserDir.load_global_settings()

        def load_from_persistent(self):
            if renpy.store.persistent.JK_Settings:
                data = json.loads(renpy.store.persistent.JK_Settings)
            else:
                data = {}

            return data

        def set_settings(self, data):
            self.autosaveNotificationEnabled = data.get("autosaveNotificationEnabled", False)
            self.autosaveKey = data.get("autosaveKey", "alt_K_a")
            self.quickSaveEnabled = data.get("quickSaveEnabled", True)
            self.quickSaveNotificationEnabled = data.get("quickSaveNotificationEnabled", True)
            self.quickSaveKey = data.get("quickSaveKey", "K_F5")
            self.memoriesEnabled = data.get("memoriesEnabled", False)
            self.memoriesKey = data.get("memoriesKey", "K_BACKQUOTE")
            self.customGridEnabled = data.get("customGridEnabled", False)
            self.customGridX = data.get("customGridX", (renpy.store.gui.file_slot_cols if hasattr(renpy.store.gui, "file_slot_cols") else 2) or 2)
            self.customGridY = data.get("customGridY", (renpy.store.gui.file_slot_rows if hasattr(renpy.store.gui, "file_slot_rows") else 2) or 2)
            self.loadScreenName = data.get("loadScreenName", ["load"])
            self.saveScreenName = data.get("saveScreenName", ["save"])
            self.offsetSlotAfterManualSaveIsLoaded = data.get("offsetSlotAfterManualSaveIsLoaded", False)
            self.offsetSlotAfterManualSave = data.get("offsetSlotAfterManualSave", True)
            self.offsetSlotAfterQuickSave = data.get("offsetSlotAfterQuickSave", True)
            self.sizeAdjustment = data.get("sizeAdjustment", 0) or 0
            self.changeSidepanelVisibilityKey = data.get("changeSidepanelVisibilityKey", "alt_K_p")
            self.debugEnabled = data.get("debugEnabled", False)
            self.pageFollowsQuickSave = data.get("pageFollowsQuickSave", True)
            self.pageFollowsAutoSave = data.get("pageFollowsAutoSave", True)
            self.updaterEnabled = data.get("updaterEnabled", True)
            self.autoUpdateWithoutPrompt = data.get("autoUpdateWithoutPrompt", False)
            self.globalizedSettings = data.get("globalizedSettings", [])
            self.autosaveOnSingletonChoice = data.get("autosaveOnSingletonChoice", False)
            self.playthroughTemplate = data.get("playthroughTemplate", None)
            self.preventAutosavingWhileNotInGame = data.get("preventAutosavingWhileNotInGame", True)
            self.seamlessPagination = data.get("seamlessPagination", False)
            self.autosaveOnQuestion = data.get("autosaveOnQuestion", True)
            self.sidepanelHorizontal = data.get("sidepanelHorizontal", False)
            self.searchPlaythroughKey = data.get("searchPlaythroughKey", "ctrl_K_f")
            self.searchPlaythroughsKey = data.get("searchPlaythroughsKey", "ctrl_shift_K_f")
            self.showConfirmOnLargePageJump = data.get("showConfirmOnLargePageJump", True)
            self.dialogOpacity = data.get("dialogOpacity", 1)
            self.sidepanelOpacity = data.get("sidepanelOpacity", 0.8)
            self.paginationOpacity = data.get("paginationOpacity", 0.9)
            self.preventAutosaveModifierKey = data.get("preventAutosaveModifierKey", "ALT")
            self.noUpdatePrompt = data.get("noUpdatePrompt", False)
            self.autosaveOnNormalButtonsWithJump = data.get("autosaveOnNormalButtonsWithJump", False)
            self.playthroughsViewMode = data.get("playthroughsViewMode", "grid")
            self.paginationQuickSaves = data.get("paginationQuickSaves", True)
            self.paginationAutoSaves = data.get("paginationAutoSaves", True)
            self.paginationFirstPage = data.get("paginationFirstPage", True)
            self.paginationLastPage = data.get("paginationLastPage", True)
            self.paginationBigJump = data.get("paginationBigJump", True)
            self.paginationGoTo = data.get("paginationGoTo", True)
            self.paginationNumbers = data.get("paginationNumbers", True)

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
                'offsetSlotAfterQuickSave': self.offsetSlotAfterQuickSave,
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
                'dialogOpacity': self.dialogOpacity,
                'sidepanelOpacity': self.sidepanelOpacity,
                'paginationOpacity': self.paginationOpacity,
                'preventAutosaveModifierKey': self.preventAutosaveModifierKey,
                'noUpdatePrompt': self.noUpdatePrompt,
                'autosaveOnNormalButtonsWithJump': self.autosaveOnNormalButtonsWithJump,
                'playthroughsViewMode': self.playthroughsViewMode,
                'paginationQuickSaves': self.paginationQuickSaves,
                'paginationAutoSaves': self.paginationAutoSaves,
                'paginationFirstPage': self.paginationFirstPage,
                'paginationLastPage': self.paginationLastPage,
                'paginationBigJump': self.paginationBigJump,
                'paginationGoTo': self.paginationGoTo,
                'paginationNumbers': self.paginationNumbers,
            })

        def get_settings_for_reset(self, no_globals=False):
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

        def get_global_settings_as_json(self):
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
            self.save_to_user_dir()
            self.save_to_globals()
            self.save_to_persistent()

        def save_to_user_dir(self):
            UserDir.save_settings(self.getSettingsAsJson())

        def save_to_globals(self):
            UserDir.save_global_settings(self.get_global_settings_as_json())

        def save_to_persistent(self):
            renpy.store.persistent.JK_Settings = self.getSettingsAsJson()

            renpy.save_persistent()

        def reset(self, include_global):
            rebuild_ui = False
            if self.sizeAdjustment != 0:
                rebuild_ui = True

            renpy.store.persistent.JK_Settings = None
            UserDir.remove_settings()

            if include_global:
                UserDir.remove_global_settings()
            
            self.set_settings(self.get_settings_for_reset(no_globals=include_global))

            self.save()

            if rebuild_ui:
                renpy.store.gui.rebuild()

        class ResetAction(renpy.ui.Action):
            def __init__(self, include_global=False):
                self.include_global = include_global

            def __call__(self):
                Settings.reset(self.include_global)
                renpy.restart_interaction()

        class ToggleEnabledAction(renpy.ui.Action):
            def __init__(self, attr_name):
                self.attr_name = attr_name

            def __call__(self):
                setattr(Settings, self.attr_name, not getattr(Settings, self.attr_name))

                Settings.save()
                renpy.restart_interaction()

        class SetAction(renpy.ui.Action):
            def __init__(self, attr_name, value):
                self.attr_name = attr_name
                self.value = value

            def __call__(self):
                setattr(Settings, self.attr_name, self.value)

                Settings.save()
                renpy.restart_interaction()

        class IncrementAction(renpy.ui.Action):
            def __init__(self, attr_name, amount=1, min=None, max=None):
                self.attr_name = attr_name
                self.amount = amount
                self.min = min
                self.max = max

            def __call__(self):
                current_value = getattr(Settings, self.attr_name)
                new_value = current_value + self.amount

                if self.min:
                    new_value = max(self.min, new_value)

                if self.max:
                    new_value = min(self.max, new_value)

                Settings.SetAction(self.attr_name, new_value)()

        @staticmethod
        def DecrementAction(key, amount=-1, min=None):
            return Settings.IncrementAction(key, amount, min)

        class SetSaveScreenNameAction(renpy.ui.Action):
            def __init__(self, name):
                self.name = name

            def __call__(self):
                if self.name in Settings.saveScreenName:
                    Settings.saveScreenName.remove(self.name)
                else:
                    Settings.saveScreenName.append(self.name)
                Settings.save()
                renpy.restart_interaction()

        class SetLoadScreenNameAction(renpy.ui.Action):
            def __init__(self, name):
                self.name = name

            def __call__(self):
                if self.name in Settings.loadScreenName:
                    Settings.loadScreenName.remove(self.name)
                else:
                    Settings.loadScreenName.append(self.name)
                Settings.save()
                renpy.restart_interaction()

        class IncrementSizeAdjustmentAction(renpy.ui.Action):
            def __call__(self):
                if renpy.store.persistent.JK_SizeAdjustmentRollbackValue is None:
                    renpy.store.persistent.JK_SizeAdjustmentRollbackValue = int(Settings.sizeAdjustment)

                Settings.sizeAdjustment = min(Settings.sizeAdjustment + 1, 100)
                Settings.save()
                renpy.restart_interaction()

                if renpy.store.persistent.JK_SizeAdjustmentRollbackValue == Settings.sizeAdjustment or Settings.sizeAdjustment == 0:
                    renpy.store.persistent.JK_SizeAdjustmentRollbackValue = None
        
        class DecrementSizeAdjustmentAction(renpy.ui.Action):
            def __call__(self):
                if renpy.store.persistent.JK_SizeAdjustmentRollbackValue is None:
                    renpy.store.persistent.JK_SizeAdjustmentRollbackValue = int(Settings.sizeAdjustment)

                Settings.sizeAdjustment = max(Settings.sizeAdjustment - 1, -100)
                Settings.save()
                renpy.restart_interaction()

                if renpy.store.persistent.JK_SizeAdjustmentRollbackValue == Settings.sizeAdjustment or Settings.sizeAdjustment == 0:
                    renpy.store.persistent.JK_SizeAdjustmentRollbackValue = None

        class ApplySizeAdjustmentAction(renpy.ui.Action):
            def __call__(self):
                renpy.store.gui.rebuild()

                if renpy.store.persistent.JK_SizeAdjustmentRollbackValue is not None:
                    renpy.show_screen("JK_ConfirmSizeAdjustment")

        class SetSizeAdjustmentAction(renpy.ui.Action):
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

        class ResetSizeAdjustmentAction(renpy.ui.Action):
            def __call__(self):
                Settings.sizeAdjustment = 0
                #Also reset sidepanel and pagination positions just in case there are positioned somewhere outside of the screen
                renpy.store.persistent.JK_SidepanelPos = None
                renpy.store.persistent.JK_PaginationPos = None
                Settings.save()
                renpy.restart_interaction()

        class SetChangeSidepanelVisibilityKeyAction(SetKeyAction):
            def __call__(self):
                Settings.changeSidepanelVisibilityKey = self.resolve_key()
                renpy.config.gestures['n_e_s_w'] = Settings.changeSidepanelVisibilityKey

                Settings.save()
                renpy.restart_interaction()

        class ToggleGlobalizedSettingAction(renpy.ui.Action):
            def __init__(self, setting_name):
                self.setting_name = setting_name

            def __call__(self):
                if self.setting_name in Settings.globalizedSettings:
                    Settings.globalizedSettings.remove(self.setting_name)
                else:
                    Settings.globalizedSettings.append(self.setting_name)

                Settings.save()
                renpy.restart_interaction()

        class SaveDefaultPlaythroughTemplateAction(renpy.ui.Action):
            def __init__(self, playthrough_template, name, description, storeChoices, autosaveOnChoices, useChoiceLabelAsSaveName, enabledSaveLocations):#MODIFY HERE
                self.template = playthrough_template.edit(name=name, description=description, storeChoices=storeChoices, autosaveOnChoices=autosaveOnChoices, useChoiceLabelAsSaveName=useChoiceLabelAsSaveName, enabledSaveLocations=enabledSaveLocations)#MODIFY HERE

            def __call__(self):
                Settings.playthroughTemplate = self.template.serialize_template_for_json()

                Settings.save()
                renpy.restart_interaction()

        class TogglePreventAutosavingWhileNotInGameEnabledAction(renpy.ui.Action):
            def __call__(self):
                Settings.preventAutosavingWhileNotInGame = not Settings.preventAutosavingWhileNotInGame

                Autosaver.prevent_autosaving = False

                Settings.save()
                renpy.restart_interaction()

        class ToggleSidepanelHorizontalEnabledAction(renpy.ui.Action):
            def __call__(self):
                Settings.sidepanelHorizontal = not Settings.sidepanelHorizontal

                Settings.save()

                Settings.ResetSidepanelPositionAction()()

        class ResetSidepanelPositionAction(renpy.ui.Action):
            def __call__(self):
                renpy.store.persistent.JK_SidepanelPos = None

                renpy.restart_interaction()

        class FieldValueAction(renpy.store.FieldValue):
            def changed(self, value):
                super(Settings.FieldValueAction, self).changed(value)

                Settings.save()

        class ShowSaveLoadAction(renpy.ui.Action):
            def __call__(self):
                renpy.store.Show('JK_Settings', section='SAVE_LOAD')()

        # ==============
        # Static methods
        # ==============

        @staticmethod
        def get_set_key_action(key):
            class SetKeyAction(renpy.store.JK.SetKeyAction):
                def __call__(self):
                    setattr(Settings, key, self.resolve_key())

                    Settings.save()
                    renpy.restart_interaction()

            return SetKeyAction
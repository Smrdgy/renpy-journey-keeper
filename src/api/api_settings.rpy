init 1 python in JK.api.settings:
    JK = renpy.exports.store.JK

    def set_setting(setting_key, value, save=True):
        """"
        Sets the specific setting based on `setting_key` with a `value`

        Args:
            setting_key (str):
                "autosaveNotificationEnabled" (bool): Whether to show notification when autosave is performed.
                "autosaveKey" (key): Which key should toggle autosave.
                "quickSaveEnabled" (bool): Whether quick save is allowed.
                "quickSaveNotificationEnabled" (bool): Whether to show notification when quick save is perfomed.
                "quickSaveKey" (key): Which key should trigger quick save.
                "customGridEnabled" (bool): Whether to use custom save/load grid.
                "customGridX" (int): Number of columns in the save/load grid.
                "customGridY" (int): Number of rows in the save/load grid.
                "loadScreenName" (list<str>): List of strings of load screen names. On these screens, the sidepanel will be visible.
                "saveScreenName" (list<str>): List of strings of save screen names. On these screens, the sidepanel will be visible.
                "offsetSlotAfterManualSaveIsLoaded" (bool): Whether to offset the slot counter by +1 when a manual save is loaded, in order to prevent overwriting it with the next auto/quick save.
                "offsetSlotAfterManualSave" (bool): Whether to offset the slot counter by +1 when a manual save is created, in order to prevent overwriting it with the next auto/quick save.
                "offsetSlotAfterQuickSave" (bool): Whether to offset the slot counter by +1 when a quick save is created, in order to prevent overwriting it with the next auto/quick save.
                "sizeAdjustment" (int): Adjustment value for the overall sizes of texts, paddings, offsets, etc. Some games, mostly with resolution 720p and 4K have different pixel densities which then make this mod either too big or too small. There is an automatic correction in place, but it isn't perfect.
                "changeSidepanelVisibilityKey" (key): Which key should cycle the sidepanel visibity.
                "debugEnabled" (bool): Whether debug is enabled.
                "pageFollowsQuickSave" (bool): When making a quick save that is placed on another page than the player currently is on, it will change to the page where the quick save was made.
                "pageFollowsAutoSave" (bool): When making an autosave that is placed on another page than the player currently is on, it will change to the page where the autosave was made.
                "updaterEnabled" (bool): Whether the auto updater is enabled.
                "autoUpdateWithoutPrompt" (bool): Whether to download the update without prompting the player.
                "autosaveOnSingletonChoice" (bool): Whether to perform an autosave on a single visible choice.
                "playthroughTemplate" (str): A default template of a new playthrough. Has the same structure as PlaythroughClass when serialized into JSON.
                "preventAutosavingWhileNotInGame" (bool): Whether to prevent autosaving when not in game. If true, the Autosaver will wait for "start" label before allowing any autosaves.
                "seamlessPagination" (bool): Whether to use seamless pagination. Check settings in the mod to see the difference, but in a nutshell seamless pagination always holds the currently active page in the center.
                "sidepanelHorizontal" (bool): Whether to show the sidepanel horizontally.
                "searchPlaythroughKey" (key): Which key should open the search screen for a single playthrough.
                "searchPlaythroughsKey" (key): Which key should open the search screen for all playthroughs.
                "showConfirmOnLargePageJump" (bool): Whether to show confirm on large changes of page while playing the game (not menu!).
                "dialogOpacity" (float): A number ranging from 0 to 1 representing the opacity of the dialog background.
                "sidepanelOpacity" (float): A number ranging from 0 to 1 representing the opacity of the sidepanel background.
                "paginationOpacity" (float): A number ranging from 0 to 1 representing the opacity of the pagination background.
                "preventAutosaveModifierKey" ("SHIFT"|"ALT"|None) A modifier key that when held, it will skip the autosaving feature.
                "noUpdatePrompt" (bool): When enabled, it will not show the update prompt of a new version. `updaterEnabled` must be True!
                "autosaveOnNormalButtonsWithJump" (bool): When enabled even normal buttons (that contain Jump) will be considered a choice buttons.
                "playthroughsViewMode" ("GRID"|"ROWS"): Playthroughs picker visibility mode
                "paginationQuickSaves" (bool): Whether to show the native Ren'Py Quick Saves button (Q) on the custom pagination
                "paginationAutoSaves" (bool): Whether to show the native Ren'Py Auto Saves button (A) on the custom pagination
                "paginationFirstPage" (bool): Whether to show the first page button (|<) on the custom pagination
                "paginationLastPage" (bool): Whether to show the last page button (>|) on the custom pagination
                "paginationBigJump" (bool): Whether to show the big jump buttons (<< & >>) on the custom pagination
                "paginationGoTo" (bool): Whether to show the Go-To button on the custom pagination
                "paginationNumbers" (bool): Whether to show the pages on the custom pagination

            value: Value to set, see the types in brackets next to the setting key.
        """

        if setting_key == "globalizedSettings":
            raise Exception("Which settings to globalize should not be changed programatically! That is for each player to decide on their own.")

        setattr(JK.Settings, setting_key, value)

        if save:
            JK.Settings.save()

    def save():
        """ Saves the settings into persistent storage and user directory (if available) """

        JK.Settings.save()
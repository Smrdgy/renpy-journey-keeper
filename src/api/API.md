> ## ⚠️ All API definitions are in `init 1` python blocks.<br>Ensure your modifications use at least `init 2`, or are triggered after the init phase. ⚠️

# Playthroughs API Documentation

Here you can find all the functions and actions related to playthroughs.

accessed through `JK.api.playthroughs`

---

## Terminology

- **playthrough**: A `PlaythroughClass` instance representing a collection of saves.
- **activation**: A process that swaps active save directories and refreshes save/load screens with saves from a specific playthrough.
- **id**: A numerical unique identifier. Currently, IDs 1 and 2 are reserved, as well as any numbers beyond approximately 1,730,000,000 (which come from a timestamp using `time.time()`).
- **[something]Action**: Represents a class inheriting from `renpy.ui.Action` that can be called directly in the script without triggering immediately. Useful for buttons and key actions.
- **autosave**: Unlike Ren'Py's native autosaves, these saves are stored directly into numbered pages and store which choice was made.
- **quick save**: Unlike Ren'Py's native quick saves, these saves are stored directly into numbered pages. (Default: triggered by pressing F5.)

---

## Functions

### `list_all()`
Returns a list of all playthrough instances.

**Returns:**
- `PlaythroughClass[]`

---

### `list_all_filtered(additional_filter_callback=None, include_hidden=False)`
Returns a list of all playthroughs that pass all the conditions set by filters and are not hidden (unless `include_hidden` is set to True)

Results are going to be affected by these callback functions:
  - `additional_filter_callback`
  - `JK.api.callbacks.playthroughs_filter_callbacks`

Args:
  - `additional_filter_callback (Callable[[PlaythroughClass], bool]?)`: If defined, this function must return either True or False, otherwise you'll get an exception. `True` allows the playthrough to be included, while `False` will filter it out.
  - `include_hidden (bool?)`: By default, hidden playthroughs are filtered out, if `True`, they will be included.


**Returns:**
- `PlaythroughClass[]`

**Example:**
```python
a = JK.api.playthroughs.create_playthrough_instance(name="A")
b = JK.api.playthroughs.create_playthrough_instance(name="B", hidden=True)
c = JK.api.playthroughs.create_playthrough_instance(name="C")

JK.api.playthroughs.add(a, activate=False, save=False, restart_interaction=False)
JK.api.playthroughs.add(b, activate=False, save=False, restart_interaction=False)
JK.api.playthroughs.add(c)

print(JK.api.playthroughs.list_all_filtered()) # -> [a, c]
print(JK.api.playthroughs.list_all_filtered(include_hidden=True)) # -> [a, b, c]
print(JK.api.playthroughs.list_all_filtered(lambda playthrough: playthrough.name == "C")) # -> [c]

JK.api.callbacks.playthroughs_filter_callbacks.append(lambda p: p.name == "A")
print(JK.api.playthroughs.list_all_filtered()) # -> [a]
print(JK.api.playthroughs.list_all_filtered(lambda playthrough: playthrough.name == "C")) # -> []
```
---

### `get_active()`
Returns the currently active playthrough. If there is none, the native playthrough is returned.

**Returns:**
- `PlaythroughClass`

---

### `get_by_name(name)`
Returns a playthrough by its name.

**Args:**
- `name (str)`: Name of the playthrough

**Returns:**
- `PlaythroughClass` if found
- `None` if not found

---

### `get_by_id(id)`
Returns a playthrough by its ID.

**Args:**
- `id (int)`

**Returns:**
- `PlaythroughClass` if found
- `None` if not found

---

### `get_index_by_id(id)`
Returns the index of a playthrough by its ID.

**Args:**
- `id (int)`

**Returns:**
- `int`: Matching index
- `-1`: If not found

---

### `add(playthrough, activate=True, save=True, restart_interaction=True)`
Adds a playthrough instance to the collection.

**Args:**
- `playthrough (PlaythroughClass)`
- `activate (bool?)`: Automatically activate after adding *(recommended off when adding multiple)*
- `save (bool?)`: Save the collection immediately *(recommended off when adding multiple)*
- `restart_interaction (bool?)`: Restart interaction after adding *(recommended off when adding multiple)*
- `i_know_what_i_am_doing_with_the_name_so_skip_the_check (bool?)`: A safety override for those who like to live dangerously. If set to True, it will skip the `name` check and add the playthrough regardless of any conflicting names that already exist. ⚠️ If you choose to do this, make absolutely sure you have set the `directory` on the playthrough instance! ⚠️

**Returns:**
- `PlaythroughClass`

Example
```python
playthrough = JK.api.playthroughs.create_playthrough_instance(name="Test")
JK.api.playthroughs.add(playthrough)
```

---

### `edit(original, other, moveSaveDirectory=False)`
Edits the original playthrough with data from another playthrough.

**Args:**
- `original (PlaythroughClass)`: The playthrough to modify
- `other (PlaythroughClass)`: Source of new data
- `allow_moving_save_directory (bool?)`: Move the save directory (on the machine) if names differ

**Returns:**
- `PlaythroughClass`

Example
```python
original_playthrough = JK.api.playthroughs.create_playthrough_instance(name="Original")
edited_playthrough = JK.api.playthroughs.create_playthrough_instance(name="New")

JK.api.playthroughs.edit(original_playthrough, edited_playthrough)

print(original_playthrough.name) # -> "New"
```

---

### `add_or_edit(playthrough, allow_moving_save_directory=False, force=False)`
Adds a new playthrough if it did not exist before based on ID, or edits the data of an existing one.

**Args:**
- `playthrough (PlaythroughClass)`
- `allow_moving_save_directory (bool?)`
- `force (bool?)`

**Returns:**
- `PlaythroughClass`

---

### `remove_by_id(id)`
Removes a playthrough by ID.

**Args:**
- `id (int)`
- delete_save_files (bool, default=False): Whether to delete all the save files related to this playthrough from the machine

**Returns:**
- `bool`: `True` if removed, `False` otherwise

---

### `toggle_autosave_on_choice_for_active()`
Toggles the "Autosave on Choice" feature for the currently active playthrough.

---

### `set_autosave_on_choice_for_active(enabled)`
Sets the "Autosave on Choice" feature for the currently active playthrough.

**Args:**
- `enabled (bool)`

---

### `activate_by_name(name)`
Activates a playthrough by its name.

**Args:**
- `name (str)`

---

### `activate_by_id(id)`
Activates a playthrough by its ID.

**Args:**
- `id (int)`

---

### `activate_by_instance(playthrough)`
Activates a playthrough by its instance.

**Args:**
- `playthrough (PlaythroughClass)`

---

### `activate_native()`
Activates the native (default) playthrough (#1).

---

### `activate_first()`
Activates the first available playthrough (same as `activate_native()`).

---

### `save()`
Saves all playthroughs into persistent storage and the user directory (if available).

---

### `is_name_available(name)`
Checks if a playthrough name is available (not already used).

**Args:**
- `name (str)`

**Returns:**
- `bool`

---

### `get_encoded_thumbnail()`
Returns a UTF-8 base64-encoded thumbnail ready for storage.  
Useful for manual retrieval of thumbnail for programmatically creating new playthroughs with a thumbnail.
⚠️ Just make sure to not print it into a console! It can't handle the amount of text and will crash... ⚠️
If that happens, you have to clear the persistent storage...

**Returns:**
- `str`

Example
```python
thumbnail = JK.api.playthroughs.get_encoded_thumbnail()
with open(renpy.os.path.join(renpy.config.basedir, "thumbnail.txt"), "w", encoding="utf-8") as f:
    f.write(thumbnail)
    f.close()
```
then
```python
JK.api.playthroughs.create_playthrough_instance(name="Example", thumbnail="[Paste the thumbnail string here]")
...
```

---

### `output_encoded_thumbnail_into_file(filename="thumbnail.txt")`
Outputs the encoded thumbnail into a file (duh).
Unlike `get_encoded_thumbnail()`, this is console-safe and requires no additional code to get the thumbnail.

**Args:**
- `filename (str, default="thumbnail.txt")`: Name of the file where the string will be outputted

---

## Actions

### `ToggleAutosaveOnChoiceForActiveAction`
Asynchronous action that toggles the "Autosave on Choice" feature.  
Can be used directly in buttons or key mappings to avoid UI stutter.

Example
```python
screen Example():
    textbutton "Toggle" action JK.api.playthroughs.ToggleAutosaveOnChoiceForActiveAction()
```

---

### `PerformQuickSaveAction`
Performs a quick save operation.

Example
```python
screen ExampleOverlay():
    key "K_q" action JK.api.playthroughs.PerformQuickSaveAction()
```

---

## Playthrough related functions

### Functions

#### `create_playthrough_instance(name, id=None, directory=None, description=None, thumbnail=None, autosave_on_choice=True, use_choice_label_as_save_name=False, enabled_save_locations=None, meta=None, native=False, directory_immovable=False, hidden=False, serializable=True, deletable=True)`
Creates a new playthrough instance.

**Args:**
- `name (str)`: Name of the playthrough **(Required)**
- `id (int?)`: ID of the playthrough (optional; auto-fills with a timestamp if `None`)
- `directory (str?)`: Save directory name (optional; defaults from `name`)
- `description (str?)`: A description players can read (optional)
- `thumbnail (str?)`: UTF-8 base64 encoded thumbnail (optional)
- `autosave_on_choice (bool?)`: Enable "Autosave on Choice"
- `use_choice_label_as_save_name (bool?)`: Use the choice label as the save name
- `enabled_save_locations ([list<str> or None]?)`:
A list of keywords ("USER"/"GAME") and full system paths where this playthrough will store its saves 
  - `list`:
    - `"USER"`: User directory (e.g., `%appdata%` on Windows)
    - `"GAME"`: `/game/saves` directory
    - `str`: Full system path
  - `None`: Enable all
- `meta ([anything JSON serializable]?)`: Optional metadata associated with the playthrough. It can be any type you wish, as long as it's JSON serializable.
- `native (bool?)`: Marks the playthrough as a built-in or system-level playthrough.
- `directory_immovable (bool?)`: Prevents the playthrough's saves directory from being moved or renamed.
- `hidden (bool?)`: Hides the playthrough from standard user interfaces.
- `serializable (bool?)`: Controls whether the playthrough should be saved to persistent storage.
- `deletable (bool?)`: Determines whether the playthrough can be deleted by the player or system.

**Returns:**
- `PlaythroughClass`

## PlaythroughClass

I'm so sorry about this class... It's the oldest one along with PlaythroughsClass, and it's a complete mess.
I hope to clean it up some day, but we will see.

### Attributes
- `id (int)`:
A numerical unique identifier.
Currently, IDs 1 and 2 are reserved, as well as any numbers beyond approximately 1,730,000,000 (which come from a timestamp using `time.time()`).
- `name (str)`
A name of the playthrough
- `directory (str)`
A name of the directory where the saves are going to be stored  
- `description (str?)`
A description of the playthrough the player can read
- `thumbnail (str?)`
UTF-8 base64-encoded thumbnail image
- `storeChoices (bool)` [DEPRECATED]
Was supposed to determine whether to store choices in the save files, but I must have forgotten about it, and now it doesn't make much sense.
- `autosaveOnChoices (bool)`
Whether to perform an autosave when player makes a choice
- `selectedPage (int)`
Currently selected page in the save/load screen.
When switching playthroughs this value is being set from `renpy.store.persistent._file_page`.
Likewise, when the playthrough is being activated, this value is overwriting `renpy.store.persistent._file_page`.
- `filePageName (dict)`
Same as `selectedPage` above, this value stores and modifies `renpy.store.persistent._file_page_name`.
- `useChoiceLabelAsSaveName (bool)`
When true, the choice label is also used as a save name (the text under timestamp in the save/load screens) when performing an autosave.
- `enabledSaveLocations (list<str> or None)`
A list of keywords ("USER"/"GAME") and full system paths where this playthrough will store its saves 
  - `list`:
    - `"USER"`: User directory (e.g., `%appdata%` on Windows)
    - `"GAME"`: `/game/saves` directory
    - `str`: Full system path
  - `None`: Enable all
- `meta (anything JSON serializable)`
Optional metadata associated with the playthrough. It can be any type you wish, as long as it's JSON serializable.
- `native (bool)`
Marks the playthrough as a built-in or system-level playthrough.
- `directory_immovable (bool)`
Prevents the playthrough's saves directory from being moved or renamed.
- `hidden (bool)`
Hides the playthrough from standard user interfaces.
- `serializable (bool)`
Controls whether the playthrough should be saved to persistent storage.
- `deletable (bool)`
Determines whether the playthrough can be deleted by the user or system.

### Methods

#### `regenerate_unique_data()`
Regenerates a unique `id` and save `directory` from the playthrough's name.

---

#### `remove_unique_data()`
Resets `id` and clears the `directory`.

---

#### `copy()`
Creates a deep copy of the playthrough.

---

#### `edit(**kwargs)`
Updates the playthrough's attributes dynamically.
You can pass any of the attributes as key-worded arguments without affecting the rest.

Example
```python
playthrough.edit(name="Test", useChoiceLabelAsSaveName=True)
```

---

#### `edit_from_playthrough(playthrough, moveSaveDirectory=False)`
Copies data from another `PlaythroughClass` instance.
If `moveSaveDirectory` is True, also allow renaming of a directory when names are not identical.

---

#### `serialize_for_json()`
Returns a JSON-serializable dictionary of the playthrough data.

---

#### `serialize_template_for_json()`
Returns a JSON-serializable dictionary suitable for being used as a template (without IDs or directories).

---

#### `serialize_to_json_string()`
Returns the full serialized playthrough as a JSON string.

---

#### `getThumbnail(width=None, height=None, maxWidth=None, maxHeight=None)`
Returns a rendered thumbnail image. Falls back to a placeholder if none exists.

---

#### `hasThumbnail()`
Checks if a thumbnail is set.

---

#### `make_thumbnail()`
Captures a screenshot from the game and sets it as the playthrough thumbnail (encoded as Base64 UTF-8 string).

---

#### `removeThumbnail()`
Removes the thumbnail from the playthrough.

---

#### `sequentializeSaves()`
Organizes save slots sequentially across pages.

---

### Factories

#### `from_dict(data)`
Creates a `PlaythroughClass` instance from a dictionary.

#### `from_json_string(json_string)`
Creates a `PlaythroughClass` instance from a JSON string.


# Autosaver API Documentation

Here you can find all the functions and actions related to autosaving.

accessed through `JK.api.autosaver`

---

## Terminology

- **Autosave**:  
  Not to be confused with Ren'Py's native autosave — this system performs a **manual save** in numbered pages when a player makes a choice.

- **Active slot**:  
  A `"[page]-[slot]"` string representing the currently targeted slot for autosave or quick save.

---

## Functions

### `set_active_slot(slotname, ignore_large_jump=False)`
Sets the currently active slot for autosaves.

**Args:**
- `slotname (str)`: Ren'Py's `"[page]-[slot]"` formatted slot name.
- `ignore_large_jump (bool)`:  
  If `True`, ignores large page number changes (greater than 1) without showing a confirmation dialog.  
  Useful for games that manually save across distant pages, which could confuse the slot counter.

---

### `get_current_slot()`
Returns the currently active slot (tuple):

- `page (int)`: Page number
- `slot (int)`: Slot number
- `slotname (str)`: The original `"[page]-[slot]"` string

---

### `get_next_slot()`
Returns the next slot based on the page size (tuple):

- `page (int)`
- `slot (int)`
- `slotname (str)`

---

### `use_next_slot()`
Sets the active slot to the next slot.

---

### `perform_autosave(choice_label=None)`
Performs an autosave.

**Args:**
- `choice_label (str, optional)`:  
  The label attached to the choice, which will be stored and shown in the timeline.

---

# Settings API Documentation

Here you can find all the functions and actions related to settings.

accessed through `JK.api.settings`

---

## Functions

### `set_setting(setting_key, value, save=True)`
Sets a specific setting identified by `setting_key` to a given `value`.

**Args:**
- `setting_key (str)`: The key identifying the setting. Possible keys:
  - **Autosave and Quick Save Settings**
    - `"autosaveNotificationEnabled" (bool)`: Whether to show a notification when an autosave is performed.
    - `"autosaveKey" (key)`: Which key toggles autosave.
    - `"quickSaveEnabled" (bool)`: Whether quick save is allowed.
    - `"quickSaveNotificationEnabled" (bool)`: Whether to show a notification when a quick save is performed.
    - `"quickSaveKey" (key)`: Which key triggers quick save.
  - **Custom Save/Load Grid Settings**
    - `"customGridEnabled" (bool)`: Whether to use a custom save/load grid.
    - `"customGridX" (int)`: Number of columns in the grid.
    - `"customGridY" (int)`: Number of rows in the grid.
  - **Screen and Visibility Settings**
    - `"loadScreenName" (list<str>)`: Screens where the load sidepanel should be visible.
    - `"saveScreenName" (list<str>)`: Screens where the save sidepanel should be visible.
  - **Slot and Offset Settings**
    - `"offsetSlotAfterManualSaveIsLoaded" (bool)`: Offset slot after loading a manual save to prevent overwrites.
    - `"offsetSlotAfterManualSave" (bool)`: Offset slot after creating a manual save.
    - `"offsetSlotAfterQuickSave" (bool)`: Offset slot after creating a quick save.
  - **Display and UX Settings**
    - `"sizeAdjustment" (int)`: Adjusts size scaling for different resolutions.
    - `"dialogOpacity" (float)`: Dialog background opacity (0 to 1).
    - `"sidepanelOpacity" (float)`: Sidepanel background opacity (0 to 1).
    - `"paginationOpacity" (float)`: Pagination background opacity (0 to 1).
  - **Key Bindings and Hotkeys**
    - `"changeSidepanelVisibilityKey" (key)`: Key to toggle sidepanel visibility.
    - `"searchPlaythroughKey" (key)`: Key to search a single playthrough.
    - `"searchPlaythroughsKey" (key)`: Key to search across all playthroughs.
  - **Debugging and Updates**
    - `"debugEnabled" (bool)`: Enables or disables debug mode.
    - `"updaterEnabled" (bool)`: Enables or disables the auto-updater.
    - `"noUpdatePrompt" (bool)`: Disables update prompt display (requires `updaterEnabled=True`).
    - `"autoUpdateWithoutPrompt" (bool)`: Automatically update without prompting the user (requires `updaterEnabled=True`).
  - **Pagination and Playthrough UI**
    - `"playthroughsViewMode" ("GRID"|"ROWS")`: Playthroughs view mode.
    - `"paginationQuickSaves" (bool)`: Show Quick Saves button (Q) on pagination.
    - `"paginationAutoSaves" (bool)`: Show Auto Saves button (A) on pagination.
    - `"paginationFirstPage" (bool)`: Show first page button (|<) on pagination.
    - `"paginationLastPage" (bool)`: Show last page button (>|) on pagination.
    - `"paginationBigJump" (bool)`: Show big jump buttons (<< and >>).
    - `"paginationGoTo" (bool)`: Show Go-To button.
    - `"paginationNumbers" (bool)`: Show page numbers.
  - **Advanced Behavior Settings**
    - `"pageFollowsQuickSave" (bool)`: Switch to the quick save's page after saving.
    - `"pageFollowsAutoSave" (bool)`: Switch to the autosave's page after saving.
    - `"autosaveOnSingletonChoice" (bool)`: Autosave even when there's only one visible choice.
    - `"playthroughTemplate" (str)`: Default template for a new playthrough.
    - `"preventAutosavingWhileNotInGame" (bool)`: Prevent autosaving until gameplay starts (at "start" label).
    - `"seamlessPagination" (bool)`: Center active page in pagination.
    - `"sidepanelHorizontal" (bool)`: Display the sidepanel horizontally.
    - `"showConfirmOnLargePageJump" (bool)`: Show confirmation dialog on large page jumps during gameplay.
    - `"preventAutosaveModifierKey" ("SHIFT"|"ALT"|None)`: Modifier key to skip autosaving when held.
    - `"autosaveOnNormalButtonsWithJump" (bool)`: Enable autosave on normal jump buttons.

- `value`:  
  The value to assign, according to the type indicated next to each setting key.

- `save (bool, default=True)`:  
  Whether to save the settings immediately after setting the value.

**Note:**  
If `setting_key` is `"globalizedSettings"`, an exception will be raised.  
Changing which settings are globalized must be left to the player.

---

## Example Usage

```python
JK.api.settings.set_setting("autosaveNotificationEnabled", True, save=False)
JK.api.settings.set_setting("customGridX", 5, save=False)
JK.api.settings.set_setting("dialogOpacity", 0.75)
```

---

### `save()`
Saves the settings into persistent storage and user directory (if available)

---

# Callbacks API Documentation

Here you can find all the available callbacks.
These callbacks allow you to hook into core systems at various points in the mod's flow.

accessed through `JK.api.callbacks`

---

### `new_playthrough_instance_callbacks (list)`

**Description**:  

Called whenever a new playthrough instance is created.

**Use Case**:  

Useful for initializing custom data, tracking analytics, or modifying the new playthrough before it becomes active.

**Example Scenario**:  

You might register a callback to pre-populate `meta` field for every newly created playthrough.

**Code example**:

```python
def __add_metadata(playthrough):
  playthrough.meta = "My metadata"  # This will add "My metadata" to every new playthrough


JK.api.callbacks.new_playthrough_instance_callbacks.append(__add_metadata)
```

---

### `playthroughs_filter_callbacks (list)`

**Description**:  

Called whenever playthroughs are being collected for display, such as on the "Select Playthrough" screen or in the side
panel showing available playthrough counts.

**Use Case**:

Useful for filtering or modifying the list of playthroughs shown to the user.

**Example Scenario**:

You might register a callback to hide certain playthroughs from the standard UI.

**Code example**:
```python
# This filter will allow only playthroughs that have id < 0. There aren't any, but you got the point, right?
def __filter(playthrough):
  return playthrough.id < 0


JK.api.callbacks.playthroughs_filter_callbacks.append(__filter)
```
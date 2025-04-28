![Journey Keeper](/banner.jpg)

# Journey Keeper

[![Static Badge](https://dcbadge.limes.pink/api/server/https://discord.gg/H5SgkKbBE7)](https://discord.gg/H5SgkKbBE7)

**Journey Keeper** (**JK**) is a Ren'Py mod, designed to help you organize saves into distinct playthroughs. Introduces an autosave on choice feature, tracks all choices with a timeline, and offers a variety of tools for save management.
Compatible with all Ren'Py games from version 7 onward, JK ensures you never lose track of your journey, whether you're exploring new routes or revisiting past decisions.

# Table of Contents
1. [Installation](#installation)
2. [First-Time Orientation](#first-time-orientation)
3. [Features](#features)
4. [Troubleshooting](#troubleshooting)
5. [Known Issues](#known-issues)
6. [API](#API)

# Installation
Download the [latest release](https://github.com/Smrdgy/renpy-journey-keeper/releases/latest) right here from GitHub

Copy `JK.rpa` into the `/game` directory of the game you want to play.

*Tip for Windows*:
If you plan to use this mod for multiple games, consider using [Link Shell Extension](https://schinagl.priv.at/nt/hardlinkshellext/linkshellextension.html#download).  
By dragging the `.rpa` file with the right mouse button and selecting `Drop Here > Hardlink` from the context menu, you can store the mod anywhere on your PC and reference it as if it were located in the game's directory.  
This approach enables you to reuse the mod across multiple games, and in the event of an update, update it only once.

# First-time orientation
When you start the game, go to the load screen. You should see a black bar with buttons on the right side -- a sidepanel.
If the sidepanel doesn't appear, check the [Troubleshooting](#troubleshooting) section for the "I can't find the panel" issue.

The sidepanel is the only element added to your field of view by default. From here, you can:
- Select, edit, or create playthroughs.
- Quickly toggle autosaving for the active playthrough.
- Manage active playthrough via specific actions, like:
  - Duplicate playthrough.
  - Manage saves.
  - Show choices timeline.
  - Search playthrough(s).

## Keyboard shortcuts
- `ALT + P` or draw `P` → `Up + Right + Down + Left` on a touch screen
  - Cycles between 3 modes of sidepanel visibility "Visible only on save/load screens" → "Always visible" → "Always hidden".
- `ALT + A`
  - Toggles autosave function (if it can be enabled).
- `F5`
  - Makes a quick save.
- `CTRL + ALT + SHIFT + P`
  - Resets text sizing as well as sidepanel and pagination position.
- `CTRL + F` (save/load screen only)
  - Search in active playthrough.
- `CTRL + SHIFT + F` (save/load screen only)
  - Search in all playthroughs.
- `ALT + [Click on a choice]`
  - Prevents autosaving the choice when autosave is enabled.
- `ESC` / `[Right mouse click]`
  - Exit any dialog

💡 **Note**: All shortcuts can be remapped in the settings, in case of conflicts with the game or another mod.
Additionally, the mappings can be set global via the globe icon button. Meaning, the mapping will apply to all other games as well.
> For example: I'm not using the Ren'Py's native accessibility menu (`A`), so I unchecked ALT on the autosave mapping to simplify the shortcut.

💡 **Also note**: A lot of buttons have underlined letter like: <ins>S</ins>ave. This implies, the button action can be triggered by a combination of `ALT + [that letter]`

You can also unassign the mapping by clicking the circular red X button 

# Features
- 📂 Manage multiple playthroughs, each with its own name, thumbnail, and description—accessible from the save/load screen.
- 💾 Autosave every choice you make, with the ability to view them in a list.
- 🧮 View and manage saves across playthroughs:
  - Copy saves from one playthrough to another.
  - Delete any save from any location.
  - Restructure saves into a sequence.
- 🔢 Use actually working pagination, with go-to a specific page feature
- 🔎 Search playthrough(s) and their save names and choices
- 📚 Import playthroughs from other games (to continue from a previous part/season for example)
- ⚙️ Comprehensive collection of settings to personalize your experience

💡 **Note** Every non-fullscreen element can be dragged around.

### Planned features *(or at least under consideration)*

- Add custom save/load page
- Add more progress bars wherever a time-consuming operation occurs
- Implement system to prevent autosaving when choosing a choice question (a choice that leads back to the same menu the choice was made from)
- Add memories
  - A system to record segments of the gameplay to be replayed at any time. Basically a glorified save and replay in one. No choices, minigames, etc.. Perfect for replaying key moments like 18+ scenes when gallery isn't available.
- Localization
- Improve performance of save picker screens (if it's even possible)
- Colors customization (colorblind accessibility)

# Troubleshooting
ℹ️ If you've encountered an issue, first check the frequently occurring scenarios below for possible solutions. If that doesn't help, feel free to visit our [Discord](https://discord.gg/H5SgkKbBE7) to report it and/or get further help. Alternatively you can submit an issue right here on GitHub. 

💡 Most of these issues arise from the wide diversity of how the games are programmed, so don't be surprised by the recurring pattern of blaming the other developers 😅.

## I can't find the panel
### Scenario A: Wrong save/load names
#### Solution:
1. Press `ALT + P` (or draw `P` -> `Up + Right + Down + Left` on a touch screen) to cycle through the panel's visibility modes.
2. Open settings (⚙️).
3. Navigate to the `Save/Load` section and find `Screens`.
4. Select a screen name that likely represents the save/load screen.
   - Optionally, detach the section using the `Detach from settings` button to preview changes in real time.

#### Reason:
Some game developers rename save/load screens while customizing them, breaking the mod's detection system when it looks for "save"/"load" screen names.

### Scenario B: No independent screens
#### Solution (sort of)
In extreme cases were you are unable to find the save/load screen(s), follow these steps:
1. Press `ALT + P` (or draw `P` -> `Up + Right + Down + Left` on a touch screen) to cycle the sidepanel visibility to "Always visible". 
2. Do what you need to do.
3. Press `ALT + P` (or the touch screen equivalent) again to hide the sidepanel. 

> 💡 **Note** The visibility cycle has 3 modes. In order to bring the sidepanel back again, you will have to repeat the press multiple times.

#### Reason:
So far, in all of my tests, there has only been one game where the developer integrated the save/load screens directly into the game screen, making them impossible to detect.

## UI is too big or too small
The mod was developed with a 1080p resolution in mind. Older games, often using 720p resolution, or newer using 4K may encounter sizing issues.

### Solution:
1. Open settings (⚙️).
2. Navigate to the `Accessibility` section.
3. Adjust the `Size adjustment` value until you find a fitting size.
   - The first "T" represents the native scale, while the second "T" previews the new size.
   - Usually, adjustments in the range of -3 to +3 are sufficient.
4. Click `Click here to apply the new size` to apply the changes.

## The 'A' button in the sidepanel is greyed out, or the `Autosave on choice` option is disabled
### Solution:
1. Count the number of rows and columns in the save/load grid.
2. Open settings (⚙️).
3. Find and enable `Custom slots grid` checkbox under `Save/Load` section.
4. Use the `+` and `-` buttons to match the row and column numbers from step 1.

### Reason:
Custom save/load screens may not follow standard Ren'Py variables, such as `renpy.store.gui.file_slot_cols` and `renpy.store.gui.file_slot_rows`, which the mod uses for calculating the next save slot.

## Autosave is enabled, but it won’t save my choices

### Scenario A: No `start` label

#### Solution:
1. Open settings (⚙️).
2. Go to `Autosave` tab
3. Uncheck `Restrict autosave to in-game only` in the `Advanced` section.

#### Reason:
The mod depends on a very specific moment in the game's lifecycle to prevent saving during menus or age verification prompts.

For instance, some games feature an age check right at the beginning, and the "yes/no" buttons could potentially overwrite the save slot 1-1.

### Scenario B: Custom choice buttons

#### Solution:
1. Open settings (⚙️).
2. Go to the `Autosave` tab
3. Find and enable `Perform autosave on normal buttons` in the `Advanced` section.

#### Reason:
The game uses custom buttons for choices, which the mod cannot detect by default.
To accommodate this, the setting forces an autosave on any button that might be considered a choice.
However, be aware that this may result in false positives, such as free-roam navigation buttons.

**For the curious technically apt users**:
A Button is considered a choice button if it contains the `Jump` action.

## The autosaves are disorganized

### Scenario A: Manual saves performed by the game

#### Solution:
1. Perform a manual save to correct the slot counter and continue from there, until another manual save breaks it again.

#### Reason:
Some games force manual saves during gameplay, disrupting the autosave system. There is nothing that can be done about it, short of manually removing all the save function calls from the game’s code.
However, there is a system that detects when the page number jumps too much (by more than one page) while making a choice. When that happens, you will be prompted to either keep the new page or revert it back.

### Scenario B: Incorrect save grid numbers

#### Solution:
1. Count the number of rows and columns in the save/load grid.
2. Open settings (⚙️).
3. Find and enable `Custom slots grid` checkbox under `Save/Load` section.
4. Use the `+` and `-` buttons to match the row and column numbers from step 1.

#### Reason:
Some games with custom save/load screens may encounter issues if two variables, `renpy.store.gui.file_slot_cols` and `renpy.store.gui.file_slot_rows`, are defined incorrectly. This misconfiguration can confuse the autosave counter, leading saves to either overflow the grid or prematurely jumping to another page.


# Known issues

## “Reload” button on the exception screen crashes the game
~~This issue stems from two file injections that are overwriting standard Ren'Py behavior, specifically: `loadsave.rpy` and `ui.rpy`. Simply re-start the game manually.~~

**This issue should be resolved. If it persists, please report it.**

## Loss of progress
~~There have been rare cases, so far only 2 out of ~100 games, where save values were not stored properly, causing loss of progress and subsequently exceptions.~~~

**This issue should be resolved. If it persists, please report it.**

## Error while saving after an update
~~The mod may throw an error when attempting to autosave after an update. If any code inside the injects directory changes, a full restart of the game is required—reloading isn't enough.
This occurs because the old code from those files remains loaded when the game reloads itself.~~

**This issue should be resolved. If it persists, please report it.**

## Game error
```
I'm sorry, but an uncaught exception occurred.

While running game code:
  File "game/JK/src/classes/playthroughs/Playthroughs.rpy", line 342, in call
  File "game/JK/src/injects/loadsave.rpy", line 34, in new_funct
PicklingError: Can't pickle [some function]: it's not the same object as renpy.[something]
```
This, or very similar error, is not necessarily related to this mod.
Despite the trace, it only indicates that something has happened during saving/loading, which this mod "hijacks" in order to detect when user performed save/load.
The issue is most likely with other mod or the game itself.

# License 
In a nutshell (not legally binding):

- ✅ You can use this software for personal or internal use.
- ✅ You can modify it and share your modified versions. Fork away! Just leave me a little credit somewhere, okay?
- 🚫 You cannot redistribute the original, unmodified version. **Unless it's bundled with a game.**
- 🚫 You cannot sell or commercially use this software or its derivatives, **except when bundled as part of a commercialized game.**

Please refer to the full license below for legally binding terms.

[Full license](LICENSE)

# Disclaimer

This mod is provided as-is and is not officially supported by the game developers nor the engine developers. Use at your own risk.
Installing or using this mod may result in unintended behavior, including but not limited to game crashes, corrupted save files, or loss of progress.
It is strongly recommended that you back up your save data before installing.
The mod creator is not responsible for any damage or data loss caused by the use of this mod.

# API

Full API documentation can be found [here](src/api/API.md)

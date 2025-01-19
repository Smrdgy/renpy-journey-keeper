# TODO: Add header image 

# Journey Keeper (JK)

**Journey Keeper (JK)** is a universal Ren'Py mod designed to manage saves across multiple playthroughs.

---

# Table of Contents
1. [Install](#install)
2. [First-Time Orientation](#first-time-orientation)
3. [Features](#features)
5. [Troubleshooting](#troubleshooting)
6. [Known Issues](#known-issues)

# Install
Copy `JK.rpa` into the `/game` directory of the game you want to play.

*Tip for Windows*:
If you plan to use this mod for multiple games, consider using [Link Shell Extension](https://schinagl.priv.at/nt/hardlinkshellext/linkshellextension.html).  
By dragging the `.rpa` file with the right mouse button and selecting `Drop Here > Hardlink` from the context menu, you can store the mod anywhere on your PC and reference it as if it were located in the game's directory.  
This approach allows you to reuse the mod across games and update only once.

---

# First-time orientation
When you start the game, go to the load screen. You should see a black bar with buttons on the right side -- a sidepanel.
If the sidepanel doesn't appear, check the [Troubleshooting](#troubleshooting) section for the "I can't find the panel" issue.

The sidepanel is the only element added to your field of view. From here, you can:
- Select, edit, or create playthroughs.
- View created memories (*WIP*).
- Toggle autosaving quickly.
- Manage active playthrough via specific actions, like:
  - Duplicate playthrough.
  - Manage saves.
  - Show choices timeline.

## Key shortcuts
- `ALT + P` or draw `P` → `Up + Right + Down + Left` on a touch screen
  - Cycles between 3 modes of sidepanel visibility "visible only on save/load screens" → "Always visible" → "Always hidden"
- `ALT + A`
  - Toggles autosave function (if it can be enabled)
- `F5`
  - Makes a quick save
- ` (Backtick)
  - Saves memory
- `CTRL + ALT + SHIFT + P`
  - Resets text sizing and sidepanel and pagination position

**Note**: All shortcuts can be remapped in the settings in case of conflicts with the game or another mod.
Additionally, the mappings can be set global via the globe icon button, meaning, the mapping will apply to all other games as well.
> For example, I'm not using the Ren'Py's native accessibility menu (`A`), so I unchecked ALT on the autosave mapping to simplify the shortcut.

You can also unassign the mapping by clicking the circular red X button 

---

# Features
- Manage multiple playthroughs, each with its own name, thumbnail, and description—accessible from the save/load screen.
- Autosave every choice you make, with the ability to view them in a list.
- View and manage saves across playthroughs:
  - Copy saves from one playthrough to another.
  - Delete any save from any location.
  - Restructure saves into a sequence.
- Use actually working pagination, with go-to a specific page feature
- Create memories (*WIP*).

**Note:**  
Memories are an experimental feature. Until I figure out how to store a sequence of events, a "memory" will be just a glorified save.

---

### Planned features *(or at least under consideration)*

- Complete memories
- Add custom save/load page

---

# Troubleshooting
Most of these issues stem from the vast diversity of how the games are programmed, so don't be surprised about the repeated pattern of the blame.

## I can't find the panel
### Scenario A:
#### Solution:
1. Press `ALT + P` (or draw `P` -> `Up + Right + Down + Left` on a touch screen) to cycle through the panel's visibility modes.
2. Open settings (⚙️).
3. Navigate to the `Save/Load` section and find `Screens`.
4. Select a screen name that likely represents the save/load screen.
   - Optionally, detach the section using the `Detach from settings` button to preview changes in real time.

#### Reason:
Some game developers rename save/load screens while customizing them, breaking the mod's detection system when it looks for "save"/"load" screen names.

---

### Scenario B:
#### Solution
In extreme cases, were you are unable to find the save/load screen(s), you'll have to:
1. Use `ALT + P` to toggle the sidepanel visibility to always visible. 
2. Do what you need to do.
3. Use again `ALT + P` to hide the sidepanel.

#### Reason:
So far, in all my tests, there have been only one game, where the dev decided to include the save/load screens directly into the game screen, which made them undetectable.

---

## UI is too big or too small
The mod was developed with a 1080p resolution in mind. Older games, often using 720p resolution, may encounter sizing issues.

### Solution:
1. Open settings (⚙️).
2. Navigate to the `Accessibility` section.
3. Adjust the `Size adjustment` value until you find a fitting size.
   - The first "T" represents the native scale, while the second "T" previews the new size.
   - Usually, adjustments in the range of -3 to +3 are sufficient.
4. Click `Click here to apply the new size` to apply the changes.

---

## The 'A' button in the sidepanel is greyed out, or the `Autosave on choice` option is disabled
### Solution:
1. Count the number of rows and columns in the save/load grid.
2. Open settings (⚙️).
3. Find `Custom slots grid` checkbox under `Save/Load` section.
4. Use the `+` and `-` buttons to match the row and column numbers from step 1.

### Reason:
Custom save/load screens may not follow standard Ren'Py variables, such as `renpy.store.gui.file_slot_cols` and `renpy.store.gui.file_slot_rows`, which the mod uses for calculating the next save slot.

---

## Autosave is enabled, but it won’t save my choices

### Scenario A: No `start` label

#### Solution:
1. Open settings (⚙️).
2. Uncheck “Restrict autosave to in-game only” under `Advanced` in the `Autosave` section.

#### Reason:
The mod relies on a very specific moment in the game’s lifetime to avoid saving during menus or age verification prompts.

For example, some games have an age check at the very start of the game and the yes/no buttons might overwrite save 1-1.

### Scenario B: Custom choice buttons

#### Solution:
Cannot be fixed.

#### Reason:
The game uses custom buttons for choices, which the mod cannot detect.

---

# Known issues

## “Reload” button on the exception screen crashes the game
This issue stems from `loadsave.rpy` and `ui.rpy` injections. Simply re-start the game manually.

---

## Loss of progress
There have been rare cases, so far only 2 out of ~100, where save values were not stored or loaded properly, causing loss of progress and/or exceptions.

**This issue should be resolved. If it persists, please report it.**

----

## The autosaves are disorganized
Some games force manual saves during gameplay, disrupting the autosave system. There is nothing that can be done about it, short of manually removing all the save function calls from the game’s code.
As a silver lining, when you come across this behavior, you can perform a manual save to correct the slot counter and continue from there, until another manual save breaks it agan.

---

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
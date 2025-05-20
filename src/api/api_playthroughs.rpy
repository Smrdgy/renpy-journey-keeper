init 1 python in JK.api.playthroughs:
    """
    Here you can find all the functions and actions related to the playthroughs

    Terminology:
        playthrough: A `PlaythroughClass` instance representing a collection of saves.
        
        activation: A process that changes save directories and refreshes save/load screens with saves from a specific playthrough.
        
        id: A numerical unique identifier. Currently, IDs 1 and 2 are reserved, as well as any numbers beyond approximately 1,730,000,000 (which come from a timestamp using `time.time()`).
        
        [something]Action: Represents a class inheriting from `renpy.ui.Action` that can be called directly in the script without triggering immediately. Useful for buttons and key actions.
        
        autosave: Unlike Ren'Py's native autosaves, these saves are stored directly into numbered pages and store which choice was made.
        
        quick save: Unlike Ren'Py's native quick saves, these saves are stored directly into numbered pages. (Default: triggered by pressing F5.)
    """

    JK = renpy.exports.store.JK
    
    def list_all():
        """ Returns a list of all playthroughs """
        return JK.Playthroughs.playthroughs

    def list_all_filtered(additional_filter_callback=None, include_hidden=False):
        """
        Returns a list of all playthroughs that pass all the conditions set by filters and are not hidden (unless `include_hidden` is set to True)
        Results are going to be affected by these callback functions:
            - additional_filter_callback
            - JK.api.callbacks.playthroughs_filter_callbacks

        Args:
            additional_filter_callback (Callable[[PlaythroughClass], bool]?): If defined, this function must return either True or False, otherwise you'll get an exception.
            include_hidden (bool?): By default, hidden playthroughs are filtered out, if True, they will be included.

        Example:
            a = JK.api.playthroughs.create_playthrough_instance(name="A")
            b = JK.api.playthroughs.create_playthrough_instance(name="B", hidden=True)
            c = JK.api.playthroughs.create_playthrough_instance(name="C")

            JK.api.playthroughs.add(a, activate=False, save=False, restart_interaction=False)
            JK.api.playthroughs.add(b, activate=False, save=False, restart_interaction=False)
            JK.api.playthroughs.add(c)

            print(JK.api.playthroughs.list_all_filtered()) # -> [a, c]
            print(JK.api.playthroughs.list_all_filtered(include_hidden=True)) # -> [a, b, c]
            print(JK.api.playthroughs.list_all_filtered(lambda playthrough: not playthrough.name == "C")) # -> [c]

            JK.api.callbacks.playthroughs_filter_callbacks.append(lambda p: p.name == "A")
            print(JK.api.playthroughs.list_all_filtered(lambda playthrough: not playthrough.name == "C")) # -> []
        """
        return JK.Playthroughs.get_filtered_playthroughs(additional_filter_callback=additional_filter_callback, include_hidden=include_hidden)

    def get_active():
        """ Returns currently active playthrough. If there is none, the native playthrough is returned. """
        return JK.Playthroughs.active_playthrough

    def get_by_name(name):
        """
        Returns playthrough by its name or None, if not found.

        Args:
            name (str): Name of the playthrough

        Returns:
            PlaythroughClass: If found a match
            None: If not found
        """
        return JK.Playthroughs.get(name)

    def get_by_id(id):
        """
        Returns playthrough by its ID or None, if not found.

        Args:
            id (int)

        Returns:
            PlaythroughClass: If found a match
            None: If not found
        """
        return JK.Playthroughs.get_by_id(id)

    def get_index_by_id(id):
        """
        Returns playthrough index by its ID or -1, if not found.
        
        Args:
            id (int)

        Returns:
            int: Match index
            -1: If none found
        """
        return JK.Playthroughs.get_index_by_id(id)

    def add(playthrough, activate=True, save=True, restart_interaction=True, i_know_what_i_am_doing_with_the_name_so_skip_the_check=False):
        """
        Adds a playthrough instance to the playthroughs

        Args:
            playthrough (PlaythroughClass): A playthrough class instance
            activate (bool): Whether to automatically activate this playthrough.
            save (bool): Whether to save the playthroughs into the persistent storage (if false, you have to manually perform save() ortherwise the playthroughs might be lost when the game quits!)
            restart_interaction (bool): Whether to perform restart_interaction when the playthrough is added, it is advised to turn this off when adding multiple playthroughs at the same time.
            i_know_what_i_am_doing_with_the_name_so_skip_the_check (bool): A safety override for those who like to live dangerously. If set to True, it will skip the `name` check and add the playthrough regardless of any conflicting names that already exist. ⚠️ If you choose to do this, make absolutely sure you have set the `directory` on the playthrough instance! ⚠️

        Returns:
            PlaythroughClass: The same instance that was provided; good for chaining.
        """

        if not i_know_what_i_am_doing_with_the_name_so_skip_the_check and not JK.Playthroughs.is_valid_name(playthrough.name):
            raise Exception("Playthrough name \"{}\" already exists.".format(playthrough.name))

        return JK.Playthroughs.add(playthrough=playthrough, activate=activate, save=save, restart_interaction=restart_interaction)

    def edit(original, other, allow_moving_save_directory=False):
        """
        Edits original playthrough with data from a the other one

        Args:
            original (PlaythroughClass): Reference to the original playthrough (This playthrough won't be replaced, only the data will)
            other (PlaythoughClass): Reference to a playthrough with new data (This playthrough will then be discarded)
            allow_moving_save_directory (bool): Whether to allow moving the save directory if the name of the playthrough doesn't match with the original playthrough (works only with edit).

        Returns:
            PlaythroughClass: Returns the original playthrough with new data
        """
        return JK.Playthroughs.edit(playthrough=other, originalPlaythrough=original, moveSaveDirectory=allow_moving_save_directory)

    def add_or_edit(playthrough, allow_moving_save_directory=False, force=False):
        """
        Adds a new playthrough if it didn't exist befofe based on the ID, or edits data of the existing one.

        Args:
            playthrough (PlaythroughClass): Reference to the playthrough that is supposed to be added or have a new data for edit.
            allow_moving_save_directory (bool): Whether to allow moving the save directory if the name of the playthrough doesn't match with the original playthrough (works only with edit).
            force (bool): Whether to ignore all errors during the chaning of the saves directory and forcibly overwrite any conflicts.
        """

        return JK.Playthroughs.add_or_edit(playthrough=playthrough, moveSaveDirectory=allow_moving_save_directory, force=force)

    def remove_by_id(id, delete_save_files=False, keep_active=False):
        """
        Remove a playthrough by ID

        Args:
            id (int)
            delete_save_files (bool): Whether to delete all the save files related to this playthrough from the machine.

        Returns:
            bool: Status whether it removed something. It will be False if no playthrough was found.
        """
        return JK.Playthroughs.remove(id, delete_save_files=delete_save_files)

    def toggle_autosave_on_choice_for_active():
        """
        Toggles the "Autosave on choice" feature for currently active playthrough.
        """

        JK.Playthroughs.toggle_autosave_on_choices_for_active()

    def set_autosave_on_choice_for_active(enabled):
        """
        Sets the "Autosave on choice" feature for currently active playthrough.
        """

        JK.Playthroughs.set_autosave_on_choices_for_active(enabled=enabled)

    def activate_by_name(name):
        """
        Activates playthrough by name
        
        Args:
            name (str)
        """
        JK.Playthroughs.activate_by_name(playthroughName=name)
    
    def activate_by_id(id):
        """
        Activates playthrough by ID
        
        Args:
            id (int)
        """
        JK.Playthroughs.activate_by_id(playthroughID=id)
    
    def activate_by_instance(playthrough):
        """
        Activates playthrough by instance

        Args:
            playthrough (PlaythroughClass)
        """
        JK.Playthroughs.activate_by_instance(playthrough=playthrough)
    
    def activate_native():
        """ Activates native playthrough (#1) """
        JK.Playthroughs.activate_native()
    
    def activate_first():
        """ Activates first playthrough (Most of the time, that is Native playthrough, but the order is changeable by the player.)  """
        JK.Playthroughs.activate_first()
    
    def save():
        """ Performs save of all playthroughs into the persistent storage and user directory (if available) """
        JK.Playthroughs.save()

    def is_name_available(name):
        """
        Returns whether the name is not already in use by another playthrough

        Args:
            name (str)

        Returns:
            bool: True = is available; False = already in use
        """

        return JK.Playthroughs.is_valid_name(name=name)

    def get_encoded_thumbnail():
        """
        Returns base64 UTF-8 encoded thumbnail ready to be stored.
        Useful when you want to make your own playthrough with a thumbnail programatically.
        ⚠️ Just make sure to not call this in a console or print into it. Console can't handle the amount of text and will crash! ⚠️
        If that happens, you have to clear the persistent storage...

        Returns:
            str: Encoded image
        """

        return JK.PlaythroughClass().make_thumbnail().thumbnail

    def output_encoded_thumbnail_into_file(filename="thumbnail.txt"):
        """
        Outputs the encoded thumbnail into a file (duh).
        Unlike `get_encoded_thumbnail()`, this is console-safe and requires no additional code to get the thumbnail.
        """

        thumbnail = get_encoded_thumbnail()
        file_path = renpy.os.path.join(renpy.config.basedir, filename)
        with open(file_path, "w") as f:
            f.write(thumbnail)
            f.close()

        print("Thumbnail created at:", file_path, "\nAttempting to open the directory...")
        JK.OpenDirectoryAction(renpy.config.basedir)()

    """
    Toggles the "Autosave on choice" feature for currently active playthrough.
    Works the same as toggle_autosave_on_choice_for_active, but this is in a form of an action, so you can simply use it as a button or a key action. It also performs this asynchronously, to avoid stutter when toggling.
    """
    ToggleAutosaveOnChoiceForActiveAction = JK.Playthroughs.ToggleAutosaveOnChoicesForActiveAction

    """
    Performs a quick save action.
    """
    PerformQuickSaveAction = JK.Playthroughs.QuickSaveAction

    def create_playthrough_instance(
        name,
        id=None,
        directory=None,
        description=None,
        thumbnail=None,
        autosave_on_choice=True,
        use_choice_label_as_save_name=False,
        enabled_save_locations=None,
        meta=None,
        native=False,
        directory_immovable=False,
        hidden=False,
        serializable=True,
        deletable=True
        #MODIFY HERE
    ):
        """
        Creates a playthrough instance

        Args:
            name (str): Name of the playthrough [REQUIRED]
            id (int): ID of the playthrough. Can be left None and will be autofilled by current a timestamp using `time.time()`
            directory (str): Name of the directory where this playthrough is going to store saves. When None, the directory will be autofilled from `name`
            description (str): A description of the playthrough the player can read.
            thumbnail (str): UTF-8 - base64 encoded renpy screenshot (@see get_encoded_thumbnail)
            autosave_on_choice (bool): Whether to use "Autosave on choice" feature
            use_choice_label_as_save_name (bool): Whether to enable storing choice label as a save name
            enabled_save_locations (list<"USER"|"GAME"|str>|None):
                list:
                    A list of enabled save location on the system.
                    ⚠️ Not every option is available in every OS, for example MacOS apps can't store saves in "/game/saves", so "GAME" will be ignored.

                    "USER" - user directory - %appdata% on Windows, Library on Mac, etc.
                    "GAME" - /game/saves directory
                    str - Any full path route the game uses

                None:
                    All of the above enabled
            meta (anything JSON serializable): Optional metadata associated with the playthrough. It can be any type you wish, as long as it's JSON serializable.
            native (bool): Marks the playthrough as a built-in or system-level playthrough.
            directory_immovable (bool): Prevents the playthrough's saves directory from being moved or renamed.
            hidden (bool): Hides the playthrough from standard user interfaces.
            serializable (bool): Controls whether the playthrough should be saved to persistent storage.
            deletable (bool): Determines whether the playthrough can be deleted by the player or system.

        Returns:
            PlaythroughClass: The newly created playthrough instance
        """

        if not name:
            raise Exception("\"name\" is required")

        return JK.PlaythroughClass(id=id, directory=directory, name=name, description=description, thumbnail=thumbnail, autosaveOnChoices=autosave_on_choice, useChoiceLabelAsSaveName=use_choice_label_as_save_name, enabledSaveLocations=enabled_save_locations)#MODIFY HERE
# Unfortunately this must be saved into the save game, so the system can properly recognize which slot to use next,
# especially when a manual save is made somewhere in between and then a rollback occurs.
default JK_ActiveSlot = "1-1"

init python in JK:
    _constant = True

    import time
    from json import dumps as json_dumps
    import io
    import sys
    import re
    import pygame_sdl2 as pygame

    before_storing_choice_text_callbacks = []

    class AutosaverClass(x52NonPicklable):
        def __init__(self):
            self.suppress_autosave_confirm = False
            self.pending_save = None
            self.prev_active_slot = "N/A"
            self.slot_before_load = "N/A"
            self.confirm_dialog_opened = False
            self.after_load_save_position_pending = False
            self.active_slot_pending = None
            self.prevent_autosaving = Settings.preventAutosavingWhileNotInGame
            self.loaded_manual_save_without_choices = False
            self.prevent_confirm_on_large_page_jump = False

        def set_active_slot(self, slotname, ignore_large_jump=False):
            page, slot = Utils.split_slotname(slotname)

            #Last resort check to counter forced autosaves screwing up the counter (e.g. $ renpy.save("auto-1") somewhere in the dialog)
            if page != 0 and slot != 0:
                self.prev_active_slot = renpy.store.JK_ActiveSlot + "" # Copy the data, not just the pointer
                renpy.store.JK_ActiveSlot = slotname

                if self.prevent_confirm_on_large_page_jump:
                    self.prevent_confirm_on_large_page_jump = False

                elif not ignore_large_jump:
                    prev_page, _ = Utils.split_slotname(self.prev_active_slot)

                    if Settings.showConfirmOnLargePageJump and not Utils.is_save_load_screen() and (prev_page > page + 1 or prev_page < page - 1):
                        showConfirm(
                            title="Page number jumped unexpectedly too far",
                            message="The page jumped from {} to {}.\nIs this correct?".format(prev_page, page),
                            yes_text="Yes, keep the change",
                            no_text="No, revert it",
                            no=Autosaver.RevertActiveSlotAction(self.prev_active_slot)
                        )

        def get_next_slot(self):
            page, slot = Utils.split_slotname(renpy.store.JK_ActiveSlot)

            slot += 1

            if slot > Utils.get_last_slot_number_for_page(page):
                page += 1
                slot = Utils.get_first_slot_number_for_page(page)

            slotString = Utils.make_slotname(page, slot)

            return page, slot, slotString

        def get_current_slot(self):
            slotString = renpy.store.JK_ActiveSlot
            page, slot = Utils.split_slotname(slotString)

            return page, slot, slotString

        def set_next_slot(self):
            _, _, slotString = Autosaver.get_next_slot()
            self.set_active_slot(slotString)

        def try_save_pending_save(self):
            if self.pending_save:
                # If the save slot is not bigger than the very last one, do once a confirm whether to disable autosaving
                if renpy.scan_saved_game(Utils.format_slotname(renpy.store.JK_ActiveSlot)) and not self.suppress_autosave_confirm and (self.loaded_manual_save_without_choices or renpy.store.JK_ActiveSlot != self.prev_active_slot):
                    self.confirm_dialog_opened = True
                    if renpy.get_skipping():
                        if hasattr(renpy, "stop_skipping"):
                            renpy.stop_skipping()
                        elif hasattr(renpy, "skip"):
                            renpy.skip(False)
                    renpy.show_screen("JK_AutosaveOverwriteConfirm")
                    return

                self.pending_save.save()

        def __describe_node(self, node):#Debug
            if node is None:
                return "None"
            try:
                return "{} @ {}:{}".format(type(node).__name__, node.filename, node.linenumber)
            except Exception:
                return repr(node)

        # Static, bounded-depth prediction of whether a choice leads back to the same menu.
        #  Python blocks are treated as transparent pass-throughs (mirroring Ren'Py's own Python.scry(),
        #  which does the same) instead of aborting detection, since a single `$` line used to make every
        #  choice past it look save-worthy.
        #  `If` is evaluated exactly like the real interpreter evaluates it (renpy.python.py_eval per entry,
        #  first true condition wins, falls through to the merge point if none match - see ast.py's own
        #  If.execute()). This is needed because menus are often gated directly behind a condition
        #  (e.g. `if char_available: menu: ...`), so skipping over an `If` blindly would jump clean past
        #  the very menu we're trying to detect a loop back to.
        #  `Call` is treated the same way: since a callee that doesn't escape via jump always returns to the
        #  statement right after the call, jumping straight to that return site (instead of recursing into the
        #  callee) gets the same result almost all of the time for a fraction of the cost.
        def __is_question(self, choice=None, node=None):
            debug = Settings.debugEnabled#Debug
            try:
                i = 0
                resolved_nodes = []

                if choice:
                    if debug:#Debug
                        print(choice.location)#Debug
                    menu_node = renpy.game.script.lookup(choice.location)
                    choice_item = menu_node.items[choice.value]
                    if len(choice_item) > 2 and choice_item[2]:
                        node = choice_item[2][0]
                    else:
                        node = None

                    resolved_nodes = [menu_node]

                    if debug:#Debug
                        print("[JK] is_question: menu={} choice_index={} start={}".format(#Debug
                            self.__describe_node(menu_node), choice.value, self.__describe_node(node)))#Debug
                elif debug:#Debug
                    print("[JK] is_question: start={} (no choice, called from a raw node)".format(self.__describe_node(node)))#Debug

                prediction_depth = 0
                while node and prediction_depth < 2:
                    if debug:#Debug
                        print("[JK] is_question step={} depth={} node={}".format(i, prediction_depth, self.__describe_node(node)))#Debug

                    if node in resolved_nodes:
                        if debug:#Debug
                            renpy.notify("Already resolved")#Debug
                            print("[JK] is_question: node already visited in this walk -> True (question)")#Debug
                        return True

                    resolved_nodes.append(node)

                    if isinstance(node, renpy.ast.Python) and hasattr(node, 'code') and hasattr(node.code, 'source'):
                        is_inert = node.code.source.startswith('renpy.pause(') or node.code.source.startswith('ui.')

                        if debug:#Debug
                            print("[JK] is_question: python inert={} source={!r}".format(is_inert, node.code.source))#Debug

                        # Kept in case a game/engine fork ever puts an `expression` on a Python node - harmless as-is since it's hasattr-gated.
                        if not is_inert and hasattr(node, "expression") and node.expression is not None:
                            if bool(node.expression) == node.expression or renpy.python.py_eval(node.expression):
                                if debug:#Debug
                                    renpy.notify("Expression evaluated to False")#Debug
                                    print("[JK] is_question: python node has a truthy `expression` -> False (save-worthy)")#Debug
                                return False

                        node = node.next

                    elif isinstance(node, renpy.ast.If):
                        matched = False

                        for condition, block in node.entries:
                            condition_result = renpy.python.py_eval(condition)

                            if debug:#Debug
                                print("[JK] is_question: if condition {!r} -> {}".format(condition, condition_result))#Debug

                            if condition_result:
                                node = block[0]
                                matched = True
                                break

                        if not matched:
                            if debug:#Debug
                                print("[JK] is_question: if - no condition matched, falling to merge point {}".format(self.__describe_node(node.next)))#Debug
                            node = node.next

                    elif isinstance(node, renpy.ast.Call):
                        if debug:#Debug
                            print("[JK] is_question: call expression={} label={!r} -> resuming at return site {}".format(#Debug
                                node.expression, node.label, self.__describe_node(node.next)))#Debug

                        node = node.next

                    elif isinstance(node, renpy.ast.Jump):
                            prediction_depth += 1

                            prediction = node.predict()

                            if debug:#Debug
                                print("[JK] is_question: jump expression={} target={!r} -> resolved={}".format(#Debug
                                    node.expression, node.target, self.__describe_node(prediction[0]) if prediction else "unresolved (dynamic target)"))#Debug

                            if len(prediction) > 0:
                                node = prediction[0]
                            else:
                                node = node.next
                    else:
                        node = node.next

                    i += 1

                    if i > 1000:
                        raise Exception("Autosaver.__is_choice_question() infinite loop prevented. Or just reeeeeally long code stack...")
            except Exception as e:
                print(e)

                if Settings.debugEnabled:
                    renpy.notify(str(e))

            if debug:#Debug
                renpy.notify("End")#Debug
                print("[JK] is_question: walk ended without revisiting the menu -> False (save-worthy)")#Debug
            return False

        def _assert_can_autosave(self):
            # Prevent making any autosave actions when the feature is disabled
            if not Playthroughs.active_playthrough.autosaveOnChoices:
                raise Exception("Autosaver is disabled in the current playthrough.")

            # Prevent when forcefully disabled
            if self.prevent_autosaving:
                raise Exception("Autosaver is forcefully disabled.")

            # Prevent a single choice from saving multiple times (debouncer)
            if self.pending_save:
                raise Exception("Autosaver is already saving a choice.")

            # Prevent when viewing a replay or a memory
            if Memories.memoryInProgress or renpy.store._in_replay:
                raise Exception("Autosaver is disabled while viewing a memory or a replay.")

            # Prevent for as long as the Autocomplete banner is present, paused or not - not
            # just while it's actively replaying. It already runs the real ChoiceReturn/Jump
            # action for each choice it replays (see AutocompleteClass.__try_resolve_menu),
            # so this would fire redundantly for those regardless. And while paused, whatever
            # the player clicks to resolve the interruption manually isn't part of the
            # recorded sequence being replayed - autosaving it would mix an unplanned choice
            # into that playthrough's history rather than leaving it for the player's own
            # manual/quick save to capture, same as it would be disabled entirely if this
            # were a genuine memory/replay.
            if Autocomplete.active:
                raise Exception("Autosaver is disabled while Autocomplete is active.")

            # Prevent when singleton choice is detected and not allowed
            if not Settings.autosaveOnSingletonChoice and not Utils.is_displaying_multiple_choices():
                raise Exception("Autosaver is disabled when displaying a single choice.")

            # Prevent making autosave when prevent modifier (SHIFT/ALT) is held
            if Settings.preventAutosaveModifierKey:
                key_mods = pygame.key.get_mods()

                if key_mods and (
                    (Settings.preventAutosaveModifierKey == "ALT" and key_mods & (pygame.KMOD_ALT | pygame.KMOD_META)) or
                    (Settings.preventAutosaveModifierKey == "SHIFT" and key_mods & pygame.KMOD_SHIFT)
                ):
                    raise Exception("Autosaver is disabled when the prevent autosave modifier key is held down.")

            return True

        def handle_any_button_click(self, button):
            # Make sure the autosave can be performed
            try:
                self._assert_can_autosave()
            except Exception as e:
                if Settings.debugEnabled:
                    renpy.notify(str(e))
                return

            # Retrieve label

            if isinstance(button, renpy.display.behavior.Button):
                if isinstance(button.child, renpy.text.text.Text):
                    # Processes the label as Ren'Py would to remove any possible substitutions via [...] e.g. [player_name]
                    text_component = renpy.ui.text(button.child.text)
                    choice_text = Utils.escape_renpy_reserved_characters(' '.join(text_component.text))

                    self.create_pending_save_from_generic_button(button, choice_text)
                else:
                    self.create_pending_save_from_generic_button(button)

            elif isinstance(button, renpy.display.behavior.ImageButton):
                    self.create_pending_save_from_generic_button(button)

            elif isinstance(button, renpy.display.behavior.TextButton):
                self.create_pending_save_from_generic_button(button)

        def create_pending_save_from_generic_button(self, button, label=None):
            node = button.action.node

            # If "autosave on question" is disabled, make sure the jump at then end of the choice doesn't lead back to JK_LastLabel
            if not Settings.autosaveOnQuestion and node:
                if self.__is_question(node=node):
                    return

            self.create_pending_save(label)

        def handle_choice_selection(self, choice):
            # Make sure the autosave can be performed
            try:
                self._assert_can_autosave()
            except Exception as e:
                if Settings.debugEnabled:
                    renpy.notify(str(e))
                return

            # If "autosave on question" is disabled, make sure the jump at then end of the choice doesn't lead back to JK_LastLabel
            if not Settings.autosaveOnQuestion:
                if self.__is_question(choice=choice):
                    return

            self.create_pending_save_from_choice(choice)

        def create_pending_save_from_choice(self, choice):
            choice_text = Utils.derive_choice_text(choice.label)

            original_choice_text = choice_text
            for callback in before_storing_choice_text_callbacks:
                choice_text = callback(choice_text, original_choice_text, choice) or choice_text

            self.create_pending_save(choice_text)

        # The JK_ActiveSlot always equals the slot that was loaded because the saves are made right before selecting a choice for easy re-choicing.
        #  However when a manual save is loaded it might not be a choice screen.
        #  If so, the save slot needs to move further as to not override the manual slot with the next autosave.
        def process_slot_after_load(self):
            self.loaded_manual_save_without_choices = False

            if not Utils.is_displaying_choices():
                if Settings.offsetSlotAfterManualSaveIsLoaded:
                    self.set_next_slot()

                self.loaded_manual_save_without_choices = True

            self.after_load_save_position_pending = False

        def create_pending_save(self, choice):
            self.pending_save = AutosaverClass.PendingSaveClass(choice)
            self.pending_save.early_save()

            # Debouncer
            # Some games, call the choice action twice, example:
            # `action [SensitiveIf( i.action), SetVariable("timeout", 8), SetVariable("timeout_label", None), i.action]`
            #
            # This results in duplicate saves. By using multithreading and introducing a very short delay,  
            # we ensure that the second call is ignored.

            callback = self.try_save_pending_save

            def worker():
                time.sleep(0.01)
                if callable(callback):
                    callback()  # Call the function on the main thread

            renpy.invoke_in_thread(worker)

        class ConfirmDialogSaveAction(renpy.ui.Action):
            def __call__(self):
                Autosaver.suppress_autosave_confirm = True

                if(Autosaver.pending_save != None):
                    Autosaver.pending_save.save()

        class ConfirmDialogCloseAction(renpy.ui.Action):
            def __call__(self):
                Autosaver.confirm_dialog_opened = False
                Autosaver.pending_save = None
                Autosaver.loaded_manual_save_without_choices = False

        class MoveOneSlotOverAction(renpy.ui.Action):
            def __call__(self):
                Autosaver.set_next_slot()

        class TrySavePendingSaveAction(renpy.ui.Action):
            def __call__(self):
                Autosaver.try_save_pending_save()
                renpy.restart_interaction()

        class RevertActiveSlotAction(renpy.ui.Action):
            def __init__(self, prev_slot):
                self.prev_slot = prev_slot

            def __call__(self):
                Autosaver.prevent_confirm_on_large_page_jump = True

                new_slot = self.prev_slot

                Autosaver.set_active_slot(new_slot)
                renpy.notify("Active slot reverted back to {}".format(new_slot))

        class PendingSaveClass(x52NonPicklable):
            temp_save_slotname = "JK-temp-autosave"

            def __init__(self, choice):
                self.choice = choice
                self.async_handle = None

                # Never, EVER call any saving functions from here!!!!!!!!!!!!!!!!!!!!!!!!!
                # I, an idiot, have made this mistake twice,
                # leading to an hour of debugging why, in the ever-loving f***, Autosaver.pending_save is None.
                # (The instance is in the process of being constructed, including calling functions that were trying to access this instance,
                # and the assignment happens afterward...)

            def early_save(self):
                extra_info = ''
                if Playthroughs.active_playthrough.useChoiceLabelAsSaveName:
                    extra_info = self.choice

                # Capturing the screenshot pixels and freezing/pickling the game state must
                # happen synchronously, right now, to reflect the exact moment of this choice.
                # The slow parts (PNG encode, zip compression, writing to every active save
                # location) don't depend on further game state, so AsyncSave defers those to
                # a background thread instead of blocking the interaction.
                self.async_handle = AsyncSave.begin(
                    location=SaveSystem.multilocation,
                    slotname=self.temp_save_slotname,
                    extra_info=extra_info,
                )

            def save(self):
                if self.async_handle is not None:
                    finished = self.async_handle.wait(AsyncSave.DEFAULT_WAIT_TIMEOUT)

                    if not finished or self.async_handle.error:
                        print("[JK] Autosave: pending write to '{}' did not complete successfully ({}).".format(
                            self.temp_save_slotname, self.async_handle.error))
                        renpy.notify("Autosave failed. Check log.txt for more info.")

                        Autosaver.pending_save = None
                        Autosaver.loaded_manual_save_without_choices = False
                        return

                slotname = Utils.format_slotname(renpy.store.JK_ActiveSlot)

                renpy.rename_save(self.temp_save_slotname, slotname)

                if Settings.autosaveNotificationEnabled:
                    renpy.notify("Autosave created at {}".format(slotname))

                Autosaver.pending_save = None
                Autosaver.loaded_manual_save_without_choices = False

                if Settings.pageFollowsAutoSave:
                    page, _, _ = Autosaver.get_current_slot()
                    renpy.store.persistent._file_page = str(page)

                Autosaver.set_next_slot()
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

    class AutosaverClass(x52NonPicklable):
        def __init__(self):
            self.suppress_autosave_confirm = False
            self.pending_save = None
            self.prev_active_slot = "N/A"
            self.confirm_dialog_opened = False
            self.after_load_save_position_pending = False
            self.active_slot_pending = None
            self.prevent_autosaving = Settings.preventAutosavingWhileNotInGame
            self.loaded_manual_save_without_choices = False
            self.prevent_confirm_on_large_page_jump = False

        def set_active_slot(self, slotname):
            page, slot = Utils.split_slotname(slotname)

            #Last resort check to counter forced autosaves screwing up the counter (e.g. $ renpy.save("auto-1") somewhere in the dialog)
            if page != 0 and slot != 0:
                self.prev_active_slot = renpy.store.JK_ActiveSlot + "" # Copy the data, not just the pointer
                renpy.store.JK_ActiveSlot = slotname

                if self.prevent_confirm_on_large_page_jump:
                    self.prevent_confirm_on_large_page_jump = False

                else:
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

            if(slot > Utils.get_slots_per_page()):
                slot = 1
                page += 1

            slotString = str(page) + "-" + str(slot)

            return page, slot, slotString

        def get_current_slot(self):
            slotString = renpy.store.JK_ActiveSlot
            page, slot = Utils.split_slotname(slotString)

            return page, slot, slotString

        def get_previous_slot(self):
            page, slot = Utils.split_slotname(renpy.store.JK_ActiveSlot)

            slot -= 1

            if(slot < 1):
                slot = 1
                page -= 1

            slotString = str(page) + "-" + str(slot)

            return page, slot, slotString

        def set_next_slot(self):
            _, _, slotString = Autosaver.get_next_slot()
            self.set_active_slot(slotString)

        def set_previous_slot(self):
            _, _, slotString = Autosaver.get_previous_slot()
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

        def __is_choice_question(self, choice):
            try:
                i = 0
                menu_node = renpy.game.script.lookup(choice.location)
                choice_item = menu_node.items[choice.value]
                if len(choice_item) > 2 and choice_item[2]:
                    node = choice_item[2][0]
                else:
                    node = None

                resolved_nodes = [menu_node]
                
                prediction_depth = 0
                while node and prediction_depth < 2:
                    if node in resolved_nodes:
                        return True
                    
                    # Python usually indicates that something will happen with variables,
                    # so even if the choice might be a question it is a question with a potential reward, thus save-worthy.
                    if isinstance(node, renpy.ast.Python) and hasattr(node, 'code') and hasattr(node.code, 'source'):
                        if not node.code.source.startswith('renpy.pause(') and not node.code.source.startswith('ui.'):
                            if hasattr(node, "expression") and node.expression is not None:
                                if bool(node.expression) == node.expression or renpy.python.py_eval(node.expression):
                                    return False
                            else:
                                return False

                    elif isinstance(node, renpy.ast.If):
                        for condition, block in node.entries:
                            if renpy.python.py_eval(condition):
                                node = block[0]
                                break

                    elif isinstance(node, renpy.ast.Jump):
                            prediction_depth += 1

                            prediction = node.predict()
                            if len(prediction) > 0:
                                node = prediction[0]
                            else:
                                node = node.next
                    else:
                        node = node.next

                    i += 1

                    if i > 1000000:
                        raise Exception("JK.Utils.find_next_label_from_current() infinite loop prevented. Or just reeeeeally long code stack...")
            except Exception as e:
                print(e)

            return False

        def handle_choice_selection(self, choice):
            # Prevent a single choice from saving multiple times (debouncer)
            if self.pending_save:
                return

            # Prevent making any autosave actions when the feature is diabled or is viewing a memory or a replay
            if not Playthroughs.active_playthrough.autosaveOnChoices or Memories.memoryInProgress or renpy.store._in_replay:
                return

            # If autosave on question is disabled, make sure the jump at then end of the choice doesn't lead back to JK_LastLabel
            if not Settings.autosaveOnQuestion:
                if self.__is_choice_question(choice):
                    return

            # Processes the label as Ren'Py would to remove any possible substitutions via [...] e.g. [player_name]
            textComponent = renpy.ui.text(choice.label)
            choiceText = Utils.escape_renpy_reserved_characters(' '.join(textComponent.text))

            self.create_pending_save(choiceText)

        # The JK_ActiveSlot always equals the slot that was loaded because the saves are made right before selecting a choice for easy re-choicing.
        # However when a manual save is loaded it might not be a choice screen.
        # If so, the save slot needs to move further as to not override the manual slot with the next autosave.
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
            temp_save_slotname = "JK-temp"

            def __init__(self, choice):
                self.choice = choice

                # Never, EVER call any saving functions from here!!!!!!!!!!!!!!!!!!!!!!!!!
                # I, an idiot, have made this mistake twice,
                # leading to an hour of debugging why, in the ever-loving f***, Autosaver.pending_save is None.
                # (The instance is in the process of being constructed, including calling functions that were trying to access this instance, 
                # and the assignment happens afterward...)

            def early_save(self):
                extra_info = ''
                if Playthroughs.active_playthrough.useChoiceLabelAsSaveName:
                    extra_info = self.choice

                renpy.take_screenshot()
                renpy.save(self.temp_save_slotname, extra_info)

            def save(self):
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
init python in JK:
    _constant = True

    import pygame_sdl2 as pygame

    class CaretBlink(renpy.display.core.Displayable):
        """
        A displayable that renders the caret.
        """

        def __init__(self, caret, caret_blink, **properties):

            properties.setdefault("yalign", 0.0)

            super(CaretBlink, self).__init__(**properties)
            caret = renpy.easy.displayable(caret)

            if caret._duplicatable:
                caret = caret._duplicate(None)
                caret._unique()

            self.caret = caret
            self.caret_blink = caret_blink

            self.st_base = 0

        def get_placement(self):
            xpos, ypos, xanchor, yanchor, _xoffset, _yoffset, subpixel = self.caret.get_placement()

            return (xpos, ypos, xanchor, yanchor, 0, 2, subpixel)

        def visit(self):
            return [ self.caret ]

        def render(self, width, height, st, at):
            st -= self.st_base or 0

            cr = renpy.display.render.render(self.caret, width, height, st, at)
            rv = renpy.display.render.Render(1, height)

            ttl = self.caret_blink - st % self.caret_blink

            if ttl > self.caret_blink / 2.0:
                rv.blit(cr, (0, 0))

            renpy.display.render.redraw(self, ttl % (self.caret_blink / 2.))

            return rv

    class TextInput(x52NonPicklable):
        active_text_input_screen_variable_name = "__activeTextInput__"

        def __init__(self, identifier, variableName=None, value=None, auto_focus=False, disabled=False, multiline=False, allowed_characters=None, excluded_characters=None, max_length=None, placeholder=None):
            self.id = identifier
            self.variableName = variableName or identifier
            self.disabled = disabled
            self.value = value
            self.displayable_reference = None
            self.auto_focus = auto_focus
            self.editable = False
            self.edit_text = None
            self.caret_pos = 0
            self.old_caret_pos = 0
            self.selection_start = None
            self.multiline = multiline
            self.allowed_characters = allowed_characters
            self.excluded_characters = excluded_characters
            self.max_length = max_length
            self.placeholder = placeholder

            if auto_focus:
                self.enable()

        def displayable(self, placeholder=None, **properties):
            self.displayable_reference = TextInputDisplayable(controller=self, placeholder=placeholder, **properties)
            return self.displayable_reference

        def enable(self):
            self.editable = True
            self.caret_pos = len(self.get_value() or "")

            TextInput.set_active(self.id)

        def disable(self):
            self.editable = False

            cs = renpy.current_screen()
            if not cs:
                return

            if cs.scope[self.active_text_input_screen_variable_name] == self.id:
                cs.scope[self.active_text_input_screen_variable_name] = None

                renpy.restart_interaction()
        
        def get_value(self):
            if self.value:
                return self.value.get_text()
            elif self.variableName:
                return Utils.get_screen_variable(self.variableName)
            return None

        def get_enable_action(self):
            class Action(renpy.ui.Action):
                def __init__(self, input):
                    self.input = input

                def __call__(self):
                    self.input.enable()

            return Action(self)

        def get_disable_action(self):
            class Action(renpy.ui.Action):
                def __init__(self, input):
                    self.input = input

                def __call__(self):
                    self.input.disable()

            return Action(self)

        def get_selection_start_end(self):
            start = min(self.selection_start, self.caret_pos)
            end = max(self.selection_start, self.caret_pos)

            return start, end

        @staticmethod
        def is_active(id):
            return Utils.get_screen_variable(TextInput.active_text_input_screen_variable_name) == id

        @staticmethod
        def set_active(id):
            renpy.store.SetScreenVariable(TextInput.active_text_input_screen_variable_name, id)()

        class SetActiveAction(renpy.ui.Action):
            def __init__(self, id):
                self.id = id

            def __call__(self):
                TextInput.set_active(self.id)

    class TextInputDisplayable(renpy.text.text.Text):
        focusable = True

        def __init__(self, controller, placeholder=None, style="textinput", **properties):
            super(TextInputDisplayable, self).__init__("", style=style, **properties)

            self.width_height = (0, 0)
            self.controller = controller
            self.prefix = ""
            self.suffix = ""
            self.shown = False
            self.st = None
            self.changed = None
            self.placeholder = placeholder
            
            if self.controller.value:
                self.changed = self.controller.value.set_text

            self.default = self.controller.get_value() or ""
            self.content = self.default

            if not self.controller.editable and TextInput.is_active(self.controller.id):
                self.controller.enable()
            elif self.controller.editable and not TextInput.is_active(self.controller.id):
                self.controller.disable()

            self.setup_caret(style, **properties)

            self.update_text(self.content)

        def setup_caret(self, style, **properties):
            caretprops = { 'color' : None }

            for i, v in properties.items():
                if i.endswith("color") or i.startswith("caret_"):
                    caretprops[i] = v
            
            caret = renpy.display.image.Solid(xysize=(1, self.style.size), style=style + "_caret", **caretprops)
            self.caret = CaretBlink(caret, 1)

        # =====================
        # Displayable overrides
        # =====================

        # This is needed to ensure the caret updates properly.
        def set_style_prefix(self, prefix, root):
            if prefix != self.style.prefix:
                self.update_text(self.content)

            super(TextInputDisplayable, self).set_style_prefix(prefix, root)

        def per_interact(self):
            if not self.shown:
                self.content = self.controller.get_value() or ""
                self.update_text(self.content)

                self.shown = True

        def place(self, dest, x, y, width, height, surf, main=True):
            self.width_height = (width, height)

            return super(TextInputDisplayable, self).place(dest, x, y, width, height, surf, main)

        def render(self, width, height, st, at):
            self.st = st

            rv = super(TextInputDisplayable, self).render(width, height, st, at)

            if self.controller.editable:
                rv.text_input = True

            return rv

        def event(self, ev, x, y, st):
            self.st = st

            # Test for enable/disable on click
            try:
                self.__event_click(ev, x, y, st)
            except Exception as e:
                print(e)
                raise renpy.display.core.IgnoreEvent()
            
            if not self.controller.editable:
                return None

            edit_controls = any([
                renpy.map_event(ev, "input_jump_word_left"),
                renpy.map_event(ev, "input_jump_word_right"),
                renpy.map_event(ev, "input_delete_word"),
                renpy.map_event(ev, "input_delete_full"),
            ])

            if (ev.type == pygame.KEYDOWN) and (pygame.key.get_mods() & pygame.KMOD_LALT) and (not ev.unicode) and not edit_controls:
                return None

            l = len(self.content)

            raw_text = None

            if renpy.map_event(ev, "input_backspace"):
                if self.controller.selection_start != None:
                    self.update_text(self.__try_delete_selected_content())

                elif self.content and self.controller.caret_pos > 0:
                    content = self.content[0:self.controller.caret_pos - 1] + self.content[self.controller.caret_pos:l]
                    self.controller.caret_pos -= 1
                    self.update_text(content)

                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif self.controller.multiline and renpy.map_event(ev, 'input_next_line'):
                self.__try_set_selection_start()

                content = self.content[:self.controller.caret_pos] + '\n' + self.content[self.controller.caret_pos:]
                self.controller.caret_pos += 1
                self.update_text(content)

                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif renpy.map_event(ev, "input_left"):
                self.__try_set_selection_start()

                if self.controller.caret_pos > 0:
                    self.controller.caret_pos -= 1
                    self.update_text(self.content)

                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif renpy.map_event(ev, "input_jump_word_left"):
                self.__try_set_selection_start()

                if self.controller.caret_pos > 0:
                    space_pos = 0
                    for item in re.finditer(r"\s+", self.content[:self.controller.caret_pos]):
                        _start, end = item.span()
                        if end != self.controller.caret_pos:
                            space_pos = end
                    self.controller.caret_pos = space_pos
                    self.update_text(self.content)

                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif renpy.map_event(ev, "input_right"):
                self.__try_set_selection_start()

                if self.controller.caret_pos < l:
                    self.controller.caret_pos += 1
                    self.update_text(self.content)

                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif renpy.map_event(ev, "input_jump_word_right"):
                self.__try_set_selection_start()

                if self.controller.caret_pos < l:
                    space_pos = l
                    for item in re.finditer(r"\s+", self.content[self.controller.caret_pos + 1:]):
                        start, end = item.span()
                        space_pos = end
                        break
                    self.controller.caret_pos = min(space_pos + self.controller.caret_pos + 1, l)
                    self.update_text(self.content)

                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif renpy.map_event(ev, "input_up"):
                self.__try_set_selection_start()

                lines, current_line_idx, current_column = self.__get_caret_info()

                # If already on the first line, no movement is possible
                if current_line_idx == 0:
                    self.controller.caret_pos = 0

                    self.update_text(self.content)
                    renpy.display.render.redraw(self, 0)
                    raise renpy.display.core.IgnoreEvent()

                # Move to the previous line
                prev_line = lines[current_line_idx - 1]
                new_column = min(len(prev_line.rstrip()), current_column)  # Move to the same column or the end of the previous line

                # Calculate the new caret position
                new_caret_pos = sum(len(line) for line in lines[:current_line_idx - 1]) + new_column

                # Update the caret position
                self.controller.caret_pos = new_caret_pos

                self.update_text(self.content)
                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()
            
            elif renpy.map_event(ev, "input_down"):
                self.__try_set_selection_start()

                lines, current_line_idx, current_column = self.__get_caret_info()

                # If already on the last line, no movement is possible
                if current_line_idx == len(lines) - 1:
                    self.controller.caret_pos = len(self.content)  # Move to the end of the content (last position)

                    self.update_text(self.content)
                    renpy.display.render.redraw(self, 0)
                    raise renpy.display.core.IgnoreEvent()

                # Move to the next line
                next_line = lines[current_line_idx + 1]
                new_column = min(len(next_line.rstrip()), current_column)  # Move to the same column or the end of the next line

                # Calculate the new caret position
                new_caret_pos = sum(len(line) for line in lines[:current_line_idx + 1]) + new_column

                # Update the caret position
                self.controller.caret_pos = new_caret_pos

                self.update_text(self.content)
                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()
            
            elif renpy.map_event(ev, "input_delete"):
                if self.controller.selection_start != None:
                    self.update_text(self.__try_delete_selected_content())

                elif self.controller.caret_pos < l:
                    content = self.content[0:self.controller.caret_pos] + self.content[self.controller.caret_pos + 1:l]
                    self.update_text(content)

                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif renpy.map_event(ev, "input_delete_word"):
                if self.controller.selection_start != None:
                    self.update_text(self.__try_delete_selected_content())

                elif self.controller.caret_pos <= l:
                    space_pos = 0
                    for item in re.finditer(r"\s+", self.content[:self.controller.caret_pos]):
                        start, end = item.span()
                        if end != self.controller.caret_pos:
                            space_pos = end
                    content = self.content[0:space_pos] + self.content[self.controller.caret_pos:l]
                    self.controller.caret_pos = space_pos
                    self.update_text(content)

                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif renpy.map_event(ev, "input_delete_full"):
                if self.controller.selection_start != None:
                    self.update_text(self.__try_delete_selected_content())

                elif self.controller.caret_pos <= l:
                    content = self.content[self.controller.caret_pos:l]
                    self.controller.caret_pos = 0
                    self.update_text(content)

                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif renpy.map_event(ev, "input_content_start"):
                self.__try_set_selection_start()

                self.controller.caret_pos = 0
                self.update_text(self.content)
                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif renpy.map_event(ev, "input_content_end"):
                self.__try_set_selection_start()

                self.controller.caret_pos = l
                self.update_text(self.content)
                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif renpy.map_event(ev, "input_home"):
                self.__try_set_selection_start()

                lines, current_line_idx, current_column = self.__get_caret_info()
                self.controller.caret_pos = self.controller.caret_pos - current_column
                self.update_text(self.content)
                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif renpy.map_event(ev, "input_end"):
                self.__try_set_selection_start()

                lines, current_line_idx, current_column = self.__get_caret_info()
                self.controller.caret_pos = self.controller.caret_pos - current_column + len(lines[current_line_idx]) - (0 if current_line_idx == len(lines) - 1 else 1)
                self.update_text(self.content)
                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif renpy.map_event(ev, "input_copy"):
                if self.controller.selection_start != None:
                    start, end = self.controller.get_selection_start_end()
                    text = self.content[0:start] + self.content[end:l]
                else:
                    text = self.content.encode("utf-8")

                pygame.scrap.put(pygame.scrap.SCRAP_TEXT, text)
                raise renpy.display.core.IgnoreEvent()

            elif renpy.map_event(ev, "input_paste"):
                text = pygame.scrap.get(pygame.scrap.SCRAP_TEXT)
                text = text.decode("utf-8")
                raw_text = ""
                for c in text:
                    if ord(c) >= 32:
                        raw_text += c
            
            elif renpy.map_event(ev, "input_select_all"):
                self.controller.selection_start = 0
                self.controller.caret_pos = l

                self.update_text(self.content)
                renpy.display.render.redraw(self, 0)

                raise renpy.display.core.IgnoreEvent()

            # elif renpy.map_event(ev, 'input_next_input'):
            #     if self.id:
            #         inputIDs = Utils.get_screen_variable(self.availableTextInputsScreenVariableName) or []
            #         print(inputIDs)
            #         i = inputIDs.index(self.id) + 1

            #         if i == 0:
            #             return

            #         if i < 0:
            #             i = len(inputIDs) - 1
                    
            #         renpy.store.SetScreenVariable(self.active_text_input_screen_variable_name, inputIDs[i])()
            #         raise renpy.display.core.IgnoreEvent()

            # elif renpy.map_event(ev, 'input_prev_input'):
            #     if self.id:
            #         inputIDs = Utils.get_screen_variable(self.availableTextInputsScreenVariableName) or []
            #         i = inputIDs.index(self.id) - 1

            #         if i == -1:
            #             return

            #         if i > len(inputIDs) - 1:
            #             i = 0
                    
            #         renpy.store.SetScreenVariable(self.active_text_input_screen_variable_name, inputIDs[i])()
            #         raise renpy.display.core.IgnoreEvent()


            elif ev.type == pygame.TEXTEDITING:
                self.update_text(self.content, check_size=True)

                raise renpy.display.core.IgnoreEvent()

            elif ev.type == pygame.TEXTINPUT:
                self.edit_text = ""
                raw_text = ev.text

            elif ev.type == pygame.KEYDOWN:

                if ev.unicode and ord(ev.unicode[0]) >= 32:
                    raw_text = ev.unicode
                elif renpy.display.interface.text_event_in_queue():
                    raise renpy.display.core.IgnoreEvent()
                elif (32 <= ev.key < 127) and not (ev.mod & (pygame.KMOD_ALT | pygame.KMOD_META)):
                    # Ignore printable keycodes without unicode.
                    raise renpy.display.core.IgnoreEvent()

            if raw_text is not None:

                text = ""

                allow = self.controller.allowed_characters
                exclude = self.controller.excluded_characters

                for c in raw_text:

                    # Allow is given
                    if allow:

                        # Allow is regex
                        if isinstance(allow, re.Pattern if hasattr(re, "Pattern") else re._pattern_type):

                            # Character doesn't match
                            if allow.search(c) is None:
                                continue

                        # Allow is string
                        elif c not in allow:
                            continue

                    # Exclude is given
                    if exclude:

                        # Exclude is regex
                        if isinstance(exclude, re.Pattern if hasattr(re, "Pattern") else re._pattern_type):

                            # Character matches
                            if exclude.search(c) is not None:
                                continue

                        # Exclude is string
                        elif c in exclude:
                            continue

                    text += c

                if self.controller.max_length:
                    remaining = self.controller.max_length - len(self.content)
                    text = text[:remaining]

                if text:
                    content = self.__try_delete_selected_content() or self.content
                    content = content[0:self.controller.caret_pos] + text + content[self.controller.caret_pos:l]
                    self.controller.caret_pos += len(text)

                    self.update_text(content, check_size=True)

                raise renpy.display.core.IgnoreEvent()

        # =================
        # Private functions
        # =================

        def __event_click(self, ev, x, y, st):
            if renpy.map_event(ev, "button_select"):
                width, height = self.width_height

                # Ensure clicked inside
                if x >= 0 and x <= width and y >= 0 and y <= height:
                    if not self.controller.editable:
                        self.controller.enable()
                        return renpy.display.core.IgnoreEvent()
                elif self.controller.editable:
                    self.controller.disable()

            return None

        def __get_caret_info(self):
            # Split the content into lines, preserving the line endings
            lines = self.content.splitlines(1)

            # Calculate the caret's current line and column
            char_count = 0
            current_line_idx = 0
            current_column = 0

            for i, line in enumerate(lines):
                current_line_idx = i
                current_column = self.controller.caret_pos - char_count

                if char_count + len(line) > self.controller.caret_pos:
                    break

                char_count += len(line)

            return lines, current_line_idx, current_column

        def __try_set_selection_start(self):
            if self.controller.selection_start is None:
                if (pygame.key.get_mods() & pygame.K_LSHIFT or pygame.key.get_mods() & pygame.K_RSHIFT):
                    self.controller.selection_start = 0 + self.controller.caret_pos
            else:
                if not (pygame.key.get_mods() & pygame.K_LSHIFT or pygame.key.get_mods() & pygame.K_RSHIFT):
                    self.controller.selection_start = None

        def __try_delete_selected_content(self):
            if self.controller.selection_start != None:
                start, end = self.controller.get_selection_start_end()

                self.controller.caret_pos = start
                self.controller.selection_start = None

                return self.content[0:start] + self.content[end:len(self.content)]

        def update_text(self, new_content, check_size=False):
            editable = self.controller.editable
            edit = renpy.display.interface.text_editing
            old_content = self.content

            if new_content != self.content or editable != self.controller.editable or edit:
                renpy.display.render.redraw(self, 0)

            self.controller.editable = editable

            # Choose the caret.
            caret = self.style.caret
            if caret is None:
                caret = self.caret

            # Format text being edited by the IME.
            if edit:
                self.edit_text = edit.text

                edit_text_0 = edit.text[:edit.start]
                edit_text_1 = edit.text[edit.start:edit.start + edit.length]
                edit_text_2 = edit.text[edit.start + edit.length:]

                edit_text = ""

                if edit_text_0:
                    edit_text += "{u=1}" + edit_text_0.replace("{", "{{") + "{/u}"

                if edit_text_1:
                    edit_text += "{u=2}" + edit_text_1.replace("{", "{{") + "{/u}"

                if edit_text_2:
                    edit_text += "{u=1}" + edit_text_2.replace("{", "{{") + "{/u}"

            else:
                self.edit_text = ""
                edit_text = ""

            def set_content(content):
                if content == "":
                    content = self.placeholder or self.controller.placeholder or u" "
                    self.style.color = Colors.text_placeholder# Set placeholder color

                if editable:
                    l = len(content)

                    content = content.replace("{", "{{")

                    selection_start = self.controller.selection_start
                    caret_pos = self.controller.caret_pos

                    if selection_start is None:
                        selection_start = caret_pos

                    start = min(selection_start, caret_pos)
                    end = max(selection_start, caret_pos)

                    selection_start_tag = "{color=#ff0}{u}"
                    selection_end_tag = "{/color}{/u}"

                    content_before_selection = content[0:start]
                    selected_content = selection_start_tag + content[start:end] + selection_end_tag if selection_start != caret_pos else content[start:end]
                    content_after_selection = content[end:l]

                    self.set_text([self.prefix, content_before_selection, edit_text, selected_content, caret, content_after_selection, self.suffix])
                else:
                    self.set_text([self.prefix, content.replace("{", "{{"), self.suffix ])

                if isinstance(self.caret, CaretBlink):
                    self.caret.st_base = self.st
                    renpy.display.render.redraw(self.caret, 0)

            set_content(new_content)

            if new_content != old_content:
                self.content = new_content

                if self.changed:
                    self.changed(new_content)

                    new_value = self.controller.get_value() or ""
                    if new_value != new_content:
                        #The new value was most likely rejected, restore the previous position
                        self.controller.caret_pos = self.controller.old_caret_pos

                    self.update_text(new_value, check_size)

                if self.controller.variableName:
                    renpy.store.SetScreenVariable(self.controller.variableName, new_content)()
        
    
    # Input.
    renpy.config.keymap.update({
        'input_backspace': [ 'K_BACKSPACE', 'repeat_K_BACKSPACE' ] if not hasattr(renpy.config.keymap, 'input_backspace') else renpy.config.keymap.input_backspace,
        'input_next_line': [ 'K_RETURN', 'repeat_K_RETURN', 'K_KP_ENTER', 'repeat_K_KP_ENTER' ] if not hasattr(renpy.config.keymap, 'input_next_line') else renpy.config.keymap.input_next_line,
        'input_left': [ 'K_LEFT', 'repeat_K_LEFT' ] if not hasattr(renpy.config.keymap, 'input_left') else renpy.config.keymap.input_left,
        'input_right': [ 'K_RIGHT', 'repeat_K_RIGHT' ] if not hasattr(renpy.config.keymap, 'input_right') else renpy.config.keymap.input_right,
        'input_up': [ 'K_UP', 'repeat_K_UP' ] if not hasattr(renpy.config.keymap, 'input_up') else renpy.config.keymap.input_up,
        'input_down': [ 'K_DOWN', 'repeat_K_DOWN' ] if not hasattr(renpy.config.keymap, 'input_down') else renpy.config.keymap.input_down,
        'input_delete': [ 'K_DELETE', 'repeat_K_DELETE' ] if not hasattr(renpy.config.keymap, 'input_delete') else renpy.config.keymap.input_delete,
        'input_home': [ 'K_HOME', 'meta_K_LEFT' ] if not hasattr(renpy.config.keymap, 'input_home') else renpy.config.keymap.input_home,
        'input_end': [ 'K_END', 'meta_K_RIGHT' ] if not hasattr(renpy.config.keymap, 'input_end') else renpy.config.keymap.input_end,
        'input_copy': [ 'ctrl_noshift_K_INSERT', 'ctrl_noshift_K_c', 'meta_noshift_K_c' ] if not hasattr(renpy.config.keymap, 'input_copy') else renpy.config.keymap.input_copy,
        'input_paste': [ 'shift_K_INSERT', 'ctrl_noshift_K_v', 'meta_noshift_K_v' ] if not hasattr(renpy.config.keymap, 'input_paste') else renpy.config.keymap.input_paste,
        'input_jump_word_left': [ 'ctrl_K_LEFT', 'repeat_ctrl_K_LEFT' ] if not hasattr(renpy.config.keymap, 'input_jump_word_left') else renpy.config.keymap.input_jump_word_left,
        'input_jump_word_right': [ 'ctrl_K_RIGHT', 'repeat_ctrl_K_RIGHT' ] if not hasattr(renpy.config.keymap, 'input_jump_word_right') else renpy.config.keymap.input_jump_word_right,
        'input_delete_word': [ 'repeat_ctrl_K_BACKSPACE' ] if not hasattr(renpy.config.keymap, 'input_delete_word') else renpy.config.keymap.input_delete_word,
        'input_delete_full': [ 'repeat_meta_K_BACKSPACE' ] if not hasattr(renpy.config.keymap, 'input_delete_full') else renpy.config.keymap.input_delete_full,
        'input_content_start': [ 'shift_K_HOME' ],
        'input_content_end': [ 'shift_K_END' ],
        'input_select_all': [ 'ctrl_K_a' ],
        # 'input_next_input': ['noshift_K_TAB'], #TODO: Finish prev/next input via TAB
        # 'input_prev_input': ['shift_K_TAB']
    })
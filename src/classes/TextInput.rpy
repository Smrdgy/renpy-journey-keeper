init 1 python in SSSSS:
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
            st -= self.st_base

            cr = renpy.display.render.render(self.caret, width, height, st, at)
            rv = renpy.display.render.Render(1, height)

            ttl = self.caret_blink - st % self.caret_blink

            if ttl > self.caret_blink / 2.0:
                rv.blit(cr, (0, 0))

            renpy.display.render.redraw(self, ttl % (self.caret_blink / 2.))

            return rv

    class TextInputBase(renpy.text.text.Text): # @UndefinedVariable
        """
        This is a Displayable that takes text as input.
        """

        activeTextInputScreenVariableName = "__activeTextInput__"
        availableTextInputsScreenVariableName = "__availableInputs__"
        changed = None
        prefix = ""
        suffix = ""
        caret_pos = 0
        old_caret_pos = 0
        pixel_width = None
        default = u""
        edit_text = u""
        value = None
        shown = False
        multiline = False
        editable = False

        st = 0

        def __init__(
            self,
            id=None,
            default="",
            length=None,
            style='textinput',
            allow=None,
            exclude=None,
            prefix="",
            suffix="",
            changed=None,
            button=None,
            replaces=None,
            editable=False,
            pixel_width=None,
            value=None,
            copypaste=True,
            caret_blink=1,
            multiline=False,
            text_size=None,
            variableName=None,
            **properties
        ):
            super(TextInputBase, self).__init__("", style=style, replaces=replaces, substitute=False, **properties)

            self.width_height = (0, 0)

            self.button = None
            
            self.variableName = variableName
            self.id = id

            if variableName:
                default = Utils.getScreenVariable(self.variableName)

            if value:
                self.value = value
                changed = value.set_text
                default = value.get_text()

            self.default = str(default)
            self.content = self.default

            self.length = length

            self.allow = allow
            self.exclude = exclude
            self.prefix = prefix
            self.suffix = suffix
            self.copypaste = copypaste

            self.changed = changed

            self.editable = editable
            self.pixel_width = pixel_width

            self.multiline = multiline

            caretprops = { 'color' : None }

            for i, v in properties.items():
                if i.endswith("color"):
                    caretprops[i] = v

            # Get font size for the caret's height
            text_size = renpy.style.Style(style, properties).size
            caret = renpy.display.image.Solid(xysize=(1, text_size), style=style, **caretprops)

            if caret_blink:
                caret = CaretBlink(caret, caret_blink)

            self.caret = caret

            if self.id and not editable:
                self.editable = Utils.getScreenVariable(self.activeTextInputScreenVariableName) == self.id

            if self.id:
                inputs = Utils.getScreenVariable(self.availableTextInputsScreenVariableName) or []
                inputs.append(self.id)

                renpy.store.SetScreenVariable(self.availableTextInputsScreenVariableName, inputs)

            if button:
                button.clicked = TextInputBase.ToggleProxy(self)
                self.button = button

            if isinstance(replaces, TextInputBase):
                self.content = replaces.content
                self.editable = replaces.editable
                self.caret_pos = replaces.caret_pos
                self.shown = replaces.shown
                self.editable = replaces.editable

            if editable:
                TextInputBase.caret_pos = len(self.content)

            self.update_text(self.content, self.editable)

        def place(self, dest, x, y, width, height, surf, main=True):
            self.width_height = (width, height)

            return super(TextInputBase, self).place(dest, x, y, width, height, surf, main)

        class ToggleProxy(renpy.ui.Action):
            def __init__(self, textinput):
                self.textinput = textinput

            def __call__(self):
                if self.textinput.editable:
                    self.textinput.disable()
                else:
                    self.textinput.enable()
                

        def update_text(self, new_content, editable, check_size=False):

            edit = renpy.display.interface.text_editing

            old_content = self.content

            if new_content != self.content or editable != self.editable or edit:

                renpy.display.render.redraw(self, 0)

            self.editable = editable

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
                    content = u" "

                if editable:
                    l = len(content)
                    self.set_text([self.prefix, content[0:TextInputBase.caret_pos].replace("{", "{{"), edit_text, caret, content[TextInputBase.caret_pos:l].replace("{", "{{"), self.suffix])
                else:
                    self.set_text([self.prefix, content.replace("{", "{{"), self.suffix ])

                if isinstance(self.caret, CaretBlink):
                    self.caret.st_base = self.st
                    renpy.display.render.redraw(self.caret, 0)

            set_content(new_content)

            if check_size and self.pixel_width:
                w, _h = self.size()
                if w > self.pixel_width:
                    if self.editable:
                        TextInputBase.caret_pos = TextInputBase.old_caret_pos
                    set_content(old_content)
                    return

            if new_content != old_content:
                self.content = new_content

                if self.changed:
                    self.changed(new_content)

                if self.variableName:
                    renpy.store.SetScreenVariable(self.variableName, new_content)()

        # This is needed to ensure the caret updates properly.
        def set_style_prefix(self, prefix, root):
            if prefix != self.style.prefix:
                self.update_text(self.content, self.editable)

            super(TextInputBase, self).set_style_prefix(prefix, root)

        def enable(self):
            self.update_text(self.content, True)

            TextInputBase.caret_pos = len(self.content)

            if self.id:
                renpy.store.SetScreenVariable(self.activeTextInputScreenVariableName, self.id)()

        def disable(self):
            self.update_text(self.content, False)

            if self.id:
                if Utils.getScreenVariable(self.activeTextInputScreenVariableName) == self.id:
                    renpy.store.SetScreenVariable(self.activeTextInputScreenVariableName, None)()

        def per_interact(self):

            global default_input_value

            if self.value is not None:

                inputs.append(self)
                input_values.append(self.value)

                if self.value.default and (default_input_value is None):
                    default_input_value = self.value

            if not self.shown:

                if self.value is not None:
                    default = self.value.get_text()
                    self.default = str(default)

                self.content = self.default
                self.update_text(self.content, self.editable)

                self.shown = True

        def event(self, ev, x, y, st):
            self.st = st
            TextInputBase.old_caret_pos = TextInputBase.caret_pos

            if not self.button and self.id:
                try:
                    self.handleClick(ev, x, y, st)
                except:
                    raise renpy.display.core.IgnoreEvent()
                    

            if not self.editable:
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

            if pygame.key.get_mods() & pygame.KMOD_LCTRL:
                raise renpy.display.core.IgnoreEvent()
            elif renpy.map_event(ev, "input_backspace"):

                if self.content and TextInputBase.caret_pos > 0:
                    content = self.content[0:TextInputBase.caret_pos - 1] + self.content[TextInputBase.caret_pos:l]
                    TextInputBase.caret_pos -= 1
                    self.update_text(content, self.editable)

                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif self.multiline and renpy.map_event(ev, 'input_next_line'):
                content = self.content[:TextInputBase.caret_pos] + '\n' + self.content[TextInputBase.caret_pos:]
                TextInputBase.caret_pos += 1
                self.update_text(content, self.editable)

                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif renpy.map_event(ev, "input_left"):
                if TextInputBase.caret_pos > 0:
                    TextInputBase.caret_pos -= 1
                    self.update_text(self.content, self.editable)

                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif renpy.map_event(ev, "input_jump_word_left"):
                if TextInputBase.caret_pos > 0:
                    space_pos = 0
                    for item in re.finditer(r"\s+", self.content[:TextInputBase.caret_pos]):
                        _start, end = item.span()
                        if end != TextInputBase.caret_pos:
                            space_pos = end
                    TextInputBase.caret_pos = space_pos
                    self.update_text(self.content, self.editable)

                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif renpy.map_event(ev, "input_right"):
                if TextInputBase.caret_pos < l:
                    TextInputBase.caret_pos += 1
                    self.update_text(self.content, self.editable)

                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif renpy.map_event(ev, "input_jump_word_right"):
                if TextInputBase.caret_pos < l:
                    space_pos = l
                    for item in re.finditer(r"\s+", self.content[TextInputBase.caret_pos + 1:]):
                        start, end = item.span()
                        space_pos = end
                        break
                    TextInputBase.caret_pos = min(space_pos + TextInputBase.caret_pos + 1, l)
                    self.update_text(self.content, self.editable)

                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif renpy.map_event(ev, "input_up"):
                # Split the content into lines, preserving the line endings
                lines = self.content.splitlines(1)

                # Calculate the caret's current line and column
                char_count = 0
                current_line_idx = 0
                current_column = 0

                for i, line in enumerate(lines):
                    current_line_idx = i
                    current_column = TextInputBase.caret_pos - char_count

                    if char_count + len(line) > TextInputBase.caret_pos:
                        break

                    char_count += len(line)

                # If already on the first line, no movement is possible
                if current_line_idx == 0:
                    TextInputBase.caret_pos = 0

                    self.update_text(self.content, self.editable)
                    renpy.display.render.redraw(self, 0)
                    raise renpy.display.core.IgnoreEvent()

                # Move to the previous line
                prev_line = lines[current_line_idx - 1]
                new_column = min(len(prev_line.rstrip()), current_column)  # Move to the same column or the end of the previous line

                # Calculate the new caret position
                new_caret_pos = sum(len(line) for line in lines[:current_line_idx - 1]) + new_column

                # Update the caret position
                TextInputBase.caret_pos = new_caret_pos

                self.update_text(self.content, self.editable)
                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()
            
            elif renpy.map_event(ev, "input_down"):
                # Split the content into lines, preserving the line endings 
                lines = self.content.splitlines(1)

                # Calculate the caret's current line and column
                char_count = 0
                current_line_idx = 0
                current_column = 0

                for i, line in enumerate(lines):
                    current_line_idx = i
                    current_column = TextInputBase.caret_pos - char_count

                    if char_count + len(line) > TextInputBase.caret_pos:
                        break

                    char_count += len(line)

                # If already on the last line, no movement is possible
                if current_line_idx == len(lines) - 1:
                    TextInputBase.caret_pos = len(self.content)  # Move to the end of the content (last position)

                    self.update_text(self.content, self.editable)
                    renpy.display.render.redraw(self, 0)
                    raise renpy.display.core.IgnoreEvent()

                # Move to the next line
                next_line = lines[current_line_idx + 1]
                new_column = min(len(next_line.rstrip()), current_column)  # Move to the same column or the end of the next line

                # Calculate the new caret position
                new_caret_pos = sum(len(line) for line in lines[:current_line_idx + 1]) + new_column

                # Update the caret position
                TextInputBase.caret_pos = new_caret_pos

                self.update_text(self.content, self.editable)
                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()
            
            elif renpy.map_event(ev, "input_delete"):
                if TextInputBase.caret_pos < l:
                    content = self.content[0:TextInputBase.caret_pos] + self.content[TextInputBase.caret_pos + 1:l]
                    self.update_text(content, self.editable)

                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif renpy.map_event(ev, "input_delete_word"):
                if TextInputBase.caret_pos <= l:
                    space_pos = 0
                    for item in re.finditer(r"\s+", self.content[:TextInputBase.caret_pos]):
                        start, end = item.span()
                        if end != TextInputBase.caret_pos:
                            space_pos = end
                    content = self.content[0:space_pos] + self.content[TextInputBase.caret_pos:l]
                    TextInputBase.caret_pos = space_pos
                    self.update_text(content, self.editable)

                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif renpy.map_event(ev, "input_delete_full"):
                if TextInputBase.caret_pos <= l:
                    content = self.content[TextInputBase.caret_pos:l]
                    TextInputBase.caret_pos = 0
                    self.update_text(content, self.editable)

                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif renpy.map_event(ev, "input_home"):
                TextInputBase.caret_pos = 0
                self.update_text(self.content, self.editable)
                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif renpy.map_event(ev, "input_end"):
                TextInputBase.caret_pos = l
                self.update_text(self.content, self.editable)
                renpy.display.render.redraw(self, 0)
                raise renpy.display.core.IgnoreEvent()

            elif self.copypaste and renpy.map_event(ev, "input_copy"):
                text = self.content.encode("utf-8")
                pygame.scrap.put(pygame.scrap.SCRAP_TEXT, text)
                raise renpy.display.core.IgnoreEvent()

            elif self.copypaste and renpy.map_event(ev, "input_paste"):
                text = pygame.scrap.get(pygame.scrap.SCRAP_TEXT)
                text = text.decode("utf-8")
                raw_text = ""
                for c in text:
                    if ord(c) >= 32:
                        raw_text += c

            # elif renpy.map_event(ev, 'input_next_input'):
            #     if self.id:
            #         inputIDs = Utils.getScreenVariable(self.availableTextInputsScreenVariableName) or []
            #         print(inputIDs)
            #         i = inputIDs.index(self.id) + 1

            #         if i == 0:
            #             return

            #         if i < 0:
            #             i = len(inputIDs) - 1
                    
            #         renpy.store.SetScreenVariable(self.activeTextInputScreenVariableName, inputIDs[i])()
            #         raise renpy.display.core.IgnoreEvent()

            # elif renpy.map_event(ev, 'input_prev_input'):
            #     if self.id:
            #         inputIDs = Utils.getScreenVariable(self.availableTextInputsScreenVariableName) or []
            #         i = inputIDs.index(self.id) - 1

            #         if i == -1:
            #             return

            #         if i > len(inputIDs) - 1:
            #             i = 0
                    
            #         renpy.store.SetScreenVariable(self.activeTextInputScreenVariableName, inputIDs[i])()
            #         raise renpy.display.core.IgnoreEvent()


            elif ev.type == pygame.TEXTEDITING:
                self.update_text(self.content, self.editable, check_size=True)

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

                for c in raw_text:

                    # Allow is given
                    if self.allow:

                        # Allow is regex
                        if isinstance(self.allow, re.Pattern):

                            # Character doesn't match
                            if self.allow.search(c) is None:
                                continue

                        # Allow is string
                        elif c not in self.allow:
                            continue

                    # Exclude is given
                    if self.exclude:

                        # Exclude is regex
                        if isinstance(self.exclude, re.Pattern):

                            # Character matches
                            if self.exclude.search(c) is not None:
                                continue

                        # Exclude is string
                        elif c in self.exclude:
                            continue

                    text += c

                if self.length:
                    remaining = self.length - len(self.content)
                    text = text[:remaining]

                if text:

                    content = self.content[0:TextInputBase.caret_pos] + text + self.content[TextInputBase.caret_pos:l]
                    TextInputBase.caret_pos += len(text)

                    self.update_text(content, self.editable, check_size=True)

                raise renpy.display.core.IgnoreEvent()

        def render(self, width, height, st, at):
            self.st = st

            rv = super(TextInputBase, self).render(width, height, st, at)

            if self.editable:
                rv.text_input = True

            return rv

        def handleClick(self, ev, x, y, st):
            def handle_click():
                if not self.editable:
                    self.enable()
                    return renpy.display.core.IgnoreEvent()

                return None

            # If clicked,
            if renpy.map_event(ev, "button_select"):
                width, height = self.width_height

                # Ensure clicked inside
                if x >= 0 and x <= width and y >= 0 and y <= height:
                    return handle_click()
                else:
                    self.disable()

            return None

    class TextInput(TextInputBase):
        pass
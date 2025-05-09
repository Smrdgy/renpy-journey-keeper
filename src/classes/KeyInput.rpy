init python in JK:
    _constant = True

    import pygame_sdl2 as pygame
    import re

    key_map = {
        pygame.K_BACKSPACE: "K_BACKSPACE",
        pygame.K_TAB: "K_TAB",
        pygame.K_CLEAR: "K_CLEAR",
        pygame.K_RETURN: "K_RETURN",
        pygame.K_PAUSE: "K_PAUSE",
        pygame.K_ESCAPE: "K_ESCAPE",
        pygame.K_SPACE: "K_SPACE",
        pygame.K_EXCLAIM: "K_EXCLAIM",
        pygame.K_QUOTEDBL: "K_QUOTEDBL",
        pygame.K_HASH: "K_HASH",
        pygame.K_DOLLAR: "K_DOLLAR",
        pygame.K_AMPERSAND: "K_AMPERSAND",
        pygame.K_QUOTE: "K_QUOTE",
        pygame.K_LEFTPAREN: "K_LEFTPAREN",
        pygame.K_RIGHTPAREN: "K_RIGHTPAREN",
        pygame.K_ASTERISK: "K_ASTERISK",
        pygame.K_PLUS: "K_PLUS",
        pygame.K_COMMA: "K_COMMA",
        pygame.K_MINUS: "K_MINUS",
        pygame.K_PERIOD: "K_PERIOD",
        pygame.K_SLASH: "K_SLASH",
        pygame.K_0: "K_0",
        pygame.K_1: "K_1",
        pygame.K_2: "K_2",
        pygame.K_3: "K_3",
        pygame.K_4: "K_4",
        pygame.K_5: "K_5",
        pygame.K_6: "K_6",
        pygame.K_7: "K_7",
        pygame.K_8: "K_8",
        pygame.K_9: "K_9",
        pygame.K_COLON: "K_COLON",
        pygame.K_SEMICOLON: "K_SEMICOLON",
        pygame.K_LESS: "K_LESS",
        pygame.K_EQUALS: "K_EQUALS",
        pygame.K_GREATER: "K_GREATER",
        pygame.K_QUESTION: "K_QUESTION",
        pygame.K_AT: "K_AT",
        pygame.K_LEFTBRACKET: "K_LEFTBRACKET",
        pygame.K_BACKSLASH: "K_BACKSLASH",
        pygame.K_RIGHTBRACKET: "K_RIGHTBRACKET",
        pygame.K_CARET: "K_CARET",
        pygame.K_UNDERSCORE: "K_UNDERSCORE",
        pygame.K_BACKQUOTE: "K_BACKQUOTE",
        pygame.K_a: "K_a",
        pygame.K_b: "K_b",
        pygame.K_c: "K_c",
        pygame.K_d: "K_d",
        pygame.K_e: "K_e",
        pygame.K_f: "K_f",
        pygame.K_g: "K_g",
        pygame.K_h: "K_h",
        pygame.K_i: "K_i",
        pygame.K_j: "K_j",
        pygame.K_k: "K_k",
        pygame.K_l: "K_l",
        pygame.K_m: "K_m",
        pygame.K_n: "K_n",
        pygame.K_o: "K_o",
        pygame.K_p: "K_p",
        pygame.K_q: "K_q",
        pygame.K_r: "K_r",
        pygame.K_s: "K_s",
        pygame.K_t: "K_t",
        pygame.K_u: "K_u",
        pygame.K_v: "K_v",
        pygame.K_w: "K_w",
        pygame.K_x: "K_x",
        pygame.K_y: "K_y",
        pygame.K_z: "K_z",
        pygame.K_DELETE: "K_DELETE",
        pygame.K_KP0: "K_KP0",
        pygame.K_KP1: "K_KP1",
        pygame.K_KP2: "K_KP2",
        pygame.K_KP3: "K_KP3",
        pygame.K_KP4: "K_KP4",
        pygame.K_KP5: "K_KP5",
        pygame.K_KP6: "K_KP6",
        pygame.K_KP7: "K_KP7",
        pygame.K_KP8: "K_KP8",
        pygame.K_KP9: "K_KP9",
        pygame.K_KP_PERIOD: "K_KP_PERIOD",
        pygame.K_KP_DIVIDE: "K_KP_DIVIDE",
        pygame.K_KP_MULTIPLY: "K_KP_MULTIPLY",
        pygame.K_KP_MINUS: "K_KP_MINUS",
        pygame.K_KP_PLUS: "K_KP_PLUS",
        pygame.K_KP_ENTER: "K_KP_ENTER",
        pygame.K_KP_EQUALS: "K_KP_EQUALS",
        pygame.K_UP: "K_UP",
        pygame.K_DOWN: "K_DOWN",
        pygame.K_RIGHT: "K_RIGHT",
        pygame.K_LEFT: "K_LEFT",
        pygame.K_INSERT: "K_INSERT",
        pygame.K_HOME: "K_HOME",
        pygame.K_END: "K_END",
        pygame.K_PAGEUP: "K_PAGEUP",
        pygame.K_PAGEDOWN: "K_PAGEDOWN",
        pygame.K_F1: "K_F1",
        pygame.K_F2: "K_F2",
        pygame.K_F3: "K_F3",
        pygame.K_F4: "K_F4",
        pygame.K_F5: "K_F5",
        pygame.K_F6: "K_F6",
        pygame.K_F7: "K_F7",
        pygame.K_F8: "K_F8",
        pygame.K_F9: "K_F9",
        pygame.K_F10: "K_F10",
        pygame.K_F11: "K_F11",
        pygame.K_F12: "K_F12",
        pygame.K_F13: "K_F13",
        pygame.K_F14: "K_F14",
        pygame.K_F15: "K_F15",
        pygame.K_NUMLOCK: "K_NUMLOCK",
        pygame.K_CAPSLOCK: "K_CAPSLOCK",
        pygame.K_SCROLLOCK: "K_SCROLLOCK",
        pygame.K_RSHIFT: "K_RSHIFT",
        pygame.K_LSHIFT: "K_LSHIFT",
        pygame.K_RCTRL: "K_RCTRL",
        pygame.K_LCTRL: "K_LCTRL",
        pygame.K_RALT: "K_RALT",
        pygame.K_LALT: "K_LALT",
        pygame.K_RMETA: "K_RMETA",
        pygame.K_LMETA: "K_LMETA",
        pygame.K_LSUPER: "K_LSUPER",
        pygame.K_RSUPER: "K_RSUPER",
        pygame.K_MODE: "K_MODE",
        pygame.K_HELP: "K_HELP",
        pygame.K_PRINT: "K_PRINT",
        pygame.K_SYSREQ: "K_SYSREQ",
        pygame.K_BREAK: "K_BREAK",
        pygame.K_MENU: "K_MENU",
        pygame.K_POWER: "K_POWER",
        pygame.K_EURO: "K_EURO",
        pygame.K_AC_BACK: "K_AC_BACK",
    }

    key_name = {
        "K_BACKSPACE": "Backspace",
        "K_TAB": "Tab",
        "K_CLEAR": "Clear",
        "K_RETURN": "Return",
        "K_PAUSE": "Pause",
        "K_ESCAPE": "Escape",
        "K_SPACE": "Space",
        "K_EXCLAIM": "!",
        "K_QUOTEDBL": "\"",
        "K_HASH": "#",
        "K_DOLLAR": "$",
        "K_AMPERSAND": "&",
        "K_QUOTE": "'",
        "K_LEFTPAREN": "(",
        "K_RIGHTPAREN": ")",
        "K_ASTERISK": "*",
        "K_PLUS": "+",
        "K_COMMA": ",",
        "K_MINUS": "-",
        "K_PERIOD": ".",
        "K_SLASH": "/",
        "K_0": "0",
        "K_1": "1",
        "K_2": "2",
        "K_3": "3",
        "K_4": "4",
        "K_5": "5",
        "K_6": "6",
        "K_7": "7",
        "K_8": "8",
        "K_9": "9",
        "K_COLON": ",",
        "K_SEMICOLON": ";",
        "K_LESS": "<",
        "K_EQUALS": "=",
        "K_GREATER": ">",
        "K_QUESTION": "?",
        "K_AT": "@",
        "K_LEFTBRACKET": "[",
        "K_BACKSLASH": "\\",
        "K_RIGHTBRACKET": "]",
        "K_CARET": "|",
        "K_UNDERSCORE": "_",
        "K_BACKQUOTE": "`",
        "K_a": "A",
        "K_b": "B",
        "K_c": "C",
        "K_d": "D",
        "K_e": "E",
        "K_f": "F",
        "K_g": "G",
        "K_h": "H",
        "K_i": "I",
        "K_j": "J",
        "K_k": "K",
        "K_l": "L",
        "K_m": "M",
        "K_n": "N",
        "K_o": "O",
        "K_p": "P",
        "K_q": "Q",
        "K_r": "R",
        "K_s": "S",
        "K_t": "T",
        "K_u": "U",
        "K_v": "V",
        "K_w": "W",
        "K_x": "X",
        "K_y": "Y",
        "K_z": "Z",
        "K_DELETE": "Del",
        "K_KP0": "0 (keypad)",
        "K_KP1": "1 (keypad)",
        "K_KP2": "2 (keypad)",
        "K_KP3": "3 (keypad)",
        "K_KP4": "4 (keypad)",
        "K_KP5": "5 (keypad)",
        "K_KP6": "6 (keypad)",
        "K_KP7": "7 (keypad)",
        "K_KP8": "8 (keypad)",
        "K_KP9": "9 (keypad)",
        "K_KP_PERIOD": ". (keypad)",
        "K_KP_DIVIDE": "/ (keypad)",
        "K_KP_MULTIPLY": "* (keypad)",
        "K_KP_MINUS": "- (keypad)",
        "K_KP_PLUS": "+ (keypad)",
        "K_KP_ENTER": "Enter (keypad)",
        "K_KP_EQUALS": "= (keypad)",
        "K_UP": "Up",
        "K_DOWN": "Down",
        "K_RIGHT": "Right",
        "K_LEFT": "Left",
        "K_INSERT": "Insert",
        "K_HOME": "Home",
        "K_END": "End",
        "K_PAGEUP": "Page up",
        "K_PAGEDOWN": "Page down",
        "K_F1": "F1",
        "K_F2": "F2",
        "K_F3": "F3",
        "K_F4": "F4",
        "K_F5": "F5",
        "K_F6": "F6",
        "K_F7": "F7",
        "K_F8": "F8",
        "K_F9": "F9",
        "K_F10": "F10",
        "K_F11": "F11",
        "K_F12": "F12",
        "K_F13": "F13",
        "K_F14": "F14",
        "K_F15": "F15",
        "K_NUMLOCK": "Numlock",
        "K_CAPSLOCK": "Capslock",
        "K_SCROLLOCK": "Scrollock",
        "K_RSHIFT": "Right shift",
        "K_LSHIFT": "Left shift",
        "K_RCTRL": "Right CTRL",
        "K_LCTRL": "Left CTRL",
        "K_RALT": "Right ALT",
        "K_LALT": "Left ALT",
        "K_RMETA": "Right Cmd/Windows key",
        "K_LMETA": "Left Cmd/Windows key",
        "K_LSUPER": "Left windows key",
        "K_RSUPER": "Right windows key",
        "K_MODE": "Mode shift",
        "K_HELP": "Help",
        "K_PRINT": "Print screen",
        "K_SYSREQ": "Sysrq",
        "K_BREAK": "Break",
        "K_MENU": "Menu",
        "K_POWER": "Power",
        "K_EURO": "Euro",
        "K_AC_BACK": "Back button (Android)",
    }

    class KeyInputButton(renpy.display.behavior.Button):
        def __init__(self, assignment=None, action=None, disabled=False, **properties):
            self.disabled = disabled

            self.setup_text(assignment)

            super(KeyInputButton, self).__init__(self.text, **properties)

            if not disabled:
                self.clicked = KeyInputButton.ToggleDetectingAction(self)
                self.action = KeyInputButton.ToggleDetectingAction(self)

            self.newKeyAction = action
            self.detecting = False

        def setup_text(self, assignment):
            text = assignment
            text_style = "keyinput_disabled_text" if self.disabled else "keyinput_text"
            if assignment == None:
                text = "[[unassigned]"
                text_style = "keyinput_disabled_text_placeholder" if self.disabled else "keyinput_text_placeholder"
            else:
                text = key_name[re.sub(r"(alt_)|(ctrl_)|(shift_)", "", assignment)]

            if text == "[":
                text = "[["

            self.text = renpy.text.text.Text(text, style=text_style)

        def set_detecting(self):
            self.detecting = True
            self.text.style = renpy.style.Style("keyinput_text_placeholder")
            self.text.set_text("[Waiting for input...]")

        def event(self, ev, x, y, st):
            if self.detecting:
                if ev.type == pygame.KEYDOWN:                    
                    if ev.key not in (pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LALT, pygame.K_RALT):
                        renpy.run(self.newKeyAction(key_map[ev.key]))

                    raise renpy.display.core.IgnoreEvent()

                return None

            return super(KeyInputButton, self).event(ev, x, y, st)

        class ToggleDetectingAction(renpy.ui.Action):
            def __init__(self, button):
                self.button = button

            def __call__(self):
                self.button.set_detecting()

    def KeyInput(assignment=None, action=None, style='keyinput', **properties):
        return KeyInputButton(assignment=assignment, action=action, style=style, **properties)

# Screen
screen JK_KeyInput(assignment=None, action=NullAction, disabled=False, supress_ctrl_warning=False, supress_no_mod_warning=False):
    vbox:
        hbox:
            add JK.KeyInput(assignment=assignment, action=action, disabled=disabled)

            use JK_Checkbox(checked="shift_" in (assignment or ""), text="Shift", action=action(assignment, shift=True), disabled=disabled or assignment == None)
            use JK_Checkbox(checked="ctrl_" in (assignment or ""), text="Ctrl", action=action(assignment, ctrl=True), disabled=disabled or assignment == None)
            use JK_Checkbox(checked="alt_" in (assignment or ""), text="Alt", action=action(assignment, alt=True), disabled=disabled or assignment == None)

            use JK_XSpacer(offset=2)

            use JK_IconButton(icon="\ue5c9", action=action(None), disabled=disabled or assignment == None, color=JK.Colors.reset, tt="Unassign")

        use JK_KeyAssignmentCheck(assignment)

        if assignment:
            if not supress_ctrl_warning and "ctrl_" in assignment:
                text "Please note that while CTRL is allowed, it may conflict with the skip action during gameplay." color (JK.Colors.disabled if disabled else JK.Colors.warning)

            if not supress_no_mod_warning and len(assignment.split("_")) == 2:
                text "Be aware, simple key shortcuts may trigger accidentally while renaming a page." color (JK.Colors.disabled if disabled else JK.Colors.warning)
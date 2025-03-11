init python in JK:
    _constant = True

    import difflib
    import unicodedata
    import re

    class SearchPlaythroughViewModel(x52NonPicklable):
        def __init__(self, search_playthroughs=False):
            self.search_playthroughs = search_playthroughs
            self.search_playthrough_names = True
            self.search_playthrough_descriptions = True
            self.search_page_names = True
            self.search_save_names = True
            self.search_choices = True
            self.search_text = ""

            self.caching = False
            self.all_playthroughs_cached = False
            self.search_after_cache_is_built = False
            self.save_names_cache = {}
            self.save_choices_cache = {}

            self.searched = False
            self.searching = False
            self.results = []

            renpy.invoke_in_thread(self.cache_saves)

        def set_search_text(self, text):
            if self.search_text == text:
                return

            self.search_text = text

            if len(text) > 0:
                self.search()

        def cache_saves(self):
            self.caching = True
            renpy.restart_interaction()

            cache_all_playthroughs = self.search_playthroughs

            playthroughs = Playthroughs.playthroughs if self.search_playthroughs else [Playthroughs.active_playthrough]
            for playthrough in playthroughs:
                self.save_names_cache[playthrough.id] = {}
                self.save_choices_cache[playthrough.id] = {}

                instance = SaveSystem.get_or_create_playthrough_save_instance_by_id(playthrough.id)

                saves_list = instance.location.list_including_inactive()
                for slotname in saves_list:
                    json = instance.location.save_json(slotname, include_inactive=True)

                    if json:
                        name = json.get("_save_name", None)
                        if name:
                            self.save_names_cache[playthrough.id][slotname] = name

                        choice = json.get("_JK_choice", None)
                        if choice:
                            self.save_choices_cache[playthrough.id][slotname] = choice


            self.all_playthroughs_cached = cache_all_playthroughs
            self.caching = False
            renpy.restart_interaction()

            if self.search_after_cache_is_built:
                self.search_after_cache_is_built = False
                self._search()

        def search(self):
            renpy.invoke_in_thread(self._search)

        def _search(self):
            if self.search_after_cache_is_built:
                return

            self.searched = True
            self.searching = True
            self.results = []
            renpy.restart_interaction()

            if self.caching:
                self.search_after_cache_is_built = True
                return

            playthroughs = Playthroughs.playthroughs if self.search_playthroughs else [Playthroughs.active_playthrough]
            for playthrough in playthroughs:
                # Playthrough names
                if self.search_playthroughs and self.search_playthrough_names:
                    is_match, rich_text = self.get_match(playthrough.name)
                    if is_match:
                        self.results.append(("PLAYTHROUGH_NAME", rich_text, playthrough))

                # Playthrough descriptions
                if self.search_playthroughs and self.search_playthrough_descriptions:
                    is_match, rich_text = self.get_match(playthrough.description)
                    if is_match:
                        self.results.append(("PLAYTHROUGH_DESCRIPTION", rich_text, playthrough))

                # Page names
                if self.search_page_names:
                    page_names = playthrough.filePageName
                    if playthrough.id == Playthroughs.active_playthrough.id:
                        page_names = renpy.store.persistent._file_page_name

                    for page, text in page_names.items():
                        is_match, rich_text = self.get_match(text)
                        if is_match:
                            self.results.append(("FILE_PAGE_NAME", rich_text, playthrough, page, text))

                # Save names
                if self.search_save_names:
                    for slotname, name in self.save_names_cache.get(playthrough.id, {}).items():
                        is_match, rich_text = self.get_match(name)
                        if is_match:
                            self.results.append(("SAVE_NAME", rich_text, playthrough, slotname))

                # Choices
                if self.search_choices:
                    for slotname, choice in self.save_choices_cache.get(playthrough.id, {}).items():
                        is_match, rich_text = self.get_match(choice)
                        if is_match:
                            self.results.append(("SAVE_CHOICE", rich_text, playthrough, slotname))

            self.searching = False
            renpy.restart_interaction()

        def get_match(self, text):
            if len(self.search_text) == 0 or text is None:
                return False, ""

            return self.fuzzy_match(text, self.search_text)

        @staticmethod
        def fuzzy_match(s1, s2, threshold=0.6):
            def normalize(text):
                return ''.join(
                    c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c)
                ).lower()
            
            def tokenize_with_indices(text):
                return [(m.group(), m.start(), m.end()) for m in re.finditer(r'[^\s.,\n\r]+', text)]
            
            def is_inside_brackets(text, index):
                """Check if the given index is inside curly brackets."""
                inside = False
                for i, char in enumerate(text):
                    if char == '{':
                        inside = True
                    elif char == '}':
                        inside = False
                    if i == index:
                        return inside
                return False
            
            s1_norm, s2_norm = normalize(s1), normalize(s2)
            words1 = tokenize_with_indices(s1)
            words2 = [normalize(word) for word, _, _ in tokenize_with_indices(s2)]
            
            matching_indices = []
            for word1, start, end in words1:
                for word2 in words2:
                    if word2[0] != s2 and len(word2) == 1:
                        continue

                    matcher = difflib.SequenceMatcher(None, normalize(word1), word2)
                    for match in matcher.get_matching_blocks():
                        if match.size > 0 and (matcher.ratio() >= threshold or word2 in normalize(word1)):
                            matching_indices.append((start + match.a, start + match.a + match.size))

            if not matching_indices:
                return False, ""
            
            # Add highlight around matching parts while avoiding curly brackets
            formatted_s1 = ""
            last_index = 0
            for start, end in sorted(matching_indices):
                if is_inside_brackets(s1, start):
                    formatted_s1 += s1[last_index:end]
                else:
                    formatted_s1 += s1[last_index:start] + "{b}" + s1[start:end] + "{/b}"
                last_index = end
            formatted_s1 += s1[last_index:]
            
            return True, formatted_s1

        class SetSearchEnabledAction(renpy.ui.Action):
            def __init__(self, view_model, key):
                self.view_model = view_model
                self.key = key

            def __call__(self):
                setattr(self.view_model, self.key, not getattr(self.view_model, self.key))

                if self.key == "search_playthroughs" and self.view_model.search_playthroughs and not self.view_model.all_playthroughs_cached:
                    renpy.invoke_in_thread(self.view_model.cache_saves)

                self.view_model.search()

                renpy.restart_interaction()

        class SetSearchAllAction(renpy.ui.Action):
            def __init__(self, view_model, enabled):
                self.view_model = view_model
                self.enabled = enabled

            def __call__(self):
                self.view_model.search_playthroughs = self.enabled

                if self.enabled and not self.view_model.all_playthroughs_cached:
                    renpy.invoke_in_thread(self.view_model.cache_saves)

                self.view_model.search()

                renpy.restart_interaction()

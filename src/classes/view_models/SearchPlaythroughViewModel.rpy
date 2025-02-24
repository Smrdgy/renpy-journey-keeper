init python in JK:
    _constant = True

    import difflib
    import unicodedata
    import re

    class SearchPlaythroughViewModel(x52NonPicklable):
        def __init__(self):
            self.search_playthrough_names = False #TODO
            self.search_playthrough_descriptions = False #TODO
            self.search_page_names = True
            self.search_save_names = True
            self.search_choices = True
            self.search_text = ""

            self.caching = False
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

            saves_list = SaveSystem.multilocation.list()

            for slotname in saves_list:
                json = SaveSystem.multilocation.json(slotname)

                name = json.get("_save_name", None)
                if name:
                    self.save_names_cache[slotname] = name

                choice = json.get("_JK_choice", None)
                if choice:
                    self.save_choices_cache[slotname] = choice

            self.caching = False
            renpy.restart_interaction()

            if self.search_after_cache_is_built:
                self._search()

        def search(self):
            renpy.invoke_in_thread(self._search)

        def _search(self):
            self.searched = True
            self.searching = True
            self.results = []
            renpy.restart_interaction()

            if self.caching:
                self.search_after_cache_is_built = True

            playthrough = Playthroughs.activePlaythrough

            # Playthroughs names
            # if self.search_playthrough_names:
            #     is_match, rich_text = self.get_match(playthrough.name)
            #     if is_match:
            #         self.results.append(("PLAYTHROUGH_NAME", rich_text, playthrough))

            # Playthroughs descriptions
            # if self.search_playthrough_descriptions:
            #     is_match, rich_text = self.get_match(playthrough.description)
            #     if is_match:
            #         self.results.append(("PLAYTHROUGH_DESCRIPTION", rich_text, playthrough))

            # Page names
            if self.search_page_names:
                page_names = playthrough.filePageName
                if playthrough.id == Playthroughs.activePlaythrough.id:
                    page_names = renpy.store.persistent._file_page_name

                for page, text in page_names.items():
                    is_match, rich_text = self.get_match(text)
                    if is_match:
                        self.results.append(("FILE_PAGE_NAME", rich_text, page, text))

            # Save names
            if self.search_save_names:
                for slotname, name in self.save_names_cache.items():
                    is_match, rich_text = self.get_match(name)
                    if is_match:
                        self.results.append(("SAVE_NAME", rich_text, slotname))

            # Choices
            if self.search_choices:
                for slotname, choice in self.save_choices_cache.items():
                    is_match, rich_text = self.get_match(choice)
                    if is_match:
                        self.results.append(("SAVE_CHOICE", rich_text, slotname))

            self.searching = False
            renpy.restart_interaction()

        def get_match(self, text):
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

        class SetSearchEnabled(renpy.ui.Action):
            def __init__(self, viewModel, key):
                self.viewModel = viewModel
                self.key = key

            def __call__(self):
                setattr(self.viewModel, self.key, not getattr(self.viewModel, self.key))

                self.viewModel.search()

                renpy.restart_interaction()
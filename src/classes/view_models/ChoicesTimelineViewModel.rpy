init 1 python in URPS:
    _constant = True

    import threading
    import time
    import zipfile
    import os

    class ChoicesTimelineViewModel(x52NonPicklable):
        def __init__(self, playthrough):
            self.playthrough = playthrough
            self.timeline = []
            self.loading = True
            self.loaded = 0
            self.to_load = 0
            self.error = None
            self.slots = []

            self.load_thread = None  # To track the loading thread

            self.load_timeline()

        def load_timeline(self):
            self.loading = True
            self.loaded = 0

            instance = SaveSystem.getPlaythroughSaveInstance(self.playthrough.id)
            instance.location.scan()

            self.slots = Utils.getSortedSaves()
            self.to_load = len(self.slots)

            renpy.restart_interaction()

            # Create a thread to load the saves to avoid blocking the main thread
            self.load_thread = threading.Thread(target=self.process_loading_start, args=(instance,))
            self.load_thread.daemon = True
            self.load_thread.start()

        def process_loading_start(self, instance):
            i = 0
            renpy.restart_interaction()

            time.sleep(0.1)

            for slot in self.slots:
                json = instance.location.json(slot)

                self.timeline.append((i, json.get("_URPS_choice", None), slot))

                self.loaded += 1
                renpy.restart_interaction()

                i += 1

                time.sleep(0.005)

            self.loading = False
            renpy.restart_interaction()

        class ExportTimelineToFile(renpy.ui.Action):
            def __init__(self, viewModel):
                self.timeline = viewModel.timeline
                self.playthrough = viewModel.playthrough

            def __call__(self):
                import os

                filename = self.playthrough.name + " timeline.txt"
                dirPath = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
                path = os.path.normpath(os.path.join(dirPath, filename))

                with open(path, 'w') as f:
                    for item in self.timeline:
                        f.write( str(item[0] + 1) + ". " + "    (" + item[2] + ")     " + self.__replace_tags(item[1] or "-") + "\n")

                showConfirm(
                    title="Timeline exported into the game files",
                    message="You can find the file in " + path,
                    yes=OpenDirectoryAction(path=dirPath),
                    yesText="Open location",
                    yesIcon='\ue2c8',
                    noText="Close",
                    noIcon=None
                )
            
            def __replace_tags(self, text):
                # Define the pattern to match tags like {tag}content{/tag}
                pattern = r'\{(.*?)\}(.*?)\{\/(.*?)\}'
                # Replace all occurrences of the pattern with just the content inside the tags
                result = re.sub(pattern, r'\2', text)

                return result.replace('[[', '[')
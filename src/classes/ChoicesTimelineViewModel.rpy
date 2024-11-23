init 1 python in SSSSS:
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
            try:
                i = 0
                for slot in self.slots:
                    location = instance.location.newest(slot)

                    if not location:
                        self.timeline.append((i, None, slot))
                    else:
                        path = location.filename(slot)

                        zf = zipfile.ZipFile(path, 'r', zipfile.ZIP_DEFLATED)

                        try:
                            choice = zf.read("choice")
                            self.timeline.append((i, choice.decode("UTF-8"), slot))
                        except Exception:
                            self.timeline.append((i, None, slot))

                        zf.close()

                        self.loaded += 1
                        renpy.restart_interaction()

                        i += 1

                        time.sleep(0.005)

            except Exception as e:
                print(e)
                self.loading = False
                self.error = "An error occurred while reading saves:\n{color=[SSSSS.Colors.error]}" + str(e) + "{/color}"
                renpy.restart_interaction()
                return

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
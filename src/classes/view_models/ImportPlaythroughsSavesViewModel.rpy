init python in JK:
    _constant = True
    import threading
    import time
    import os
    import shutil

    class ImportPlaythroughsSavesViewModel(x52NonPicklable):
        def __init__(self, source_game_name, playthroughs):
            # playthroughs is a list of (source_directory, destination_playthrough) tuples;
            # source_directory is the playthrough's directory name in the OTHER game.
            self.source_game_name = source_game_name
            self.playthroughs = playthroughs

            self.processing = False
            self.processed = 0
            self.saves_to_process = []
            self.error = None
            self.success = None

            self.save_thread = None
            self._last_progress_notify = 0.0

        def source_root(self):
            # Every JK-enabled game shares the same root ("JK"'s parent), each in
            # its own subfolder named after its native Ren'Py save_directory.
            return os.path.normpath(os.path.join(UserDir.root_path(), "..", self.source_game_name))

        def process_start(self):
            self.processing = True
            self.processed = 0
            self.error = None
            self._last_progress_notify = 0.0

            work = []
            source_root = self.source_root()

            for source_directory, destination_playthrough in self.playthroughs:
                source_dir = os.path.join(source_root, source_directory)
                if not os.path.isdir(source_dir):
                    continue

                destination_instance = SaveSystem.get_or_create_playthrough_save_instance(destination_playthrough)

                try:
                    filenames = os.listdir(source_dir)
                except Exception as e:
                    print(e)
                    continue

                for filename in filenames:
                    if filename.endswith(renpy.savegame_suffix):
                        work.append((filename, source_dir, destination_instance))

            self.saves_to_process = work

            renpy.restart_interaction()

            self.process_next_save()

        def process_next_save(self):
            if not self.processing:
                return

            if self.processed >= len(self.saves_to_process):
                self.process_done()
                return

            filename, source_dir, destination_instance = self.saves_to_process[self.processed]

            self.save_thread = threading.Thread(target=self.copy_save_and_continue, args=(filename, source_dir, destination_instance))
            self.save_thread.daemon = True
            self.save_thread.start()

        def copy_save_and_continue(self, filename, source_dir, destination_instance):
            try:
                source_path = os.path.join(source_dir, filename)

                with disk_lock:
                    for location in destination_instance.location.locations:
                        shutil.copyfile(source_path, os.path.join(location.directory, filename))

                self.process_continue()
            except Exception as e:
                print(e)
                self.error = "An error occurred while copying save \"" + filename + "\":\n{color=[JK.Colors.error]}" + str(e) + "{/color}"
                renpy.restart_interaction()
                self.process_stop()

        def process_continue(self):
            self.processed += 1
            self._notify_progress()

            self.process_next_save()

        def _notify_progress(self, force=False):
            now = time.time()
            if force or now - self._last_progress_notify >= 0.05:
                self._last_progress_notify = now
                renpy.restart_interaction()

        def process_stop(self, success=False):
            self.success = success
            self.processed = 0
            self.processing = False

            renpy.restart_interaction()

            if self.save_thread and self.save_thread.is_alive():
                self.save_thread.join()

            SaveSystem.multilocation.scan()

        def process_done(self):
            self.success = True
            self.processing = False

            SaveSystem.multilocation.scan()
            renpy.restart_interaction()

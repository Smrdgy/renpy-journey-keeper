init python in JK:
    _constant = True
    _urllib_request = None
    _urllib_error = None

    import json
    import re
    import os
    import shutil

    class UpdaterClass(x52NonPicklable):
        asset_name = "JK.rpa"
        temp_asset_name = asset_name + ".temp"

        mod_path = os.path.join(renpy.config.gamedir, asset_name)
        download_path = os.path.join(renpy.config.gamedir, temp_asset_name)

        url = "https://api.github.com/repos/{}/{}/releases/latest".format(MOD_GITHUB_OWNER, MOD_GITHUB_REPO)

        unavailable = False

        def __init__(self):
            self.pending_update = None
            self.loading = False
            self.asset_url = None
            self.checked_for_update = False
            self.downloading = False
            self.installing = False
            self.installed = False
            self.error = None
            self.latest = None
            self.rpa_locked_exception = False
            self.pending_utter_restart = False
            self.reload_and_update = False

            if os.path.exists(self.download_path):
                if renpy.store.persistent.JK_TriedUtterRestart:
                    print("Found temp update file \"{}\" even after attempted reload. This shouldn't happen. Either the file is locked by another program or there is a bug in the update system.".format(self.download_path))
                else:
                    print("Found temp update file \"{}\". Attempting to update...".format(self.download_path))
                    self.install_update()
                    self.pending_utter_restart = True

        def has_latest_version(self):
            return self.compare_versions(self.latest.version, MOD_VERSION) >= 0 if self.latest else None

        def check_for_update(self, ignore_blacklist=False, ignore_force_auto_update=False):
            if self.loading or self.unavailable:
                return
            
            self.checked_for_update = True

            self.pending_update = None
            self.latest = None
            self.error = None
            renpy.restart_interaction()

            self.latest = self.fetch_latest_release()
            if self.latest:
                version = self.latest.version
                if not self.has_latest_version() and (ignore_blacklist or renpy.store.persistent.JK_IgnoredUpdate != version):
                    self.pending_update = self.latest

                    if self.pending_update.asset:
                        if Settings.autoUpdateWithoutPrompt and not ignore_force_auto_update:
                            Updater.InstallUpdateAction(self.latest)()
                        elif not Settings.noUpdatePrompt and renpy.get_screen("JK_Settings_Updater") is None:
                            renpy.show_screen("JK_PendingUpdate", self.latest)


        def fetch_latest_release(self):
            self.loading = True
            self.error = None
            renpy.restart_interaction()

            print("Fetching metadata from: ", self.url)

            try:
                request = _urllib_request.Request(self.url)
                request.add_header("Accept", "application/vnd.github.v3+json")

                response = _urllib_request.urlopen(request)
                json_string = response.read()
                return Updater.Release(json.loads(json_string))
 
            # HTTP error
            except _urllib_error.HTTPError as e:
                print("HTTP error occurred while downloading update metadata: ", e)
                self.error = "A HTTP error occurred while downloading update information: {color=[JK.Colors.error]}" + Utils.escape_renpy_reserved_characters(str(e)) + "{/color}"

            # URL error
            except _urllib_error.URLError as e:
                print("URL error occurred while downloading update metadata: ", e)
                self.error = "A URL error occurred while downloading update information: {color=[JK.Colors.error]}" + Utils.escape_renpy_reserved_characters(str(e)) + "{/color}"

            # Unexpected error
            except Exception as e:
                print("An error occurred while downloading update metadata: ", e)
                self.error = "An unexpected error occurred while downloading update information: {color=[JK.Colors.error]}" + Utils.escape_renpy_reserved_characters(str(e)) + "{/color}"

            finally:
                self.loading = False
                renpy.restart_interaction()

            return None

        def download_and_install_update(self, release=None):
            if self.download_asset(release):
                self.installing = True
                self.installed = False
                renpy.restart_interaction()

                self.install_update()

        def install_update(self):
            path = self.mod_path

            if os.path.islink(self.mod_path):
                # File is a simlink

                try:
                    path = os.path.realpath(self.mod_path)
                except Exception as e:
                    print("Error resolving symlink: ", e)

            try:
                shutil.move(self.download_path, path)
                self.installing = False
                self.installed = True
                renpy.restart_interaction()
                return
            except Exception as e:
                error_message = "{color=[JK.Colors.error]}" + Utils.escape_renpy_reserved_characters(str(e)) + "{/color}"

                if e.args[0] == 13:
                    print("Unable to replace the .rpa file, Ren'Py or other program is blocking the file.")
                    renpy.store.persistent.JK_TriedUtterRestart = False
                    self.rpa_locked_exception = True
                    self.error = "Unable to replace the .rpa file, Ren'Py or other program is blocking the file: {}".format(error_message)
                else:
                    print("Error moving file: ", e)
                    self.error = "An unexpected error occurred: {}".format(error_message)

            self.installing = False
            renpy.restart_interaction()

            renpy.notify("JK successfully updated to v" + MOD_VERSION)

        def download_asset(self, release):
            release = release or self.latest

            self.downloading = True
            self.error = None

            if os.path.exists(self.download_path):
                os.unlink(self.download_path)

            print("Downloadingn asset from: ", release.download_url)
            try:
                request = _urllib_request.Request(release.download_url)
                request.add_header("Accept", "application/octet-stream")

                response = _urllib_request.urlopen(request)

                with open(self.download_path, "wb") as output_file:
                    output_file.write(response.read())

                print("Downloaded asset to: ", self.download_path)

                return True

            # HTTP error
            except _urllib_error.HTTPError as e:
                print("HTTP error occurred downloading/writing the asset: ", e)
                self.error = "A HTTP error occurred while downloading/writing the asset: {color=[JK.Colors.error]}" + Utils.escape_renpy_reserved_characters(str(e)) + "{/color}"

            # URL error
            except _urllib_error.URLError as e:
                print("URL error occurred downloading/writing the asset: ", e)
                self.error = "A URL error occurred while downloading/writing the asset: {color=[JK.Colors.error]}" + Utils.escape_renpy_reserved_characters(str(e)) + "{/color}"

            # Unexpected error
            except Exception as e:
                print("An error occurred downloading/writing the asset: ", e)
                self.error = "An unexpected error occurred while downloading/writing the asset: {color=[JK.Colors.error]}" + Utils.escape_renpy_reserved_characters(str(e)) + "{/color}"
            
            finally:
                self.downloading = False
                renpy.restart_interaction()

            return False

        @staticmethod
        def compare_versions(v1, v2):
            if v1 == v2:
                return 0

            # Remove non-numeric characters
            v1 = re.sub(r"[^0-9.]", "", v1)
            v2 = re.sub(r"[^0-9.]", "", v2)

            # Split versions into parts
            v1_parts = list(map(int, v1.split(".")))
            v2_parts = list(map(int, v2.split(".")))

            for i in range(max(len(v1_parts), len(v2_parts))):
                part1 = v1_parts[i] if i < len(v1_parts) else 0
                part2 = v2_parts[i] if i < len(v2_parts) else 0

                if part1 != part2:
                    return part2 - part1

            return 0

        class Release(x52NonPicklable):
            assets_url = "https://api.github.com/repos/{}/{}/releases/assets/".format(MOD_GITHUB_OWNER, MOD_GITHUB_REPO)

            def __init__(self, data):
                self.data = data

                # Cache
                self._download_url = None
                self._changelog = None
                self._asset = None

            @property
            def version(self):
                return self.data.get("tag_name").replace("v", "")
            
            @property
            def download_url(self):
                if self._download_url:
                    return self._download_url

                asset = self._find_asset()
                if not asset:
                    return None

                self._download_url = self.assets_url + str(self.asset.get("id"))

                return self._download_url
            
            @property
            def url(self):
                return self.data.get("html_url")

            @property
            def changelog(self):
                if self._changelog:
                    return self._changelog

                self._changelog = Utils.translate_markdown(self.data.get("body"))

                return self._changelog

            @property
            def asset(self):
                if self._asset:
                    return self._asset

                self._asset = self._find_asset()

                return self._asset

            def _find_asset(self):
                assets = self.data.get("assets")
                if assets and len(assets) > 0 and assets[0]:
                    return assets[0]

        class SkipUpdateAction(renpy.ui.Action):
            def __init__(self, version):
                self.version = version

            def __call__(self):
                renpy.store.persistent.JK_IgnoredUpdate = self.version

                renpy.restart_interaction()

        class InstallLatestUpdateAction(renpy.ui.Action):
            def __call__(self):
                Updater.InstallLatestUpdateAction(Updater.latest)()
        
        class InstallUpdateAction(renpy.ui.Action):
            def __init__(self, release=None):
                self.release = release

            def __call__(self):
                if renpy.get_screen("JK_PendingUpdate") is None:
                    renpy.show_screen("JK_PendingUpdate", release=self.release)

                renpy.invoke_in_thread(Updater.download_and_install_update, release=self.release)
                renpy.restart_interaction()

        class DisableUpdatesAction(renpy.ui.Action):
            def __call__(self):
                showConfirm(
                    title="Disable updates",
                    message="Do you really wish to disable automatic checking for the updates?\n{color=[JK.Colors.info]}You can re-enable it in the settings at any time.{/color}",
                    yes=Settings.ToggleEnabledAction("updaterEnabled"),
                    yes_icon="\ue888",
                    yes_color=Colors.error
                )
        
        class CheckForUpdateAction(renpy.ui.Action):
            def __call__(self):
                Updater.check_for_update(ignore_blacklist=True, ignore_force_auto_update=True)

        class RestartGameAction(renpy.ui.Action):
            def __call__(self):
                if renpy.get_screen("JK_PendingUpdate") is None:
                    renpy.show_screen("JK_PendingUpdate", release=Updater.pending_update)

                Updater.reload_and_update = True
                renpy.restart_interaction()

    try:
        import urllib2 as _urllib_request
        import urllib2 as _urllib_error
    except:
        try:
            import ssl
            ssl._create_default_https_context = ssl._create_unverified_context

            from urllib import request as _urllib_request
            from urllib import error as _urllib_error
        except Exception as e:
            UpdaterClass.unavailable = True
            print("No urllib present. JK updater disabled")
            pass
init 1 python in URPS:
    _constant = True
    _urllib_request = None
    _urllib_error = None

    import json
    import re
    import os
    import shutil

    class UpdaterClass(x52NonPicklable):
        asset_name = MOD_NAME + ".rpa"

        mod_path = os.path.join(renpy.config.gamedir, asset_name)
        download_path = mod_path + ".temp"

        url = "https://api.github.com/repos/{}/{}/releases/latest".format(MOD_GITHUB_OWNER, MOD_GITHUB_REPO)
        download_url = "https://api.github.com/repos/{}/{}/releases/assets/".format(MOD_GITHUB_OWNER, MOD_GITHUB_REPO)

        authorization = "Bearer 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"#TODO: Remove when the repo becomes public

        unavailable = False

        @property
        def latest_version(self):
            if self.latest:
                return self.latest.get("tag_name")

            return "N/A"

        @property
        def latest_html_url(self):
            if self.latest:
                return self.latest.get("html_url")

            return "https://github.com/repos/{}/{}/releases".format(MOD_GITHUB_OWNER, MOD_GITHUB_REPO)

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

        def check_for_update(self, ignore_blacklist=False, ignore_force_auto_update=False):
            if self.loading or self.unavailable:
                return
            
            self.checked_for_update = True

            self.pending_update = None
            self.asset_id = None
            self.latest = None
            renpy.restart_interaction()

            self.latest = self.fetch_latest_release()
            if self.latest:
                version = self.latest.get("tag_name")
                if version != MOD_VERSION and (ignore_blacklist or renpy.store.persistent.URPS_IgnoredUpdate != version):
                    self.pending_update = self.latest

                    assets = self.pending_update.get("assets")
                    if assets and len(assets) > 0 and assets[0]:
                        self.asset_id = assets[0].get("id")

                        if Settings.autoUpdateWithoutPrompt and not ignore_force_auto_update:
                            Updater.InstallUpdateAction(version)()
                        else:
                            renpy.show_screen("URPS_PendingUpdate", version=version, changelog=self.translate_markdown(self.latest.get("body")))


        def fetch_latest_release(self):
            self.loading = True
            self.error = None
            renpy.restart_interaction()

            print("Fetching metadata from: ", self.url)

            try:
                request = _urllib_request.Request(self.url)
                request.add_header("Authorization", self.authorization)
                request.add_header("Accept", "application/vnd.github.v3+json")

                response = _urllib_request.urlopen(request)
                json_string = response.read()
                data = json.loads(json_string)

                self.loading = False
                renpy.restart_interaction()
 
                return data
            except _urllib_error.HTTPError as e:
                print("HTTP error occurred: ", e)
                self.error = "A HTTP error occurred: {color=[URPS.Colors.error]}" + Utils.replaceReservedCharacters(str(e)) + "{/color}"
            except _urllib_error.URLError as e:
                print("URL error occurred: ", e)
                self.error = "A URL error occurred: {color=[URPS.Colors.error]}" + Utils.replaceReservedCharacters(str(e)) + "{/color}"
            except Exception as e:
                print("An error occurred: ", e)
                self.error = "An unexpected error occurred: {color=[URPS.Colors.error]}" + Utils.replaceReservedCharacters(str(e)) + "{/color}"

            self.loading = False
            renpy.restart_interaction()

            return None

        def download_and_install_latest_update(self):
            if self.download_asset():
                self.installing = True
                self.installed = False
                renpy.restart_interaction()

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
                    return True
                except Exception as e:
                    print("Error moving file: ", e)
                    self.error = "An unexpected error occurred: {color=[URPS.Colors.error]}" + Utils.replaceReservedCharacters(str(e)) + "{/color}"

            self.installing = False
            renpy.restart_interaction()
            
            return False

        def download_asset(self):
            self.downloading = True
            self.error = None
            print("Downloadingn asset from: ", self.asset_id)
            try:
                request = _urllib_request.Request(self.download_url + str(self.asset_id))
                request.add_header("Accept", "application/octet-stream")
                request.add_header("Authorization", self.authorization)

                response = _urllib_request.urlopen(request)

                with open(self.download_path, "wb") as output_file:
                    output_file.write(response.read())

                print("Downloaded asset to: ", self.download_path)
                self.downloading = False
                renpy.restart_interaction()

                return True
            except _urllib_error.HTTPError as e:
                print("HTTP error occurred: ", e)
                self.error = "A HTTP error occurred: {color=[URPS.Colors.error]}" + Utils.replaceReservedCharacters(str(e)) + "{/color}"
            except _urllib_error.URLError as e:
                print("URL error occurred: ", e)
                self.error = "A URL error occurred: {color=[URPS.Colors.error]}" + Utils.replaceReservedCharacters(str(e)) + "{/color}"
            except Exception as e:
                print("An error occurred: ", e)
                self.error = "An unexpected error occurred: {color=[URPS.Colors.error]}" + Utils.replaceReservedCharacters(str(e)) + "{/color}"

            self.downloading = False
            renpy.restart_interaction()

            return False

        def translate_markdown(self, text):
            # New lines
            text = re.sub(r'\r\n', r'\n', text, flags=re.MULTILINE)
            # Bold
            text = re.sub(r'\*\*(.*?)\*\*', r'{b}\1{/b}', text)
            # Italic
            text = re.sub(r'\*(.*?)\*', r'{i}\1{/i}', text)
            # Strikethrough
            text = re.sub(r'~~(.*?)~~', r'{s}\1{/s}', text)
            # Lists
            text = re.sub(r'^- (.*?)$', r'    - \1', text, flags=re.MULTILINE)
            # Links
            text = re.sub(r'\[(.*?)\]\((.*?)\)', r'{a=\1}\2{/a}', text)
            # Inline code
            text = re.sub(r'`(.*?)`', r'\1', text)
            # Block code
            text = re.sub(r'```(.*?)```', r'\1', text, flags=re.DOTALL)
            # Interpolation [...]
            text = Utils.replaceReservedCharacters(text)
            # Headers
            text = re.sub(r'^# (.*?)$', r'{color=[URPS.Colors.theme]}{b}\1{/b}{/color}', text, flags=re.MULTILINE)
            text = re.sub(r'^## (.*?)$', r'{color=[URPS.Colors.theme]}{i}\1{/i}{/color}', text, flags=re.MULTILINE)
            text = re.sub(r'^### (.*?)$', r'{color=[URPS.Colors.theme]}\1{/color}', text, flags=re.MULTILINE)

            return text

        class SkipUpdateAction(renpy.ui.Action):
            def __init__(self, version):
                self.version = version

            def __call__(self):
                renpy.store.persistent.URPS_IgnoredUpdate = self.version

                renpy.restart_interaction()
        
        class InstallUpdateAction(renpy.ui.Action):
            def __call__(self):
                renpy.invoke_in_thread(Updater.download_and_install_latest_update)
                renpy.restart_interaction()

        class DisableUpdatesAction(renpy.ui.Action):
            def __call__(self):
                showConfirm(
                    title="Disable updates",
                    message="Do you really wish to disable automatic checking for the updates?\n{color=[URPS.Colors.info]}You can re-enable it in the settings at any time.{/color}",
                    yes=Settings.ToggleUpdaterEnabled(),
                    yesIcon="\ue888",
                    yesColor=Colors.error
                )
        
        class CheckForUpdateAction(renpy.ui.Action):
            def __call__(self):
                Updater.check_for_update(ignore_blacklist=True, ignore_force_auto_update=True)

        class RestartGame(renpy.ui.Action):
            def __call__(self):
                renpy.utter_restart()

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
            print("No urllib present. URPS updater disabled")
            pass
init python in JK:
    _constant = True

    class ReleasesViewModel(x52NonPicklable):
        url = "https://api.github.com/repos/{}/{}/releases".format(MOD_GITHUB_OWNER, MOD_GITHUB_REPO)

        def __init__(self):
            self.loading = False
            self.error = None
            self.releases = []

        def fetch_all_releases(self):
            self.loading = True
            self.error = None
            renpy.restart_interaction()

            print("Fetching releases from: ", self.url)

            try:
                request = _urllib_request.Request(self.url)
                request.add_header("Accept", "application/vnd.github.v3+json")

                response = _urllib_request.urlopen(request)
                json_string = response.read()
                data = json.loads(json_string)

                for release_data in data:
                    self.releases.append(Updater.Release(release_data))

            # HTTP error
            except _urllib_error.HTTPError as e:
                print("HTTP error occurred while downloading releases: ", e)
                self.error = "A HTTP error occurred while downloading releases: {color=[JK.Colors.error]}" + Utils.escape_renpy_reserved_characters(str(e)) + "{/color}"

            # URL error
            except _urllib_error.URLError as e:
                print("URL error occurred while downloading releases: ", e)
                self.error = "A URL error occurred while downloading releases: {color=[JK.Colors.error]}" + Utils.escape_renpy_reserved_characters(str(e)) + "{/color}"

            # Unexpected error
            except Exception as e:
                print("An error occurred while downloading releases: ", e)
                self.error = "An unexpected error occurred while downloading releases: {color=[JK.Colors.error]}" + Utils.escape_renpy_reserved_characters(str(e)) + "{/color}"

            finally:
                self.loading = False
                renpy.restart_interaction()
            
init -999 python in SSSSS:
    class AutosaverClass():
        class HandlePress(renpy.ui.Action):
            def __init__(self):
                self.isDisplayingChoice = Choices.isDisplayingChoice

            def __call__(self):
                if(self.isDisplayingChoice and Playthroughs.activePlaythrough.autosaveOnChoices):
                    # If the save slot is not bigger than the very last one, do once a confirm whether to disable autosaving

                    renpy.exports.take_screenshot()
                    renpy.save("1-4")
                    # If this becomes laggy, check the autosave system and its threading
                    
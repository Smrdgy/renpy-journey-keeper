init python in JK:
    _constant = True

    class EditSaveViewModel(x52NonPicklable):
        def __init__(self, slotname, location=None):
            self.location = location
            self.slotname = slotname

            self.save_json = (location or SaveSystem.multilocation).json(slotname)

            self.name = self.save_json.get("_save_name")
            self.choice = self.save_json.get("_JK_choice")

        def save(self):
            json = self.save_json.copy()
            if self.name:
                json['_save_name'] = Utils.replaceReservedCharacters(self.name)
            if self.choice:
                json['_JK_choice'] = Utils.replaceReservedCharacters(self.choice)

            (self.location or SaveSystem.multilocation).edit_json(self.slotname, json)

        class Save(renpy.ui.Action):
            def __init__(self, view_model, name, choice):
                self.view_model = view_model
                self.name = name
                self.choice = choice

            def __call__(self):
                self.view_model.name = self.name
                self.view_model.choice = self.choice
                self.view_model.save()
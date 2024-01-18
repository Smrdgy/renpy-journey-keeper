init 51 python in SSSSS:
    _constant = True

    Playthroughs = PlaythroughsClass()
    SaveSystem = SaveSystemClass()
    Choices = ChoicesDetectorClass()
    Autosaver = AutosaverClass()
    AutosaverCounter = renpy.store.autosaveCounter = AutosaveCounterClass()

    def afterLoad():
        renpy.show_screen('SSSSS_Overlay')

init 999 python:
    if not 'SSSSSoverlay' in config.layers: config.layers.append('SSSSSoverlay') 

    renpy.config.after_load_callbacks.append(SSSSS.afterLoad)
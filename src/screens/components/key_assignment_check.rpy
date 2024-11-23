screen SSSSS_KeyAssignmentCheck(assignment):
    python:
        conflicts = []

        for key in renpy.config.keymap:
            item = renpy.config.keymap[key]

            if item and assignment in item:
                # if assignment in keys:
                conflicts.append(key)

    if len(conflicts) > 0:
        vbox:
            text "Conflicting mapping(s):" color SSSSS.Colors.warning
            
            hbox:
                hbox xsize 20

                vbox:
                    for conflict in conflicts:
                        text conflict

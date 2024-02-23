screen SSSSS_Checkbox(checked, text, action=None, xsize=None, sensitive=None):
    style_prefix 'SSSSS'

    button:
        xsize xsize
        sensitive sensitive
        action action

        hbox:
            frame yalign .5:
                style "SSSSS_checkbox_box"

                frame:
                    align (0.5, 0.5)

                    if checked:
                        style "SSSSS_checkbox_box_checked"
                    elif checked == None:
                        style "SSSSS_checkbox_box_unchecked" #"SSSSS_checkbox_box_indeterminate"
                    else:
                        style "SSSSS_checkbox_box_unchecked"
            
            if text:
                text text yalign .5
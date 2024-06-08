screen SSSSS_Checkbox(checked, text, action=None, xsize=None, sensitive=None, disabled=False):
    style_prefix 'SSSSS'

    button:
        xsize xsize
        sensitive sensitive
        action (None if disabled else action)

        hbox:
            if checked:
                use sssss_icon("\ue834", color='#2f2f2f55' if disabled else None)
            # elif checked == None:
            #     use sssss_icon("\ue909") #Indetermined
            else:
                use sssss_icon("\ue835", color='#2f2f2f55' if disabled else None)
            
            if text:
                text text yalign .5:
                    if disabled:
                        color '#2f2f2f55'
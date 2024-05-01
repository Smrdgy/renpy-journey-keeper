screen SSSSS_Checkbox(checked, text, action=None, xsize=None, sensitive=None):
    style_prefix 'SSSSS'

    button:
        xsize xsize
        sensitive sensitive
        action action

        hbox:
            if checked:
                use sssss_icon("\ue834")
            # elif checked == None:
            #     use sssss_icon("\ue909") #Indetermined
            else:
                use sssss_icon("\ue835")
            
            if text:
                text text yalign .5
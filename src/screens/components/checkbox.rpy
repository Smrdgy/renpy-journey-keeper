screen x52URM_checkbox(checked, text, action=None, xsize=None, sensitive=None, checkedIcon='\ue834', uncheckedIcon='\ue835', indeterminateIcon='\ue909'):
    style_prefix 'x52URM'

    button:
        xsize xsize
        sensitive sensitive
        action action
        hbox:
            hbox xsize x52URM.scalePxInt(30) yalign .5: # We want this size fixed, to prevent resizing on icon change
                if checked:
                    use sssss_icon(checkedIcon)
                elif checked == False:
                    use sssss_icon(uncheckedIcon)
                else:
                    use sssss_icon(indeterminateIcon)
            
            if text:
                text text style_suffix 'button_text' yalign .5
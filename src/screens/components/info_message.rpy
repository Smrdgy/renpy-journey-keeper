screen SSSSS_InfoBox(text):
    button: # Prevent any hover effects
        action None

        hbox:
            use sssss_icon('\ue88e', color = SSSSS.Colors.info)

            hbox xsize 10

            text text color SSSSS.Colors.info yalign 0.5
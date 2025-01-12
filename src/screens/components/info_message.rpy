screen JK_InfoBox(text):
    button: # Prevent any hover effects
        action None

        hbox:
            use JK_Icon('\ue88e', color = JK.Colors.info)

            hbox xsize 10

            text text color JK.Colors.info yalign 0.5
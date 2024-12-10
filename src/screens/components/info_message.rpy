screen URPS_InfoBox(text):
    button: # Prevent any hover effects
        action None

        hbox:
            use URPS_Icon('\ue88e', color = URPS.Colors.info)

            hbox xsize 10

            text text color URPS.Colors.info yalign 0.5
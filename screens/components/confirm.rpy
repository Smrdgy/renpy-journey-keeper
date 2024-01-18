screen SSSSS_Confirm(title="", message="", yes=None, no=None, yesText="Yes", noText="No"):
    modal True

    zorder 199

    frame:
        xfill True
        yfill True
        background '#000'

        vbox:
            xalign 0.5
            yalign 0.5

            text title xalign 0.5

            null height 10

            text message xalign 0.5

            null height 20

            hbox:
                xalign 0.5

                textbutton yesText:
                    action [yes, Hide("SSSSS_Confirm")]

                null width 100

                textbutton noText:
                    action [no, Hide("SSSSS_Confirm")]

init python in SSSSS:
    def showConfirm(title="", message="", yes=None, no=None, yesText="Yes", noText="No"):
        renpy.run(renpy.store.Show("SSSSS_Confirm", title=title, message=message, yes=yes, no=no, yesText=yesText, noText=noText))
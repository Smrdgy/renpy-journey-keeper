screen URPS_ConfirmSizeAdjustment():
    layer 'URPS_Overlay'

    default time = 60

    python:
        class RevertSizeAdjustmentValue(renpy.ui.Action):
            def __call__(self):
                URPS.Settings.SetSizeAdjustment(value=renpy.store.persistent.URPS_SizeAdjustmentRollbackValue, store_rollback_value=False)()
                renpy.store.persistent.URPS_SizeAdjustmentRollbackValue = None
                renpy.save_persistent()
                renpy.notify("Previous size applied. Restart the game to see the changes.")

        class ConfirmSizeAdjustment(renpy.ui.Action):
            def __call__(self):
                renpy.store.persistent.URPS_SizeAdjustmentRollbackValue = None
                renpy.save_persistent()

    timer 1 repeat True action If(time > 0, true=SetScreenVariable('time', time - 1), false=[RevertSizeAdjustmentValue(), Hide('URPS_ConfirmSizeAdjustment')])

    drag:
        draggable True
        drag_handle (0, 0, 1.0, 1.0)
        xpos 10
        ypos 10
        droppable False

        frame style "URPS_default":
            background "#000000cc"
            padding (10, 10, 10, 10)

            vbox:
                text "Adjustment confirmation" color URPS.Colors.theme xalign 0.5

                vbox ysize 5

                text "{size=-10}After 60 seconds, the previous size will be applied.{/size}" xalign 0.5

                vbox ysize 20

                text "[time]s" xalign 0.5 color (URPS.Colors.error if time < 5 else "#fff")

                hbox xalign 0.5:
                    textbutton "Revert" action [RevertSizeAdjustmentValue(), Hide('URPS_ConfirmSizeAdjustment')] text_color URPS.Colors.error text_hover_color URPS.Colors.hover

                    hbox xsize 100

                    textbutton "Confirm" action [ConfirmSizeAdjustment(), Hide('URPS_ConfirmSizeAdjustment')] text_color URPS.Colors.success text_hover_color URPS.Colors.hover


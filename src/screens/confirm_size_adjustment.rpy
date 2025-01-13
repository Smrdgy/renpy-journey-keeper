screen JK_ConfirmSizeAdjustment():
    layer 'JK_Overlay'
    zorder 99999

    default time = 60

    python:
        class RevertSizeAdjustmentValue(renpy.ui.Action):
            def __call__(self):
                JK.Settings.SetSizeAdjustment(value=renpy.store.persistent.JK_SizeAdjustmentRollbackValue, store_rollback_value=False)()
                renpy.store.persistent.JK_SizeAdjustmentRollbackValue = None
                renpy.save_persistent()
                renpy.store.gui.rebuild()
                renpy.notify("Previous size applied.")

        class ConfirmSizeAdjustment(renpy.ui.Action):
            def __call__(self):
                renpy.store.persistent.JK_SizeAdjustmentRollbackValue = None
                renpy.save_persistent()

    timer 1 repeat True action If(time > 0, true=SetScreenVariable('time', time - 1), false=[RevertSizeAdjustmentValue(), Hide('JK_ConfirmSizeAdjustment')])

    drag:
        draggable True
        drag_handle (0, 0, 1.0, 1.0)
        xpos 10
        ypos 10
        droppable False

        frame style "JK_default":
            background "#f00"
            padding (2, 2, 2, 2)

            frame style "JK_default":
                background "#000"
                padding (10, 10, 10, 10)

                vbox:
                    text "Adjustment confirmation" color JK.Colors.theme xalign 0.5

                    vbox ysize 5

                    text "{size=-10}After 60 seconds, the previous size will be applied.{/size}" xalign 0.5

                    vbox ysize 20

                    text "[time]s" xalign 0.5 color (JK.Colors.error if time < 5 else "#fff")

                    hbox xalign 0.5:
                        textbutton "Revert" action [RevertSizeAdjustmentValue(), Hide('JK_ConfirmSizeAdjustment')] text_color JK.Colors.error text_hover_color JK.Colors.hover

                        hbox xsize 100

                        textbutton "Confirm" action [ConfirmSizeAdjustment(), Hide('JK_ConfirmSizeAdjustment')] text_color JK.Colors.success text_hover_color JK.Colors.hover


screen URPS_Spacer(vertical=True, offset=1):
    style_prefix "URPS"

    $ direction = "y" if vertical else "x"

    vbox style_suffix "spacer_"+ direction + "_" + str(offset)

screen URPS_XSpacer(offset=1, **params):
    use URPS_Spacer(vertical=False, offset=offset, **params)

screen URPS_YSpacer(offset=1, **params):
    use URPS_Spacer(vertical=True, offset=offset, **params)
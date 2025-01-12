screen JK_Spacer(vertical=True, offset=1):
    style_prefix "JK"

    $ direction = "y" if vertical else "x"

    vbox style_suffix "spacer_"+ direction + "_" + str(offset)

screen JK_XSpacer(offset=1, **params):
    use JK_Spacer(vertical=False, offset=offset, **params)

screen JK_YSpacer(offset=1, **params):
    use JK_Spacer(vertical=True, offset=offset, **params)
screen SSSSS_Spacer(vertical=True, offset=1):
    style_prefix "SSSSS"

    $ direction = "y" if vertical else "x"

    vbox style_suffix "spacer_"+ direction + "_" + str(offset)

screen SSSSS_XSpacer(offset=1, **params):
    use SSSSS_Spacer(vertical=False, offset=offset, **params)

screen SSSSS_YSpacer(offset=1, **params):
    use SSSSS_Spacer(vertical=True, offset=offset, **params)
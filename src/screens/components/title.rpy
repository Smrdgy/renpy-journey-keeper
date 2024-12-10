screen URPS_Title(text, size=1, color=None):
    style_prefix "URPS"

    text text style_suffix "title_" + str(size):
        if color:
            color color
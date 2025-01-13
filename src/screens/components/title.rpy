screen JK_Title(text, size=1, color=None):
    style_prefix "JK"

    text text style_suffix "title_" + str(size):
        if color:
            color color
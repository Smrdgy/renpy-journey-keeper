init python in JK:
    _constant = True

    class ThumbnailCacheClass(x52NonPicklable):
        """
        A small in-memory cache for decoded/scaled thumbnail displayables.

        Screens that render many rows (playthroughs, saves, memories, ...)
        would otherwise re-decode and re-scale the same thumbnail on every
        screen restart, since a fresh displayable object is built from the
        stored bytes every call and Ren'Py's own render cache is keyed by
        displayable identity - it never gets to hit. This trades a bit of
        memory for skipping that repeated decode/scale work.
        """

        def __init__(self):
            self._cache = {}

        def get_or_build(self, key, builder):
            cached = self._cache.get(key)
            if cached is not None:
                return cached

            value = builder()
            self._cache[key] = value

            return value

        def invalidate_prefix(self, prefix):
            for key in list(self._cache.keys()):
                if key[:len(prefix)] == prefix:
                    del self._cache[key]

        def clear(self):
            self._cache.clear()

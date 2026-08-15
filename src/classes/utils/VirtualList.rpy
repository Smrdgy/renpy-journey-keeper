init python in JK:
    _constant = True

    import bisect

    class VirtualListState(x52NonPicklable):
        """
        Holds the persistent scroll/window state for one virtualized list.

        Create exactly one instance per on-screen list via a `default`
        statement in the screen that owns the list's viewport (SLDefault
        only assigns `default` variables once per screen-scope lifetime, so
        the same instance - and its Adjustment - survives interaction
        restarts instead of resetting the scroll position every rebuild).

        Usage (uniform row height):
            $ start, end, top_px, bottom_px = vlist.compute(len(items), row_size, viewport_size)
            viewport:
                yadjustment vlist.adjustment
                vbox:
                    null height top_px
                    for item in items[start:end]:
                        ...
                    null height bottom_px

        Usage (variable row height, e.g. interleaved section headers):
            $ start, end, top_px, bottom_px = vlist.compute_variable(row_sizes, viewport_size)
        """

        def __init__(self, overscan=15, max_window=60):
            # Each rebuild triggered by scrolling past the built range costs
            # a full renpy.restart_interaction() - global, not scoped to this
            # list - so a wider overscan margin means fewer rebuilds during a
            # continuous scroll/drag, at the cost of a few more rows staying
            # built at once (still bounded well under max_window).
            self.overscan = overscan

            # Hard cap on how many rows can ever be built at once, independent
            # of the viewport_size measurement. Ren'Py sizing (ymaximum as a
            # fraction scales whatever height the parent offers, which can
            # itself be large/unbounded inside auto-sizing containers) can't
            # always be trusted to yield a small "visible" count, so this is
            # the actual guarantee that a rebuild stays cheap.
            self.max_window = max_window

            self.adjustment = renpy.ui.adjustment(value=0, range=0, page=0, changed=self._on_scroll)

            self.built_start = 0
            self.built_end = 0

            self._item_count = 0
            self._row_size = None  # None while a compute_variable() window is active
            self._viewport_size = 0
            self._header_size = 0
            self._prefix = None

        def estimate_viewport_size(self, fallback):
            # A Viewport with set_adjustments=True (the default) overwrites
            # adjustment.page with the actual rendered pixel height of the
            # visible area on every render, bypassing the `changed`
            # callback (so this doesn't trigger extra restarts). That makes
            # this a self-correcting estimate after the first paint - before
            # that, page is still 0, so pass a generous fallback (being too
            # large only means a few extra rows get built on the first
            # frame, never a visible gap).
            page = self.adjustment.page
            return page if page else fallback

        def compute(self, item_count, row_size, viewport_size, header_size=0):
            row_size = max(1, row_size)

            self._item_count = item_count
            self._row_size = row_size
            self._viewport_size = viewport_size
            self._header_size = header_size
            self._prefix = None

            total = item_count * row_size
            self.adjustment.range = max(0, header_size + total - viewport_size)

            start, end = self.__window_for_uniform(self.adjustment.value)

            self.built_start, self.built_end = start, end

            return start, end, start * row_size, (item_count - end) * row_size

        def compute_variable(self, row_sizes, viewport_size, header_size=0):
            item_count = len(row_sizes)

            prefix = [0]
            for size in row_sizes:
                prefix.append(prefix[-1] + size)

            self._item_count = item_count
            self._row_size = None
            self._viewport_size = viewport_size
            self._header_size = header_size
            self._prefix = prefix

            total = prefix[-1]
            self.adjustment.range = max(0, header_size + total - viewport_size)

            start, end = self.__window_for_variable(self.adjustment.value)

            self.built_start, self.built_end = start, end

            return start, end, prefix[start], total - prefix[end]

        def reset(self):
            self.adjustment.value = 0
            self.built_start = 0
            self.built_end = 0

        def __window_for_uniform(self, value):
            if self._item_count <= 0:
                return 0, 0

            scroll_in_list = max(0, value - self._header_size)
            first = int(scroll_in_list // self._row_size)
            visible = int(self._viewport_size // self._row_size) + 2
            visible = min(visible, self.max_window)

            start = max(0, first - self.overscan)
            end = min(self._item_count, first + visible + self.overscan)
            end = min(end, start + self.max_window)

            return (start, end) if end > start else (start, start)

        def __window_for_variable(self, value):
            if self._item_count <= 0 or not self._prefix:
                return 0, 0

            scroll_in_list = max(0, value - self._header_size)
            prefix = self._prefix

            first = max(0, bisect.bisect_right(prefix, scroll_in_list) - 1)
            last = bisect.bisect_left(prefix, scroll_in_list + self._viewport_size)
            last = min(last, first + self.max_window)

            start = max(0, first - self.overscan)
            end = min(self._item_count, last + self.overscan)
            end = min(end, start + self.max_window)

            return (start, end) if end > start else (start, start)

        def _on_scroll(self, value):
            # Redraw already happened (Adjustment.change() redraws every
            # displayable registered with it before invoking `changed`).
            # Only force a full screen rebuild when the newly-needed window
            # would fall outside what's currently built - not on every
            # pixel of scroll, or windowing would buy nothing.
            if self._row_size is not None:
                start, end = self.__window_for_uniform(value)
            else:
                start, end = self.__window_for_variable(value)

            if start < self.built_start or end > self.built_end:
                renpy.restart_interaction()

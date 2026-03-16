from __future__ import annotations
from typing import Union
import flet as ft


class ResponsiveAutoLayout:
    """
    Responsive layout that measures the natural width of each control and groups them
    into rows based on the available screen width, scaling them if necessary.

    Workflow:
      1. Measurement: attempts to capture the real width via Container.on_resize (recent Flet).
         If not available, it reads the .width attribute of the control.
      2. Grouping: passes the widths to `_process_widths`, which decides which
         controls go together in the same row and with what scale.
      3. Rendering: builds one row per group, horizontally and vertically centered.
         If content overflows, automatic scroll appears.

    Public Attributes:
        threshold (int): below this page width, the layout switches to a single column.
                         Modifiable at runtime.

    Minimum usage:
        layout = ResponsiveAutoLayout(content=cards, page=page)
        page.add(layout.control)
    """

    # Fallback width when the control cannot be measured or its width read
    _FALLBACK_WIDTH = 200.0

    def __init__(
        self,
        content: Union[list[ft.Control], ft.Control],
        page: ft.Page,
        spacing: int = None,
        threshold: int = None,
    ):
        try:
            from flet_base.config import flet_config
            if spacing is None:
                spacing = flet_config.default_layout_spacing
            if threshold is None:
                threshold = flet_config.default_layout_threshold
        except ImportError:
            if spacing is None:
                spacing = 10
            if threshold is None:
                threshold = 600

        self._children = content if isinstance(content, list) else [content]
        self._page = page
        self._spacing = spacing
        self.threshold = threshold  # public: accessible and modifiable from outside

        # Real widths measured in phase 1; None while not yet captured
        self._widths: list[float | None] = [None] * len(self._children)

        # Internal column: tight=True so it only occupies what's necessary.
        self._inner = ft.Column(
            spacing=spacing,
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self._root = ft.Container(
            content=self._inner,
            alignment=ft.Alignment.CENTER,
        )

        # Enable scroll on the page directly: it's the only reliable mechanism
        # in Flet for mouse wheel scrolling.
        page.scroll = ft.ScrollMode.AUTO

        self._start_measurement()
        page.on_resize = self._on_resize

    # ── Public API ──────────────────────────────────────────────────────────

    @property
    def control(self) -> ft.Container:
        """Root control to be added to the page."""
        return self._root

    # ── Phase 1: Real width measurement ────────────────────────────────────

    def _read_width_from_control(self, child: ft.Control) -> float | None:
        """
        Reads the declared width of a control without needing to render it.
        Looks in the control itself and, if it's a Container, in its content.
        Returns None if no valid value is found.
        """
        for node in (child, getattr(child, "content", None)):
            if node is None:
                continue
            w = getattr(node, "width", None)
            if isinstance(w, (int, float)) and w > 0:
                return float(w)
        return None

    def _start_measurement(self) -> None:
        """
        Attempts to measure the real width of each control via Container.on_resize,
        available in recent versions of Flet.

        If on_resize is not supported (TypeError), it falls back to reading the
        .width attribute of the control directly. If it doesn't have it either, it uses _FALLBACK_WIDTH.

        In the case of real measurement, controls are rendered invisible
        (opacity=0) and the layout is built when all are measured.
        In the fallback case, the layout is built immediately.
        """
        print("\n── Measuring Controls ───────────────────────────────")
        wrappers = []
        fallback_needed = False

        for i, child in enumerate(self._children):
            expected = self._read_width_from_control(child)

            def on_measured(e: ft.ControlEvent, idx: int = i, exp=expected) -> None:
                # Only register the first valid measurement of each control
                if e.width and e.width > 0 and self._widths[idx] is None:
                    self._widths[idx] = e.width
                    # Debug: real width vs expected (width declared in the control)
                    real = int(e.width)
                    if exp is not None:
                        deviation = real - int(exp)
                        status = "OK" if abs(deviation) <= 1 else f"DEVIATION: {deviation:+d}px"
                        print(f"  [control #{idx}] real: {real}px  expected: {int(exp)}px  → {status}")
                    else:
                        print(f"  [control #{idx}] real: {real}px  expected: N/A (no declared .width)")
                    # When all controls are measured, build the layout
                    if all(w is not None for w in self._widths):
                        self._build_layout()
                        self._page.update()

            try:
                # The measurement Container goes inside a ft.Row(tight=True)
                # so it doesn't stretch to the parent Column width, but instead
                # adopts the natural size of the child control. Without this Row,
                # e.width would return the full available width, not the card's,
                # making all measurements incorrect.
                wrapper = ft.Row(
                    controls=[
                        ft.Container(
                            content=child,
                            on_resize=on_measured,
                            opacity=0.0,
                        )
                    ],
                    tight=True,  # the Row only occupies what its child needs
                )
                wrappers.append(wrapper)
            except TypeError:
                # on_resize not available in this Flet version:
                # read declared .width from the control directly
                fallback_needed = True
                w = self._read_width_from_control(child)
                measured = w if w is not None else self._FALLBACK_WIDTH
                self._widths[i] = measured
                # Debug: real width vs expected (in this mode "real" = declared)
                if w is not None:
                    print(f"  [control #{i}] real: {int(measured)}px  expected: {int(measured)}px  → OK (read from .width)")
                else:
                    print(f"  [control #{i}] real: N/A  expected: N/A  → FALLBACK {self._FALLBACK_WIDTH}px (no declared .width)")
                wrappers.append(child)

        self._inner.controls = wrappers

        # If all widths are already available (fallback mode), build now
        if fallback_needed and all(w is not None for w in self._widths):
            self._build_layout()

    # ── Phase 2: Layout construction ──────────────────────────────────────

    def _compute_available_width(self) -> float:
        """
        Available width = page width minus horizontal padding.
        Supports both numeric padding and ft.Padding object.
        """
        p = self._page
        pad = p.padding
        if pad is None:
            pl = pr = 0.0
        elif isinstance(pad, ft.Padding):
            pl = pad.left or 0.0
            pr = pad.right or 0.0
        else:
            pl = pr = float(pad)
        return (p.width or 0) - pl - pr

    def _build_layout(self) -> None:
        """
        Builds the full layout based on measured widths.
        Delegates grouping and scaling logic to _process_widths,
        then converts each group into a centered row.

        Each row occupies the full available width (expand=True) so that
        centering is consistent regardless of content size.

        If page width is below threshold, it forces a single column by
        passing each control individually without grouping.
        """
        available = self._compute_available_width()
        width = self._page.width or 0

        if width < self.threshold:
            # Single column mode: each control occupies its own row without scaling
            result = {i: 1.0 for i in range(len(self._children))}
        else:
            elements = {i: int(self._widths[i]) for i in range(len(self._children))}
            result = self._process_widths(elements, int(available), self._spacing)

        print(
            f"ResponsiveAutoLayout → width={int(width)}px "
            f"available={int(available)}px rows={len(result)}"
        )
        print(f"  widths: {[int(w) for w in self._widths]}")
        print(f"  groups: {list(result.keys())}")

        rows = []
        for key, scale in result.items():
            keys = key if isinstance(key, tuple) else (key,)
            widget = self._make_scaled_widget(keys, scale)
            rows.append(
                ft.Row(
                    controls=[widget],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        self._inner.controls = rows

    def _make_scaled_widget(self, keys: tuple, scale: float) -> ft.Control:
        """
        Builds the visual widget for a group of controls.

        - If scale == 1.0: returns the controls directly (no transformation).
        - If scale < 1.0: the group exceeds available width and needs reduction.
          ft.Scale and ft.Stack do not modify space in Flet's layout, so the only
          reliable solution is to modify width/height directly in each control
          of the group proportionally to the calculated scale.

        When there are multiple controls in a group, they are wrapped in a centered Row.
        """
        children = [self._children[k] for k in keys]

        if scale == 1.0:
            inner: ft.Control = (
                ft.Row(
                    controls=children,
                    spacing=self._spacing,
                    alignment=ft.MainAxisAlignment.CENTER,
                )
                if len(children) > 1
                else children[0]
            )
            return inner

        # Directly scale width and height of each control in the group.
        # It's the only mechanism Flet respects in the layout.
        # A copy of the attributes is modified, not the original control,
        # wrapping it in a Container with scaled dimensions.
        scaled_children = []
        for child in children:
            w = getattr(child, "width", None)
            h = getattr(child, "height", None)
            scaled_children.append(
                ft.Container(
                    content=child,
                    width=w * scale if isinstance(w, (int, float)) else None,
                    height=h * scale if isinstance(h, (int, float)) else None,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                )
            )

        return (
            ft.Row(
                controls=scaled_children,
                spacing=self._spacing * scale,
                alignment=ft.MainAxisAlignment.CENTER,
            )
            if len(scaled_children) > 1
            else scaled_children[0]
        )

    # ── Resize ───────────────────────────────────────────────────────────────

    def _on_resize(self, e: ft.ControlEvent) -> None:
        """Recalculates setup on every window resize."""
        if all(w is not None for w in self._widths):
            self._build_layout()
            self._page.update()

    # ── Grouping and scaling algorithm ─────────────────────────────────────

    @staticmethod
    def _process_widths(
        elements: dict,
        screen_width: int,
        spacing: int = 0,
    ) -> dict:
        """
        Processes a dictionary of elements with their widths and returns a new
        dictionary with the necessary scales to fit them onto the screen.

        Parameters:
        - elements:      dict {key: width} where key can be any hashable type
                         and width is a positive int.
        - screen_width:  int, reference screen width.
        - spacing:       int, fixed space between grouped elements (default 0).

        Returns:
        - dict {key_or_group: scale} where:
            · key_or_group is the original key if the element is alone,
              or a tuple of keys if multiple were grouped.
            · scale is a float indicating the applied scale factor.

        Logic (greedy until available width):
        - For each element, attempts to add the next as long as the resulting group
          does not exceed the full available width.
        - If an individual element is wider than available, it is scaled down
          exactly to fit.
        - If it fits without exceeding the limit: scale 1.0 (no change).
        - Maximizes the number of elements per row without scaling.
        """
        # Filter elements with width 0 (invalid)
        valid_elements = []
        for key, width in elements.items():
            if width == 0:
                print(f"Error: element '{key}' has width 0 and will be ignored.")
            else:
                valid_elements.append((key, width))

        if not valid_elements:
            return {}

        result = {}
        i = 0
        n = len(valid_elements)
        # Use full available width as grouping limit.
        # A 90% margin was fragile: 2px difference could prevent a group
        # of 3 cards from fitting when they visually could.
        limit = screen_width

        while i < n:
            current_key, current_width = valid_elements[i]
            group = [current_key]
            group_width = current_width

            # Keep adding elements as long as the group fits in the available width
            while i + 1 < n:
                next_key, next_width = valid_elements[i + 1]
                if group_width + next_width + spacing <= limit:
                    i += 1
                    group_width += next_width + spacing
                    group.append(next_key)
                else:
                    break

            # If an individual element exceeds available width, scale it
            scale = limit / group_width if group_width > limit else 1.0

            # Simple key if the group has one element, tuple if multiple
            if len(group) == 1:
                result[group[0]] = scale
            else:
                result[tuple(group)] = scale

            i += 1  # advance to next group

        return result
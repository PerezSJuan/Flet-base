from __future__ import annotations
from typing import Union
import flet as ft


class ResponsiveAutoLayout:
    """
    Layout responsivo que mide el ancho natural de cada control y los agrupa
    en filas según el ancho disponible de pantalla, escalándolos si es necesario.

    Flujo:
      1. Medición: intenta capturar el ancho real via Container.on_resize (Flet
         reciente). Si no está disponible, lee el atributo .width del control.
      2. Agrupación: pasa los anchos a `_procesar_anchuras`, que decide qué
         controles van juntos en la misma fila y con qué escala.
      3. Renderizado: construye una fila por cada grupo, centrada horizontal y
         verticalmente. Si el contenido desborda, aparece scroll automático.

    Atributos públicos:
        threshold (int): por debajo de este ancho de página el layout pasa a
                         columna única. Modificable en tiempo de ejecución.

    Uso mínimo:
        layout = ResponsiveAutoLayout(content=cards, page=page)
        page.add(layout.control)
    """

    # Ancho de fallback cuando no se puede medir ni leer el control
    _FALLBACK_WIDTH = 200.0

    def __init__(
        self,
        content: Union[list[ft.Control], ft.Control],
        page: ft.Page,
        separacion: int = 10,
        threshold: int = 600,
    ):
        self._children = content if isinstance(content, list) else [content]
        self._page = page
        self._separacion = separacion
        self.threshold = threshold  # público: accesible y modificable desde fuera

        # Anchos reales medidos en fase 1; None mientras no se hayan capturado
        self._widths: list[float | None] = [None] * len(self._children)

        # Columna interna: tight=True para que ocupe solo lo necesario.
        self._inner = ft.Column(
            spacing=separacion,
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self._root = ft.Container(
            content=self._inner,
            alignment=ft.Alignment.CENTER,
        )

        # Activar scroll en la página directamente: es el único mecanismo
        # fiable en Flet para scroll con rueda de ratón.
        page.scroll = ft.ScrollMode.AUTO

        self._start_measurement()
        page.on_resize = self._on_resize

    # ── API pública ──────────────────────────────────────────────────────────

    @property
    def control(self) -> ft.Container:
        """Control raíz que se añade a la página."""
        return self._root

    # ── Fase 1: medición de anchos reales ────────────────────────────────────

    def _read_width_from_control(self, child: ft.Control) -> float | None:
        """
        Lee el ancho declarado de un control sin necesidad de renderizarlo.
        Busca en el control mismo y, si es un Container, en su contenido.
        Devuelve None si no encuentra ningún valor válido.
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
        Intenta medir el ancho real de cada control via Container.on_resize,
        disponible en versiones recientes de Flet.

        Si on_resize no está soportado (TypeError), cae a leer el atributo
        .width del control directamente. Si tampoco lo tiene, usa _FALLBACK_WIDTH.

        En el caso de medición real, los controles se renderizan invisibles
        (opacity=0) y el layout se construye cuando todos están medidos.
        En el caso de fallback, el layout se construye de inmediato.
        """
        print("\n── Medición de controles ───────────────────────────────")
        wrappers = []
        fallback_needed = False

        for i, child in enumerate(self._children):
            expected = self._read_width_from_control(child)

            def on_measured(e: ft.ControlEvent, idx: int = i, exp=expected) -> None:
                # Solo registrar la primera medición válida de cada control
                if e.width and e.width > 0 and self._widths[idx] is None:
                    self._widths[idx] = e.width
                    # Debug: real width vs expected (width declarado en el control)
                    real = int(e.width)
                    if exp is not None:
                        desv = real - int(exp)
                        status = "OK" if abs(desv) <= 1 else f"DESVIACIÓN: {desv:+d}px"
                        print(f"  [control #{idx}] real: {real}px  expected: {int(exp)}px  → {status}")
                    else:
                        print(f"  [control #{idx}] real: {real}px  expected: N/A (sin .width declarado)")
                    # Cuando todos los controles están medidos, construir el layout
                    if all(w is not None for w in self._widths):
                        self._build_layout()
                        self._page.update()

            try:
                # El Container de medición va dentro de un ft.Row(tight=True)
                # para que no se estire al ancho de la Column padre, sino que
                # adopte el tamaño natural del control hijo. Sin este Row,
                # e.width devolvería el ancho disponible completo, no el de
                # la card, haciendo que todas las mediciones sean incorrectas.
                wrapper = ft.Row(
                    controls=[
                        ft.Container(
                            content=child,
                            on_resize=on_measured,
                            opacity=0.0,
                        )
                    ],
                    tight=True,  # la Row solo ocupa lo que necesita su hijo
                )
                wrappers.append(wrapper)
            except TypeError:
                # on_resize no disponible en esta versión de Flet:
                # leer .width declarado del control directamente
                fallback_needed = True
                w = self._read_width_from_control(child)
                measured = w if w is not None else self._FALLBACK_WIDTH
                self._widths[i] = measured
                # Debug: real width vs expected (en este modo "real" = declarado)
                if w is not None:
                    print(f"  [control #{i}] real: {int(measured)}px  expected: {int(measured)}px  → OK (leído de .width)")
                else:
                    print(f"  [control #{i}] real: N/A  expected: N/A  → FALLBACK {self._FALLBACK_WIDTH}px (sin .width declarado)")
                wrappers.append(child)

        self._inner.controls = wrappers

        # Si todos los anchos ya están disponibles (modo fallback), construir ya
        if fallback_needed and all(w is not None for w in self._widths):
            self._build_layout()

    # ── Fase 2: construcción del layout ──────────────────────────────────────

    def _compute_available_width(self) -> float:
        """
        Ancho disponible = ancho de página menos padding horizontal.
        Soporta tanto padding numérico como objeto ft.Padding.
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
        Construye el layout completo a partir de los anchos medidos.
        Delega la lógica de agrupación y escala a _procesar_anchuras,
        luego convierte cada grupo en una fila centrada.

        Cada fila ocupa el ancho completo disponible (expand=True) para que
        el centrado sea consistente independientemente del tamaño del contenido.

        Si el ancho de página está por debajo de threshold, fuerza una
        sola columna pasando cada control individualmente sin agrupar.
        """
        available = self._compute_available_width()
        width = self._page.width or 0

        if width < self.threshold:
            # Modo columna única: cada control ocupa su propia fila sin escala
            result = {i: 1.0 for i in range(len(self._children))}
        else:
            elementos = {i: int(self._widths[i]) for i in range(len(self._children))}
            result = self._procesar_anchuras(elementos, int(available), self._separacion)

        print(
            f"ResponsiveAutoLayout → width={int(width)}px "
            f"available={int(available)}px filas={len(result)}"
        )
        print(f"  widths: {[int(w) for w in self._widths]}")
        print(f"  grupos: {list(result.keys())}")

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
        Construye el widget visual para un grupo de controles.

        - Si scale == 1.0: devuelve los controles directamente (sin transformación).
        - Si scale < 1.0: el grupo supera el ancho disponible y hay que reducirlo.
          ft.Scale y ft.Stack no modifican el espacio en el layout de Flet, así
          que la única solución fiable es modificar width/height directamente en
          cada control del grupo proporcialmente a la escala calculada.

        Cuando hay varios controles en el grupo, se envuelven en una Row centrada.
        """
        children = [self._children[k] for k in keys]

        if scale == 1.0:
            inner: ft.Control = (
                ft.Row(
                    controls=children,
                    spacing=self._separacion,
                    alignment=ft.MainAxisAlignment.CENTER,
                )
                if len(children) > 1
                else children[0]
            )
            return inner

        # Escalar directamente width y height de cada control del grupo.
        # Es el único mecanismo que Flet respeta en el layout.
        # Se modifica una copia de los atributos, no el control original,
        # envolviéndolo en un Container con las dimensiones escaladas.
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
                spacing=self._separacion * scale,
                alignment=ft.MainAxisAlignment.CENTER,
            )
            if len(scaled_children) > 1
            else scaled_children[0]
        )

    # ── Resize ───────────────────────────────────────────────────────────────

    def _on_resize(self, e: ft.ControlEvent) -> None:
        """Recalcula el layout en cada cambio de tamaño de ventana."""
        if all(w is not None for w in self._widths):
            self._build_layout()
            self._page.update()

    # ── Algoritmo de agrupación y escala ─────────────────────────────────────

    @staticmethod
    def _procesar_anchuras(
        elementos: dict,
        ancho_pantalla: int,
        separacion: int = 0,
    ) -> dict:
        """
        Procesa un diccionario de elementos con sus anchos y devuelve un nuevo
        diccionario con las escalas necesarias para ajustarlos a la pantalla.

        Parámetros:
        - elementos:      dict {clave: ancho} donde clave puede ser cualquier tipo
                          hashable y ancho es un int positivo.
        - ancho_pantalla: int, ancho de la pantalla de referencia.
        - separacion:     int, espacio fijo entre elementos agrupados (por defecto 0).

        Retorna:
        - dict {clave_o_grupo: escala} donde:
            · clave_o_grupo es la clave original si el elemento va solo,
              o una tupla con las claves si se agruparon varios.
            · escala es un float que indica el factor de escala aplicado.

        Lógica (greedy hasta ancho disponible):
        - Por cada elemento, se intenta añadir el siguiente mientras el grupo
          resultante no supere el ancho disponible completo.
        - Si un elemento individual es más ancho que el disponible, se escala
          hacia abajo exactamente hasta caber.
        - Si cabe sin superar el límite: escala 1.0 (sin cambios).
        - Se maximiza el número de elementos por fila sin escalar.
        """
        # Filtrar elementos con ancho 0 (inválidos)
        elementos_validos = []
        for clave, ancho in elementos.items():
            if ancho == 0:
                print(f"Error: el elemento '{clave}' tiene ancho 0 y será ignorado.")
            else:
                elementos_validos.append((clave, ancho))

        if not elementos_validos:
            return {}

        resultado = {}
        i = 0
        n = len(elementos_validos)
        # Usar el ancho disponible completo como límite de agrupación.
        # Un margen del 90% era frágil: 2px de diferencia podían impedir
        # que un grupo de 3 cards cupiera cuando sí cabía visualmente.
        limite = ancho_pantalla

        while i < n:
            clave_actual, ancho_actual = elementos_validos[i]
            grupo = [clave_actual]
            ancho_grupo = ancho_actual

            # Seguir añadiendo elementos mientras el grupo quepa en el ancho disponible
            while i + 1 < n:
                sig_clave, sig_ancho = elementos_validos[i + 1]
                if ancho_grupo + sig_ancho + separacion <= limite:
                    i += 1
                    ancho_grupo += sig_ancho + separacion
                    grupo.append(sig_clave)
                else:
                    break

            # Si un elemento individual supera el ancho disponible, escalarlo
            escala = limite / ancho_grupo if ancho_grupo > limite else 1.0

            # Clave simple si el grupo tiene un solo elemento, tupla si son varios
            if len(grupo) == 1:
                resultado[grupo[0]] = escala
            else:
                resultado[tuple(grupo)] = escala

            i += 1  # avanzar al siguiente grupo

        return resultado
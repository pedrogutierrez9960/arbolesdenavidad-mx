#!/usr/bin/env python3
"""
Generador de posts para Instagram — arbolesdenavidad.mx
========================================================
Renderiza los 6 primeros posts de contenido/primeros-posts.md a 4:5 (1080x1350).

Dos plantillas, según la calidad real de la foto:
  A. FOTO COMPLETA  - para las 4 fotos de 960x1280 que aguantan sangre completa
                      (arbol-25, 19, 18, 05).
  B. TARJETA/VELO   - para fotos de menor resolución u orientación equivocada.
                      La foto va inserta o bajo velo de marca, con tipografía
                      encima. Se ve intencional en vez de exhibir el techo de
                      resolución.
  C. VECTOR PURO    - gráficos generados (comparativa de tamaños).

Uso:
    python3 herramientas/generar-posts.py            # todos
    python3 herramientas/generar-posts.py post-001   # uno solo
"""
import sys

from marca import (CREMA, CUERPO, DISPLAY, DORADO, F_CUERPO, F_CUERPO_B,
                   F_DISPLAY, F_DISPLAY_B, H, SALVIA, VERDE, VERDE_M, W,
                   ancho_texto, bloque_texto, envoltura, envolver, esc, exportar, firma,
                   foto_b64, isotipo, marco, rombo)

# ═══════════════════════════════════════════════════════════ velos reutilizables


def velo(id_, paradas):
    """Gradiente vertical de velo verde. paradas = [(offset%, opacidad), ...]"""
    stops = "".join(
        f'<stop offset="{o}%" stop-color="{VERDE}" stop-opacity="{a}"/>'
        for o, a in paradas
    )
    return (f'<linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1">{stops}'
            f'</linearGradient>')


# Velo suave: deja respirar la foto, oscurece solo los extremos donde va texto.
VELO_SUAVE = [(0, 0.72), (16, 0.34), (40, 0.06), (58, 0.16), (78, 0.78), (100, 0.97)]
# Velo fuerte: la foto pasa a ser textura de fondo, el texto manda.
VELO_FUERTE = [(0, 0.93), (35, 0.86), (52, 0.62), (70, 0.88), (100, 0.98)]


def regla(y, ancho=280, color=DORADO, opacidad=0.9):
    return (f'<line x1="{(W-ancho)//2}" y1="{y}" x2="{(W+ancho)//2}" y2="{y}" '
            f'stroke="{color}" stroke-width="2" opacity="{opacidad}"/>')


# ═══════════════════════════════════════════════════════════ POST 1 — presentación


def post_001():
    """Foto insignia a sangre completa. Mínima intervención: la foto es el mensaje."""
    p = [f'<defs>{velo("v", VELO_SUAVE)}</defs>']
    p.append(f'<image href="{foto_b64("arbol-25.jpg", anclaje_v=0.44)}" x="0" y="0" '
             f'width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#v)"/>')
    p.append(marco())
    p.append(isotipo(464, 68, 0.144))

    p.append(f'<text x="{W//2}" y="1128" font-family="{CUERPO}" font-size="25" '
             f'fill="{DORADO}" text-anchor="middle" letter-spacing="6">'
             f'ABETO NOBLE DE OREGON</text>')
    p.append(regla(1168, 300))
    p.append(f'<text x="{W//2}" y="1236" font-family="{DISPLAY}" font-size="60" '
             f'fill="{CREMA}" text-anchor="middle">Naturales, de 1 a 6 metros</text>')
    p.append(f'<text x="{W//2}" y="1288" font-family="{CUERPO}" font-size="27" '
             f'fill="{SALVIA}" text-anchor="middle">'
             f'Entrega a domicilio · CDMX y Estado de México</text>')
    p.append(firma(1330, tam=23))
    return envoltura("".join(p))


# ═══════════════════════════════════════════════════════════ POST 2 — quiénes somos


def post_002():
    """
    Tarjeta con la progresión 20 -> 100 -> 150.
    arbol-03 es horizontal (1280x720): en vez de pelearme con el recorte a 4:5,
    la uso como banda horizontal, que es su formato nativo. El recorte alto
    (anclaje 0.30) deja fuera la lona azul del piso.
    """
    banda_w, banda_h, banda_y = 940, 300, 452
    p = [f'<rect width="{W}" height="{H}" fill="{VERDE}"/>', marco()]
    p.append(isotipo(464, 62, 0.132))

    p.append(f'<text x="{W//2}" y="272" font-family="{DISPLAY}" font-size="70" '
             f'fill="{CREMA}" text-anchor="middle">Cuarta temporada</text>')
    p.append(f'<text x="{W//2}" y="330" font-family="{CUERPO}" font-size="27" '
             f'fill="{SALVIA}" text-anchor="middle" letter-spacing="2">'
             f'Así hemos crecido</text>')
    p.append(regla(384, 200))

    # banda de foto con marco dorado fino
    p.append(f'<image href="{foto_b64("arbol-03.jpg", banda_w, banda_h, 0.30)}" '
             f'x="{(W-banda_w)//2}" y="{banda_y}" width="{banda_w}" height="{banda_h}" '
             f'preserveAspectRatio="xMidYMid slice"/>')
    p.append(f'<rect x="{(W-banda_w)//2}" y="{banda_y}" width="{banda_w}" '
             f'height="{banda_h}" fill="none" stroke="{DORADO}" stroke-width="2" '
             f'opacity="0.55"/>')

    # progresión de temporadas
    # Cifras en Lato: EB Garamond usa figuras oldstyle y "20 100 150" se leía
    # como "2o ıoo ı5o". Para cifras sueltas siempre va la sans.
    datos = [("20", "Año 1"), ("100", "Año 2"), ("150", "Año 3")]
    cx = [W // 2 - 300, W // 2, W // 2 + 300]
    for (num, etiqueta), x in zip(datos, cx):
        p.append(f'<text x="{x}" y="948" font-family="{CUERPO}" font-size="92" '
                 f'font-weight="bold" fill="{DORADO}" text-anchor="middle">{num}</text>')
        p.append(f'<text x="{x}" y="994" font-family="{CUERPO}" font-size="25" '
                 f'fill="{SALVIA}" text-anchor="middle" letter-spacing="2">'
                 f'{etiqueta}</text>')
    # flechas entre cifras
    for x in (W // 2 - 150, W // 2 + 150):
        p.append(f'<text x="{x}" y="928" font-family="{CUERPO}" font-size="40" '
                 f'fill="{SALVIA}" text-anchor="middle" opacity="0.5">→</text>')

    p.append(f'<text x="{W//2}" y="1074" font-family="{CUERPO}" font-size="25" '
             f'fill="{SALVIA}" text-anchor="middle" letter-spacing="2">'
             f'ÁRBOLES ENTREGADOS POR TEMPORADA</text>')

    p.append(f'<rect x="96" y="1128" width="888" height="98" rx="8" fill="{VERDE_M}" '
             f'stroke="{DORADO}" stroke-width="2" opacity="0.95"/>')
    p.append(f'<text x="{W//2}" y="1178" font-family="{DISPLAY}" font-size="46" '
             f'fill="{CREMA}" text-anchor="middle">Este año vamos por muchos más</text>')
    p.append(f'<text x="{W//2}" y="1212" font-family="{CUERPO}" font-size="22" '
             f'fill="{SALVIA}" text-anchor="middle">'
             f'Importamos directo de Oregon · Entregamos nosotros mismos</text>')
    p.append(firma(1290, tam=23))
    return envoltura("".join(p))


# ═══════════════════════════════════════════════════════════ POST 3 — carrusel


def _slide_foto(archivo, anclaje, sobre, titulo, pie=None, indicador=None):
    p = [f'<defs>{velo("v", VELO_SUAVE)}</defs>']
    p.append(f'<image href="{foto_b64(archivo, anclaje_v=anclaje)}" x="0" y="0" '
             f'width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#v)"/>')
    p.append(marco())
    p.append(isotipo(478, 66, 0.124))
    if sobre:
        p.append(f'<text x="{W//2}" y="1088" font-family="{CUERPO}" font-size="24" '
                 f'fill="{DORADO}" text-anchor="middle" letter-spacing="6">'
                 f'{esc(sobre)}</text>')
    t, _ = bloque_texto(titulo, W // 2, 1170, F_DISPLAY, DISPLAY, 66, CREMA, 900,
                        interlineado=1.16)
    p.append(t)
    if pie:
        p.append(f'<text x="{W//2}" y="1268" font-family="{CUERPO}" font-size="26" '
                 f'fill="{SALVIA}" text-anchor="middle">{esc(pie)}</text>')
    if indicador:
        p.append(f'<text x="{W//2}" y="1322" font-family="{CUERPO}" font-size="23" '
                 f'fill="{DORADO}" text-anchor="middle" letter-spacing="3">'
                 f'{esc(indicador)}</text>')
    else:
        p.append(firma(1322, tam=22))
    return envoltura("".join(p))


def _slide_tarjeta(indice, titulo, cuerpo, fuente=None):
    """
    Tarjeta de argumento. El índice grande da ritmo al carrusel.
    El bloque se centra verticalmente para que no queden huecos muertos.
    """
    T_TIT, T_CUE = 72, 40
    lineas_tit = len(envolver(titulo, F_DISPLAY, T_TIT, 890))
    lineas_cue = len(envolver(cuerpo, F_CUERPO, T_CUE, 880))
    alto_tit = lineas_tit * int(T_TIT * 1.14)
    alto_cue = lineas_cue * int(T_CUE * 1.5)
    # índice (150) + regla (56) + título + aire (72) + cuerpo
    alto_total = 150 + 56 + alto_tit + 72 + alto_cue
    y = (H - alto_total) // 2 + 40

    p = [f'<rect width="{W}" height="{H}" fill="{VERDE}"/>']
    # isotipo como marca de agua, anclado abajo a la derecha para no estorbar
    p.append(isotipo(560, 660, 0.62, opacidad=0.055))
    p.append(marco())

    # Índice en Lato: en EB Garamond "01" se renderizaba como "OI".
    p.append(f'<text x="96" y="{y}" font-family="{CUERPO}" font-size="112" '
             f'font-weight="bold" fill="{DORADO}" opacity="0.92" '
             f'letter-spacing="2">{esc(indice)}</text>')
    y += 56
    p.append(f'<line x1="96" y1="{y}" x2="380" y2="{y}" stroke="{DORADO}" '
             f'stroke-width="3"/>')

    y += 96
    t, _ = bloque_texto(titulo, 96, y, F_DISPLAY, DISPLAY, T_TIT, CREMA, 890,
                        interlineado=1.14, anclaje="start")
    p.append(t)

    y += alto_tit + 46
    c, _ = bloque_texto(cuerpo, 96, y, F_CUERPO, CUERPO, T_CUE, SALVIA,
                        880, interlineado=1.5, anclaje="start")
    p.append(c)

    if fuente:
        p.append(rombo(106, 1186))
        f, _ = bloque_texto(fuente, 138, 1194, F_CUERPO, CUERPO, 21, SALVIA, 830,
                            interlineado=1.4, anclaje="start", opacidad=0.75)
        p.append(f)
    p.append(firma(1302, tam=22))
    return envoltura("".join(p))


def post_003a():
    return _slide_foto("arbol-19.jpg", 0.42, "ABETO NOBLE DE OREGON",
                       "¿Por qué abeto noble y no cualquier árbol?",
                       indicador="DESLIZA →")


def post_003b():
    return _slide_tarjeta(
        "01", "Aguanta la temporada completa",
        "En pruebas del Christmas Tree Research Program, el abeto noble retuvo "
        "más del 90% de su aguja a los 28 días, manteniéndolo hidratado.",
        "Christmas Tree Research Program, Oregon State University. "
        "Condiciones de sala: ~21°C, 30-40% de humedad.")


def post_003c():
    return _slide_tarjeta(
        "02", "La rama es rígida y horizontal",
        "Traducción: aguanta tus esferas pesadas sin doblarse. Es la razón por "
        "la que se ve tan bien decorado.")


def post_003d():
    return _slide_tarjeta(
        "03", "El color azul-plata",
        "Tiene el envés plateado que le da ese tono azul-verdoso que no da "
        "ningún otro árbol.")


def post_003e():
    return _slide_foto("arbol-05.jpg", 0.40, "8 A 10 AÑOS CRECIENDO",
                       "No es un árbol cualquiera",
                       pie="De plantaciones comerciales, no de bosque nativo.")


# ═══════════════════════════════════════════════════════════ POST 4 — tamaños


def _arbol_vector(cx, base_y, altura_px, color=SALVIA, opacidad=1.0):
    """
    Silueta de abeto en 3 niveles escalonados, en el lenguaje visual del isotipo.
    Ancho = 46% de la altura (proporción esbelta, coherente con el noble).
    """
    an = altura_px * 0.46
    tronco_h = altura_px * 0.07
    copa_y = base_y - altura_px
    cuerpo_h = altura_px - tronco_h
    piezas = []
    # tres niveles solapados, de arriba hacia abajo
    for i, (ini, fin, ancho_f) in enumerate([(0.00, 0.42, 0.52),
                                             (0.30, 0.74, 0.78),
                                             (0.60, 1.00, 1.00)]):
        y0 = copa_y + cuerpo_h * ini
        y1 = copa_y + cuerpo_h * fin
        med = an * ancho_f / 2
        piezas.append(
            f'<path d="M {cx},{y0:.1f} L {cx-med:.1f},{y1:.1f} '
            f'L {cx+med:.1f},{y1:.1f} Z" fill="{color}" opacity="{opacidad}"/>')
    piezas.append(
        f'<rect x="{cx - an*0.045:.1f}" y="{base_y - tronco_h:.1f}" '
        f'width="{an*0.09:.1f}" height="{tronco_h:.1f}" fill="{color}" '
        f'opacity="{opacidad*0.8}"/>')
    return "".join(piezas)


def _persona_vector(cx, base_y, altura_px, color=DORADO):
    """Silueta humana de referencia. Sin ella, la comparativa no dice nada."""
    cabeza_r = altura_px * 0.062
    cabeza_cy = base_y - altura_px + cabeza_r
    torso_y = cabeza_cy + cabeza_r * 1.5
    torso_h = altura_px * 0.36
    hombro = altura_px * 0.105
    pierna_h = base_y - (torso_y + torso_h)
    return (
        f'<circle cx="{cx}" cy="{cabeza_cy:.1f}" r="{cabeza_r:.1f}" fill="{color}"/>'
        f'<path d="M {cx-hombro:.1f},{torso_y+torso_h:.1f} '
        f'L {cx-hombro*0.82:.1f},{torso_y:.1f} '
        f'Q {cx},{torso_y-altura_px*0.022:.1f} {cx+hombro*0.82:.1f},{torso_y:.1f} '
        f'L {cx+hombro:.1f},{torso_y+torso_h:.1f} Z" fill="{color}"/>'
        f'<rect x="{cx-hombro*0.72:.1f}" y="{torso_y+torso_h:.1f}" '
        f'width="{hombro*0.58:.1f}" height="{pierna_h:.1f}" fill="{color}"/>'
        f'<rect x="{cx+hombro*0.14:.1f}" y="{torso_y+torso_h:.1f}" '
        f'width="{hombro*0.58:.1f}" height="{pierna_h:.1f}" fill="{color}"/>'
    )


def post_004():
    """
    Comparativa de escala. Resuelve la duda #1 del cliente según INVENTARIO-FOTOS.md.
    Escala honesta: todo se dibuja con el mismo factor px/metro.
    """
    base_y = 1104
    px_m = 134.0          # factor único de escala
    ref_persona = 1.70    # metros

    p = [f'<rect width="{W}" height="{H}" fill="{VERDE}"/>', marco()]
    p.append(isotipo(478, 58, 0.118))

    p.append(f'<text x="{W//2}" y="248" font-family="{DISPLAY}" font-size="66" '
             f'fill="{CREMA}" text-anchor="middle">'
             f'¿De qué tamaño me cabe?</text>')
    p.append(f'<text x="{W//2}" y="300" font-family="{CUERPO}" font-size="26" '
             f'fill="{SALVIA}" text-anchor="middle">'
             f'La pregunta que más nos hacen</text>')
    p.append(regla(340, 220))

    # retícula de referencia: una línea por metro. Llena el aire muerto y deja
    # ver que la comparativa está a escala real, no dibujada "a ojo".
    for m in range(1, 6):
        gy = base_y - m * px_m
        p.append(f'<line x1="70" y1="{gy:.0f}" x2="{W-70}" y2="{gy:.0f}" '
                 f'stroke="{SALVIA}" stroke-width="1" opacity="0.13" '
                 f'stroke-dasharray="7 9"/>')
        p.append(f'<text x="{W-78}" y="{gy-9:.0f}" font-family="{CUERPO}" '
                 f'font-size="19" fill="{SALVIA}" text-anchor="end" '
                 f'opacity="0.42">{m} m</text>')

    # piso
    p.append(f'<line x1="70" y1="{base_y}" x2="{W-70}" y2="{base_y}" '
             f'stroke="{SALVIA}" stroke-width="2" opacity="0.35"/>')

    # persona de referencia + cuatro rangos de altura
    elementos = [
        ("persona", ref_persona, "1.70 m", "referencia"),
        ("arbol", 1.20, "1 a 1.5 m", "Depas y oficinas"),
        ("arbol", 2.00, "1.8 a 2.2 m", "La más pedida"),
        ("arbol", 2.75, "2.5 a 3 m", "Doble altura"),
        ("arbol", 5.00, "4 a 6 m", "Lobbies y plazas"),
    ]
    anchos = [ref_persona * px_m * 0.22 if t == "persona" else h * px_m * 0.46
              for t, h, _, _ in elementos]
    hueco = (W - 140 - sum(anchos)) / (len(elementos) - 1)
    x = 70.0
    for (tipo, metros, etiqueta, uso), an in zip(elementos, anchos):
        cx = x + an / 2
        alto_px = metros * px_m
        if tipo == "persona":
            p.append(_persona_vector(cx, base_y, alto_px))
        else:
            p.append(_arbol_vector(cx, base_y, alto_px))
        p.append(f'<text x="{cx:.0f}" y="{base_y+44}" font-family="{CUERPO}" '
                 f'font-size="25" font-weight="bold" fill="{DORADO}" '
                 f'text-anchor="middle">{esc(etiqueta)}</text>')
        t, _ = bloque_texto(uso, int(cx), base_y + 78, F_CUERPO, CUERPO, 20,
                            SALVIA, max(an + hueco * 0.85, 130), interlineado=1.3)
        p.append(t)
        x += an + hueco

    p.append(f'<rect x="96" y="1216" width="888" height="76" rx="8" '
             f'fill="{VERDE_M}" stroke="{DORADO}" stroke-width="2"/>')
    p.append(f'<text x="{W//2}" y="1264" font-family="{CUERPO}" font-size="27" '
             f'fill="{CREMA}" text-anchor="middle">'
             f'Deja mínimo 30 cm entre la punta y el techo</text>')
    p.append(firma(1328, tam=22))
    return envoltura("".join(p))


# ═══════════════════════════════════════════════════════════ POST 5 — cómo funciona


def post_005():
    """
    arbol-22 es de 720 px de ancho: a sangre completa se vería suave.
    Bajo velo fuerte funciona como textura y el texto carga el mensaje.
    """
    p = [f'<defs>{velo("v", VELO_FUERTE)}</defs>']
    p.append(f'<image href="{foto_b64("arbol-22.jpg", anclaje_v=0.34)}" x="0" y="0" '
             f'width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#v)"/>')
    p.append(marco())
    p.append(isotipo(478, 62, 0.124))

    p.append(f'<text x="{W//2}" y="268" font-family="{DISPLAY}" font-size="60" '
             f'fill="{CREMA}" text-anchor="middle">Tú escoges.</text>')
    p.append(f'<text x="{W//2}" y="336" font-family="{DISPLAY}" font-size="60" '
             f'fill="{CREMA}" text-anchor="middle">'
             f'Nosotros hacemos todo lo demás.</text>')
    p.append(regla(392, 240))

    pasos = [
        ("1", "Apartas", "Por la página o por WhatsApp"),
        ("2", "Nos dices", "Tamaño y día de entrega"),
        ("3", "Te lo llevamos", "Y lo dejamos parado en su lugar"),
    ]
    y = 512
    for num, titulo, detalle in pasos:
        p.append(f'<circle cx="150" cy="{y+18}" r="38" fill="none" '
                 f'stroke="{DORADO}" stroke-width="2.5"/>')
        p.append(f'<text x="150" y="{y+34}" font-family="{CUERPO}" font-size="38" '
                 f'font-weight="bold" fill="{DORADO}" text-anchor="middle">{num}</text>')
        p.append(f'<text x="222" y="{y+6}" font-family="{DISPLAY}" font-size="50" '
                 f'fill="{CREMA}">{esc(titulo)}</text>')
        p.append(f'<text x="222" y="{y+50}" font-family="{CUERPO}" font-size="27" '
                 f'fill="{SALVIA}">{esc(detalle)}</text>')
        y += 148

    p.append(f'<text x="{W//2}" y="1046" font-family="{DISPLAY}" font-size="40" '
             f'fill="{CREMA}" text-anchor="middle" font-style="italic">'
             f'Sin cargarlo en el coche. Sin agujas en la cajuela.</text>')

    p.append(f'<rect x="96" y="1128" width="888" height="92" rx="8" fill="{DORADO}"/>')
    p.append(f'<text x="{W//2}" y="1170" font-family="{CUERPO}" font-size="30" '
             f'font-weight="bold" fill="{VERDE}" text-anchor="middle">'
             f'ENTREGAS EN CDMX Y ESTADO DE MÉXICO</text>')
    p.append(f'<text x="{W//2}" y="1204" font-family="{CUERPO}" font-size="23" '
             f'fill="{VERDE}" text-anchor="middle">'
             f'Si prefieres, ven a escoger el tuyo en persona</text>')
    p.append(firma(1290, tam=23))
    return envoltura("".join(p))


# ═══════════════════════════════════════════════════════════ registro

POSTS = {
    "post-001": ("post-001-presentacion", post_001),
    "post-002": ("post-002-quienes-somos", post_002),
    "post-003a": ("post-003a-abeto-portada", post_003a),
    "post-003b": ("post-003b-retencion", post_003b),
    "post-003c": ("post-003c-rama", post_003c),
    "post-003d": ("post-003d-color", post_003d),
    "post-003e": ("post-003e-cierre", post_003e),
    "post-004": ("post-004-tamanos", post_004),
    "post-005": ("post-005-como-funciona", post_005),
}


def main():
    pedidos = sys.argv[1:] or list(POSTS)
    print("Renderizando posts a 1080x1350 (4:5)\n")
    for clave in pedidos:
        if clave not in POSTS:
            print(f"  ✗ '{clave}' no existe. Opciones: {', '.join(POSTS)}")
            continue
        nombre, fn = POSTS[clave]
        exportar(fn(), nombre)
    print("\nListos en assets/render/")
    print("El post 6 (preventa) se genera con herramientas/generar-flyer.py")


if __name__ == "__main__":
    main()

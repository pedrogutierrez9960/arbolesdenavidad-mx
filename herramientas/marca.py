"""
Módulo de marca de arbolesdenavidad.mx
=======================================
Tokens de diseño y utilidades compartidas por todos los generadores de imagen.

Sigue el patrón que ya existía en assets/flyers/generar-flyer.py:
composición en SVG -> render a PNG con cairosvg, foto embebida en base64.

Regla: ningún generador define colores, fuentes ni medidas por su cuenta.
Todo sale de aquí para que la cuenta se vea como una sola marca.
"""
import base64
import html
import os
from io import BytesIO

import cairosvg
from PIL import Image, ImageFont

# ---------------------------------------------------------------- rutas
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOTOS = os.path.join(RAIZ, "assets", "fotos-historicas")
MARCA = os.path.join(RAIZ, "assets", "marca")
RENDER = os.path.join(RAIZ, "assets", "render")
FLYERS = os.path.join(RAIZ, "assets", "flyers")

# ---------------------------------------------------------------- lienzo
# 4:5 vertical, formato nativo de feed de Instagram (regla de INVENTARIO-FOTOS.md)
W, H = 1080, 1350

# ---------------------------------------------------------------- paleta
# Definida en contenido/instagram-perfil.md. No inventar colores nuevos.
VERDE = "#0E2A1C"    # verde profundo  - fondos
VERDE_M = "#1B4630"  # verde medio     - bordes, capas
SALVIA = "#BACDB4"   # salvia plateada - el árbol, texto secundario
SALVIA_O = "#8FA98A"  # salvia oscura  - solo dentro del isotipo existente
DORADO = "#C9A227"   # dorado          - acentos, botones, precios
CREMA = "#F2EFE6"    # crema           - texto principal sobre oscuro

# ---------------------------------------------------------------- tipografía
# Georgia (del flyer original) no existe en Linux: caía a DejaVu Serif, que se ve
# genérica. EB Garamond + Lato es la pareja real de la marca a partir de aquí.
DISPLAY = "EB Garamond"
DISPLAY_B = "EB Garamond"
CUERPO = "Lato"

F_DISPLAY = "/usr/share/fonts/opentype/ebgaramond/EBGaramond12-Regular.otf"
F_DISPLAY_B = "/usr/share/fonts/opentype/ebgaramond/EBGaramond12-Bold.otf"
F_CUERPO = "/usr/share/fonts/truetype/lato/Lato-Regular.ttf"
F_CUERPO_B = "/usr/share/fonts/truetype/lato/Lato-Bold.ttf"


def esc(t):
    """Escapa texto para insertarlo en SVG."""
    return html.escape(str(t), quote=False)


# ---------------------------------------------------------------- fotos
def foto_b64(nombre, ancho=W, alto=H, anclaje_v=0.5, calidad=92):
    """
    Recorta una foto al lienzo pedido conservando proporción (cover) y la
    devuelve como data-uri base64 lista para incrustar en el SVG.

    anclaje_v controla qué parte se conserva en el recorte vertical:
      0.0 = pega arriba (conserva la punta del árbol)
      0.5 = centrado
      1.0 = pega abajo
    Para árboles conviene < 0.5: es mejor perder piso que perder la punta.
    """
    ruta = nombre if os.path.isabs(nombre) else os.path.join(FOTOS, nombre)
    im = Image.open(ruta).convert("RGB")
    r = max(ancho / im.width, alto / im.height)
    im = im.resize((max(ancho, int(im.width * r)), max(alto, int(im.height * r))),
                   Image.LANCZOS)
    izq = (im.width - ancho) // 2
    arriba = int((im.height - alto) * anclaje_v)
    im = im.crop((izq, arriba, izq + ancho, arriba + alto))
    buf = BytesIO()
    im.save(buf, "JPEG", quality=calidad)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def resolucion(nombre):
    """Devuelve (ancho, alto) de una foto del acervo."""
    ruta = nombre if os.path.isabs(nombre) else os.path.join(FOTOS, nombre)
    with Image.open(ruta) as im:
        return im.width, im.height


# ---------------------------------------------------------------- texto
_cache_fuentes = {}


def _fuente(ruta, tam):
    clave = (ruta, tam)
    if clave not in _cache_fuentes:
        _cache_fuentes[clave] = ImageFont.truetype(ruta, tam)
    return _cache_fuentes[clave]


def ancho_texto(texto, ruta_fuente, tam):
    """Mide el ancho real de una cadena en píxeles."""
    f = _fuente(ruta_fuente, tam)
    return f.getbbox(texto)[2] - f.getbbox(texto)[0]


def envolver(texto, ruta_fuente, tam, ancho_max):
    """Parte el texto en líneas que quepan en ancho_max. SVG no envuelve solo."""
    lineas, actual = [], ""
    for palabra in texto.split():
        prueba = f"{actual} {palabra}".strip()
        if ancho_texto(prueba, ruta_fuente, tam) <= ancho_max or not actual:
            actual = prueba
        else:
            lineas.append(actual)
            actual = palabra
    if actual:
        lineas.append(actual)
    return lineas


def bloque_texto(texto, x, y, ruta_fuente, familia, tam, color, ancho_max,
                 interlineado=1.35, anclaje="middle", peso="normal",
                 espaciado=0, opacidad=1.0):
    """Genera un <text> con saltos de línea automáticos."""
    lineas = envolver(texto, ruta_fuente, tam, ancho_max)
    salto = int(tam * interlineado)
    tspans = "".join(
        f'<tspan x="{x}" dy="{0 if i == 0 else salto}">{esc(l)}</tspan>'
        for i, l in enumerate(lineas)
    )
    return (
        f'<text x="{x}" y="{y}" font-family="{familia}" font-size="{tam}" '
        f'font-weight="{peso}" fill="{color}" text-anchor="{anclaje}" '
        f'letter-spacing="{espaciado}" opacity="{opacidad}">{tspans}</text>'
    ), len(lineas) * salto


# ---------------------------------------------------------------- marca
def isotipo(x, y, escala, opacidad=1.0):
    """Coloca el isotipo existente (5 ramas + estrella) escalado."""
    with open(os.path.join(MARCA, "isotipo-transparente.svg")) as fh:
        svg = fh.read()
    interior = svg.split(">", 1)[1].rsplit("</svg>", 1)[0]
    return (f'<g transform="translate({x},{y}) scale({escala})" '
            f'opacity="{opacidad}">{interior}</g>')


def firma(y=None, color=DORADO, tam=26):
    """Handle de Instagram al pie. Firma consistente en todas las piezas."""
    y = y if y is not None else H - 46
    return (f'<text x="{W//2}" y="{y}" font-family="{CUERPO}" font-size="{tam}" '
            f'fill="{color}" text-anchor="middle" letter-spacing="1.5" '
            f'opacity="0.95">@arbolesdenavidad.mx</text>')


def marco(margen=34, color=DORADO, opacidad=0.45, grosor=2):
    """Marco dorado interior, heredado del diseño del flyer original."""
    return (f'<rect x="{margen}" y="{margen}" width="{W-margen*2}" '
            f'height="{H-margen*2}" fill="none" stroke="{color}" '
            f'stroke-width="{grosor}" opacity="{opacidad}"/>')


def rombo(cx, cy, lado=13, color=DORADO):
    """Viñeta en forma de rombo, heredada del flyer."""
    return (f'<rect x="{cx-lado/2}" y="{cy-lado/2}" width="{lado}" height="{lado}" '
            f'fill="{color}" transform="rotate(45 {cx} {cy})"/>')


# ---------------------------------------------------------------- salida
def envoltura(cuerpo, ancho=W, alto=H):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {ancho} {alto}" width="{ancho}" height="{alto}">'
            f'{cuerpo}</svg>')


def exportar(svg, nombre, carpeta=None, ancho=W, alto=H):
    """Escribe el .png (y el .svg fuente para poder editarlo a mano después)."""
    carpeta = carpeta or RENDER
    os.makedirs(carpeta, exist_ok=True)
    base = os.path.join(carpeta, nombre)
    with open(base + ".svg", "w") as fh:
        fh.write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=base + ".png",
                     output_width=ancho, output_height=alto)
    kb = os.path.getsize(base + ".png") // 1024
    print(f"  ✓ {nombre}.png  ({ancho}x{alto}, {kb} KB)")
    return base + ".png"

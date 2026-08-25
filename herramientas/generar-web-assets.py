#!/usr/bin/env python3
"""
Assets web optimizados — arbolesdenavidad.mx
=============================================
El sitio debe cargar en menos de 2 segundos en 4G porque casi todo el tráfico
llega desde Instagram en celular. Las fotos del acervo pesan 200-340 KB en JPEG
sin optimizar; aquí salen en WebP a la medida real en que se muestran.

También genera la imagen de Open Graph (1200x630) con la foto insignia y la
marca, para que el link se vea bien cuando alguien lo comparte por WhatsApp.

Uso:
    python3 herramientas/generar-web-assets.py
"""
import os

from PIL import Image

from marca import (CREMA, CUERPO, DISPLAY, DORADO, FOTOS, RAIZ, SALVIA, VERDE,
                   esc, foto_b64, isotipo)
import cairosvg

PUBLICO = os.path.join(RAIZ, "sitio", "public")
DEST_FOTOS = os.path.join(PUBLICO, "fotos")

# foto -> (ancho, alto, anclaje vertical). Medidas reales de uso en el sitio.
PLAN = {
    "arbol-25.jpg": [("hero", 1200, 1500, 0.44), ("hero-movil", 720, 900, 0.44)],
    "arbol-19.jpg": [("interior", 900, 1125, 0.42)],
    "arbol-05.jpg": [("decorado", 900, 1125, 0.40)],
    "arbol-22.jpg": [("entrega", 800, 1000, 0.34)],
    "arbol-03.jpg": [("lote", 1200, 500, 0.30)],
    "arbol-18.jpg": [("sala", 900, 1125, 0.42)],
}


def recortar(nombre, ancho, alto, anclaje):
    im = Image.open(os.path.join(FOTOS, nombre)).convert("RGB")
    r = max(ancho / im.width, alto / im.height)
    im = im.resize((max(ancho, int(im.width * r)), max(alto, int(im.height * r))),
                   Image.LANCZOS)
    izq = (im.width - ancho) // 2
    arr = int((im.height - alto) * anclaje)
    return im.crop((izq, arr, izq + ancho, arr + alto))


def fotos_web():
    os.makedirs(DEST_FOTOS, exist_ok=True)
    total = 0
    for archivo, variantes in PLAN.items():
        for nombre, w, h, anc in variantes:
            im = recortar(archivo, w, h, anc)
            ruta = os.path.join(DEST_FOTOS, f"{nombre}.webp")
            im.save(ruta, "WEBP", quality=80, method=6)
            kb = os.path.getsize(ruta) // 1024
            total += kb
            print(f"  ✓ fotos/{nombre}.webp  ({w}x{h}, {kb} KB)")
    print(f"    total: {total} KB")


def open_graph():
    """1200x630. Es lo que se ve al pegar el link en WhatsApp."""
    W, H = 1200, 630
    p = ['<defs><linearGradient id="v" x1="0" y1="0" x2="1" y2="0">'
         f'<stop offset="0%" stop-color="{VERDE}" stop-opacity="0.97"/>'
         f'<stop offset="52%" stop-color="{VERDE}" stop-opacity="0.86"/>'
         f'<stop offset="100%" stop-color="{VERDE}" stop-opacity="0.30"/>'
         '</linearGradient></defs>']
    p.append(f'<image href="{foto_b64("arbol-25.jpg", W, H, 0.42)}" x="0" y="0" '
             f'width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#v)"/>')
    p.append(isotipo(58, 40, 0.108))
    p.append(f'<text x="74" y="278" font-family="{DISPLAY}" font-size="62" '
             f'font-weight="bold" fill="{CREMA}">Árboles de Navidad</text>')
    p.append(f'<text x="74" y="348" font-family="{DISPLAY}" font-size="62" '
             f'font-weight="bold" fill="{CREMA}">naturales</text>')
    p.append(f'<line x1="74" y1="386" x2="330" y2="386" stroke="{DORADO}" '
             f'stroke-width="3"/>')
    p.append(f'<text x="74" y="436" font-family="{CUERPO}" font-size="27" '
             f'fill="{DORADO}" letter-spacing="4">ABETO NOBLE DE OREGON</text>')
    p.append(f'<text x="74" y="486" font-family="{CUERPO}" font-size="25" '
             f'fill="{SALVIA}">De 1 a 6 metros · Entrega a domicilio</text>')
    p.append(f'<text x="74" y="524" font-family="{CUERPO}" font-size="25" '
             f'fill="{SALVIA}">CDMX y Estado de México</text>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'width="{W}" height="{H}">{"".join(p)}</svg>')
    os.makedirs(PUBLICO, exist_ok=True)
    tmp = os.path.join(PUBLICO, "_og.png")
    cairosvg.svg2png(bytestring=svg.encode(), write_to=tmp,
                     output_width=W, output_height=H)
    Image.open(tmp).convert("RGB").save(os.path.join(PUBLICO, "og.jpg"),
                                        "JPEG", quality=86, optimize=True)
    os.remove(tmp)
    kb = os.path.getsize(os.path.join(PUBLICO, "og.jpg")) // 1024
    print(f"  ✓ og.jpg  ({W}x{H}, {kb} KB)")


def marca_web():
    """Isotipo y favicon."""
    dest = os.path.join(PUBLICO, "marca")
    os.makedirs(dest, exist_ok=True)
    for f in ("isotipo-transparente.svg", "logo-con-texto.svg"):
        origen = os.path.join(RAIZ, "assets", "marca", f)
        with open(origen) as a, open(os.path.join(dest, f), "w") as b:
            b.write(a.read())
        print(f"  ✓ marca/{f}")
    # favicon 64x64
    cairosvg.svg2png(url=os.path.join(RAIZ, "assets", "marca",
                                      "isotipo-transparente.svg"),
                     write_to=os.path.join(PUBLICO, "favicon.png"),
                     output_width=64, output_height=64)
    print("  ✓ favicon.png")


if __name__ == "__main__":
    print("Generando assets web\n")
    fotos_web()
    open_graph()
    marca_web()
    print("\nListos en sitio/public/")

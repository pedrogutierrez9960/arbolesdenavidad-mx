#!/usr/bin/env python3
"""
Generador de flyer de preventa — arbolesdenavidad.mx
=====================================================
Versión parametrizada del flyer original (assets/flyers/flyer-preventa.png).
Mismo diseño, pero descuento, fecha y sitio entran como argumentos para poder
regenerarlo en cuanto se definan, sin tocar código.

Mientras no se definan, salen como placeholders VISIBLES ([XX]%, [XX DE MES]),
según la regla dura #1: nada de datos inventados.

Uso:
    # con placeholders (estado actual)
    python3 herramientas/generar-flyer.py

    # ya con los datos reales
    python3 herramientas/generar-flyer.py --descuento 15 --fecha "30 DE SEPTIEMBRE" \\
        --sitio arbolesdenavidad.mx

    # variante para la red de vendedores (sin sitio, solo WhatsApp)
    python3 herramientas/generar-flyer.py --descuento 15 --fecha "30 DE SEPTIEMBRE" \\
        --sitio "WhatsApp 55 1234 5678" --salida flyer-vendedores
"""
import argparse

from marca import (CREMA, CUERPO, DISPLAY, DORADO, F_CUERPO, FLYERS, H, SALVIA,
                   VERDE, W, bloque_texto, envoltura, esc, exportar, foto_b64,
                   isotipo, marco, rombo)

# Los 3 argumentos que caben en el flyer, tomados de la tabla verificable
# de docs/CONTEXTO-NEGOCIO.md. No agregar ninguno que no esté en esa tabla.
ARGUMENTOS = [
    "Retiene más del 90% de su aguja a 28 días",
    "Rama rígida: aguanta adornos pesados",
    "Importación verificada por PROFEPA",
]


def construir(descuento="[XX]", fecha="[XX DE MES]", sitio="[TUSITIO.COM]",
              foto="arbol-25.jpg"):
    p = []
    p.append('<defs><linearGradient id="vel" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0%" stop-color="{VERDE}" stop-opacity="0.95"/>'
             f'<stop offset="37%" stop-color="{VERDE}" stop-opacity="0.90"/>'
             f'<stop offset="50%" stop-color="{VERDE}" stop-opacity="0.26"/>'
             f'<stop offset="62%" stop-color="{VERDE}" stop-opacity="0.82"/>'
             f'<stop offset="100%" stop-color="{VERDE}" stop-opacity="0.99"/>'
             '</linearGradient></defs>')
    p.append(f'<image href="{foto_b64(foto, anclaje_v=0.44)}" x="0" y="0" '
             f'width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#vel)"/>')
    p.append(marco())
    p.append(isotipo(464, 74, 0.144))

    # encabezado
    p.append(f'<text x="{W//2}" y="300" font-family="{DISPLAY}" font-size="72" '
             f'font-weight="bold" fill="{CREMA}" text-anchor="middle">'
             f'ÁRBOLES DE NAVIDAD</text>')
    p.append(f'<text x="{W//2}" y="368" font-family="{DISPLAY}" font-size="72" '
             f'font-weight="bold" fill="{CREMA}" text-anchor="middle">'
             f'NATURALES</text>')
    p.append(f'<line x1="400" y1="404" x2="680" y2="404" stroke="{DORADO}" '
             f'stroke-width="2"/>')
    p.append(f'<text x="{W//2}" y="458" font-family="{CUERPO}" font-size="32" '
             f'fill="{DORADO}" text-anchor="middle" letter-spacing="5">'
             f'ABETO NOBLE DE OREGON</text>')

    # oferta de producto
    p.append(f'<text x="{W//2}" y="884" font-family="{DISPLAY}" font-size="42" '
             f'fill="{CREMA}" text-anchor="middle">'
             f'De 1 a 6 metros · Entrega a domicilio</text>')
    p.append(f'<text x="{W//2}" y="934" font-family="{CUERPO}" font-size="29" '
             f'fill="{SALVIA}" text-anchor="middle">'
             f'CDMX y Estado de México</text>')

    # argumentos verificables
    y = 1006
    for arg in ARGUMENTOS:
        p.append(rombo(132, y - 6))
        p.append(f'<text x="164" y="{y}" font-family="{CUERPO}" font-size="27" '
                 f'fill="{SALVIA}">{esc(arg)}</text>')
        y += 44

    # bloque de preventa
    p.append(f'<rect x="96" y="1136" width="888" height="96" rx="8" fill="{DORADO}"/>')
    p.append(f'<text x="{W//2}" y="1180" font-family="{CUERPO}" font-size="36" '
             f'font-weight="bold" fill="{VERDE}" text-anchor="middle">'
             f'PREVENTA: {esc(descuento)}% DE DESCUENTO</text>')
    p.append(f'<text x="{W//2}" y="1216" font-family="{CUERPO}" font-size="26" '
             f'fill="{VERDE}" text-anchor="middle">'
             f'apartando antes del {esc(fecha)}</text>')

    p.append(f'<text x="{W//2}" y="1276" font-family="{DISPLAY}" font-size="33" '
             f'fill="{CREMA}" text-anchor="middle">'
             f'Aparta el tuyo en {esc(sitio)}</text>')
    p.append(f'<text x="{W//2}" y="1318" font-family="{CUERPO}" font-size="25" '
             f'fill="{DORADO}" text-anchor="middle" letter-spacing="1.5">'
             f'@arbolesdenavidad.mx</text>')
    return envoltura("".join(p))


def main():
    ap = argparse.ArgumentParser(description="Genera el flyer de preventa.")
    ap.add_argument("--descuento", default="[XX]",
                    help="Porcentaje sin el signo. Ej: 15")
    ap.add_argument("--fecha", default="[XX DE MES]",
                    help='Fecha límite. Ej: "30 DE SEPTIEMBRE"')
    ap.add_argument("--sitio", default="[TUSITIO.COM]",
                    help="Sitio o canal para apartar")
    ap.add_argument("--foto", default="arbol-25.jpg", help="Foto de fondo")
    ap.add_argument("--salida", default="flyer-preventa", help="Nombre del archivo")
    a = ap.parse_args()

    svg = construir(a.descuento, a.fecha, a.sitio, a.foto)
    exportar(svg, a.salida, carpeta=FLYERS)

    if "[" in f"{a.descuento}{a.fecha}{a.sitio}":
        print("\n  ⚠  El flyer trae placeholders sin resolver.")
        print("     NO se puede publicar así. Faltan datos anotados en PENDIENTES.md:")
        if "[" in a.descuento:
            print("       · porcentaje de descuento de preventa")
        if "[" in a.fecha:
            print("       · fecha límite de preventa")
        if "[" in a.sitio:
            print("       · dominio del sitio")


if __name__ == "__main__":
    main()

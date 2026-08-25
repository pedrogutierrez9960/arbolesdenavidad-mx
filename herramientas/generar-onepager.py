#!/usr/bin/env python3
"""
One-pager de venta corporativa (B2B) — arbolesdenavidad.mx
===========================================================
Salida en PDF tamaño carta, pensado para imprimirse y para mandarse adjunto
por correo a facilities, administradores de condominio y gerentes de agencia.

A diferencia de los posts (fondo oscuro), este va sobre crema: se imprime sin
gastar tóner y se lee mejor en pantalla de escritorio.

Todo el contenido sale de docs/CONTEXTO-NEGOCIO.md y docs/INVESTIGACION-MERCADO.md.
Los precios van como [PRECIO] hasta que se definan (regla dura #1).

Uso:
    python3 herramientas/generar-onepager.py
    python3 herramientas/generar-onepager.py --whatsapp "55 1234 5678" \\
        --sitio arbolesdenavidad.mx --correo hola@arbolesdenavidad.mx
"""
import argparse
import os

import cairosvg

from marca import (CREMA, CUERPO, DISPLAY, DORADO, F_CUERPO, F_CUERPO_B,
                   F_DISPLAY, RAIZ, SALVIA, VERDE, VERDE_M, bloque_texto, esc,
                   isotipo)

# Carta: 8.5 x 11 pulgadas a 96 dpi
PW, PH = 816, 1056
MG = 54  # margen

TINTA = "#14251C"        # texto principal sobre crema
TINTA_S = "#4A5B50"      # texto secundario


# Columna de precio pegada al margen derecho. Antes iba a media página y se
# encimaba con la descripción del espacio recomendado.
X_PRECIO = PW - MG - 16


def _fila_tamano(y, rango, uso, precio):
    return (
        f'<text x="{MG+16}" y="{y}" font-family="{CUERPO}" font-size="13" '
        f'font-weight="bold" fill="{TINTA}">{esc(rango)}</text>'
        f'<text x="{MG+130}" y="{y}" font-family="{CUERPO}" font-size="12" '
        f'fill="{TINTA_S}">{esc(uso)}</text>'
        f'<text x="{X_PRECIO}" y="{y}" font-family="{CUERPO}" font-size="13" '
        f'font-weight="bold" fill="{DORADO}" text-anchor="end">{esc(precio)}</text>'
    )


def construir(whatsapp="[WHATSAPP]", sitio="[TUSITIO.COM]", correo="[CORREO]"):
    p = [f'<rect width="{PW}" height="{PH}" fill="{CREMA}"/>']

    # ── encabezado ────────────────────────────────────────────────────────
    p.append(f'<rect x="0" y="0" width="{PW}" height="132" fill="{VERDE}"/>')
    p.append(isotipo(38, 16, 0.093))
    p.append(f'<text x="140" y="58" font-family="{DISPLAY}" font-size="30" '
             f'font-weight="bold" fill="{CREMA}">ÁRBOLES DE NAVIDAD NATURALES</text>')
    p.append(f'<text x="142" y="84" font-family="{CUERPO}" font-size="13" '
             f'fill="{DORADO}" letter-spacing="3">ABETO NOBLE DE OREGON · '
             f'IMPORTACIÓN DIRECTA</text>')
    p.append(f'<text x="142" y="108" font-family="{CUERPO}" font-size="12" '
             f'fill="{SALVIA}">Cuarta temporada · CDMX y Estado de México</text>')

    # ── título ────────────────────────────────────────────────────────────
    p.append(f'<text x="{MG}" y="186" font-family="{DISPLAY}" font-size="34" '
             f'fill="{TINTA}">Propuesta para empresas</text>')
    p.append(f'<line x1="{MG}" y1="200" x2="{MG+180}" y2="200" stroke="{DORADO}" '
             f'stroke-width="2.5"/>')

    intro = ("Surtimos e instalamos árboles de Navidad naturales para lobbies, "
             "showrooms, oficinas, hoteles, restaurantes y torres residenciales. "
             "Importamos directo del productor en Oregon, así que controlamos la "
             "calidad de cada árbol y respondemos por él toda la temporada.")
    t, alto = bloque_texto(intro, MG, 228, F_CUERPO, CUERPO, 13, TINTA_S,
                           PW - MG * 2, interlineado=1.55, anclaje="start")
    p.append(t)

    y = 228 + alto + 26

    # ── tabla de tamaños ──────────────────────────────────────────────────
    p.append(f'<text x="{MG}" y="{y}" font-family="{DISPLAY}" font-size="19" '
             f'fill="{TINTA}">Tamaños disponibles</text>')
    y += 12
    p.append(f'<rect x="{MG}" y="{y}" width="{PW-MG*2}" height="150" '
             f'fill="#FFFFFF" stroke="{SALVIA}" stroke-width="1"/>')
    p.append(f'<rect x="{MG}" y="{y}" width="{PW-MG*2}" height="26" '
             f'fill="{VERDE_M}"/>')
    p.append(f'<text x="{MG+16}" y="{y+18}" font-family="{CUERPO}" font-size="11" '
             f'font-weight="bold" fill="{CREMA}" letter-spacing="1.5">ALTURA</text>')
    p.append(f'<text x="{MG+130}" y="{y+18}" font-family="{CUERPO}" font-size="11" '
             f'font-weight="bold" fill="{CREMA}" letter-spacing="1.5">'
             f'ESPACIO RECOMENDADO</text>')
    p.append(f'<text x="{X_PRECIO}" y="{y+18}" font-family="{CUERPO}" '
             f'font-size="11" font-weight="bold" fill="{CREMA}" '
             f'text-anchor="end" letter-spacing="1.5">PRECIO</text>')

    filas = [
        ("1 a 1.5 m", "Oficinas chicas, recepciones, escritorios"),
        ("1.8 a 2.2 m", "Salas de junta, restaurantes, consultorios"),
        ("2.5 a 3 m", "Entradas, salas de doble altura"),
        ("4 a 6 m", "Lobbies, showrooms, plazas, clubes"),
    ]
    fy = y + 48
    for rango, uso in filas:
        p.append(_fila_tamano(fy, rango, uso, "[PRECIO]"))
        fy += 27
    p.append(f'<text x="{MG+16}" y="{y+142}" font-family="{CUERPO}" font-size="10" '
             f'fill="{TINTA_S}" font-style="italic">'
             f'Precio por volumen y para grupos multi-unidad, a cotizar.</text>')
    y += 176

    # ── servicio y argumentos, dos columnas ───────────────────────────────
    col_w = (PW - MG * 2 - 26) / 2
    cx2 = MG + col_w + 26

    p.append(f'<text x="{MG}" y="{y}" font-family="{DISPLAY}" font-size="19" '
             f'fill="{TINTA}">El servicio incluye</text>')
    p.append(f'<text x="{cx2}" y="{y}" font-family="{DISPLAY}" font-size="19" '
             f'fill="{TINTA}">Por qué abeto noble</text>')

    servicio = [
        ("Entrega", "En la fecha que ustedes fijen, dentro de CDMX y Edomex."),
        ("Instalación", "Lo dejamos parado, montado en su base y sin embalaje."),
        ("Retiro", "Pasamos por él al terminar la temporada."),
        ("Un contacto", "Ustedes tratan directo con los dueños, no con un call center."),
    ]
    sy = y + 26
    for titulo, detalle in servicio:
        p.append(f'<rect x="{MG+1}" y="{sy-8}" width="8" height="8" fill="{DORADO}" '
                 f'transform="rotate(45 {MG+5} {sy-4})"/>')
        p.append(f'<text x="{MG+22}" y="{sy}" font-family="{CUERPO}" font-size="12.5" '
                 f'font-weight="bold" fill="{TINTA}">{esc(titulo)}</text>')
        d, dh = bloque_texto(detalle, MG + 22, sy + 17, F_CUERPO, CUERPO, 11,
                             TINTA_S, col_w - 24, interlineado=1.4, anclaje="start")
        p.append(d)
        sy += 20 + dh + 10

    # argumentos: SOLO los de la tabla verificable de CONTEXTO-NEGOCIO.md
    argumentos = [
        ("Retiene más del 90% de su aguja a los 28 días",
         "Christmas Tree Research Program, Oregon State University"),
        ("Rama rígida y horizontal: soporta adornos pesados",
         "Característica estructural documentada del abeto noble"),
        ("Oregon es el mayor productor de Estados Unidos",
         "Oregon Department of Agriculture / USDA"),
        ("De plantaciones comerciales, no de bosque nativo",
         "SEMARNAT"),
    ]
    ay = y + 26
    for afirmacion, fuente in argumentos:
        p.append(f'<rect x="{cx2+1}" y="{ay-8}" width="8" height="8" fill="{DORADO}" '
                 f'transform="rotate(45 {cx2+5} {ay-4})"/>')
        a, ah = bloque_texto(afirmacion, cx2 + 22, ay, F_CUERPO, CUERPO, 12,
                             TINTA, col_w - 24, interlineado=1.35, anclaje="start")
        p.append(a)
        f, fh = bloque_texto(fuente, cx2 + 22, ay + ah + 4, F_CUERPO, CUERPO, 9.5,
                             TINTA_S, col_w - 24, interlineado=1.35,
                             anclaje="start", opacidad=0.85)
        p.append(f)
        ay += ah + fh + 16

    y = max(sy, ay) + 16

    # ── trazabilidad: el argumento de cumplimiento para compras ───────────
    p.append(f'<rect x="{MG}" y="{y}" width="{PW-MG*2}" height="132" '
             f'fill="{VERDE}" rx="4"/>')
    p.append(f'<text x="{MG+20}" y="{y+30}" font-family="{DISPLAY}" font-size="19" '
             f'fill="{CREMA}">Trazabilidad de importación</text>')
    traz = ("Cada embarque entra al país bajo la NOM-013-SEMARNAT-2020 y es "
            "verificado por PROFEPA en la aduana. Podemos entregar a su área de "
            "compras la documentación completa:")
    t2, h2 = bloque_texto(traz, MG + 20, y + 52, F_CUERPO, CUERPO, 11.5, SALVIA,
                          PW - MG * 2 - 40, interlineado=1.45, anclaje="start")
    p.append(t2)
    docs = ["Certificado fitosanitario internacional (NIMF-12) del estado de origen",
            "Registro de Verificación (RV) de PROFEPA"]
    dy = y + 52 + h2 + 14
    for d in docs:
        p.append(f'<rect x="{MG+21}" y="{dy-7}" width="7" height="7" fill="{DORADO}" '
                 f'transform="rotate(45 {MG+24.5} {dy-3.5})"/>')
        p.append(f'<text x="{MG+40}" y="{dy}" font-family="{CUERPO}" '
                 f'font-size="11.5" fill="{CREMA}">{esc(d)}</text>')
        dy += 19
    p.append(f'<text x="{PW-MG-20}" y="{y+120}" font-family="{CUERPO}" '
             f'font-size="9.5" fill="{SALVIA}" text-anchor="end" '
             f'font-style="italic" opacity="0.8">'
             f'Documentos de la temporada, adjuntos a esta propuesta.</text>')
    y += 152

    # ── prueba social + contacto ──────────────────────────────────────────
    p.append(f'<line x1="{MG}" y1="{y}" x2="{PW-MG}" y2="{y}" stroke="{SALVIA}" '
             f'stroke-width="1"/>')
    y += 26
    p.append(f'<text x="{MG}" y="{y}" font-family="{CUERPO}" font-size="12" '
             f'fill="{TINTA_S}">Cuarta temporada · '
             f'<tspan font-weight="bold" fill="{TINTA}">20 → 100 → 150</tspan> '
             f'árboles entregados · el año pasado, 7 agencias automotrices</text>')
    y += 34

    # Siguiente paso: una propuesta comercial siempre cierra con una acción clara.
    p.append(f'<rect x="{MG}" y="{y-24}" width="{PW-MG*2}" height="52" '
             f'fill="none" stroke="{DORADO}" stroke-width="1.5" rx="4"/>')
    p.append(f'<text x="{MG+18}" y="{y-4}" font-family="{CUERPO}" font-size="12" '
             f'font-weight="bold" fill="{TINTA}" letter-spacing="1.5">'
             f'SIGUIENTE PASO</text>')
    p.append(f'<text x="{MG+18}" y="{y+16}" font-family="{CUERPO}" font-size="11.5" '
             f'fill="{TINTA_S}">Dinos cuántos árboles, de qué altura y para qué '
             f'fecha los necesitan, y les mandamos la cotización.</text>')
    y += 62

    p.append(f'<text x="{MG}" y="{y}" font-family="{CUERPO}" font-size="12.5" '
             f'font-weight="bold" fill="{TINTA}">'
             f'WhatsApp {esc(whatsapp)}  ·  {esc(correo)}  ·  {esc(sitio)}  ·  '
             f'@arbolesdenavidad.mx</text>')

    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PW} {PH}" '
            f'width="{PW}" height="{PH}">{"".join(p)}</svg>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--whatsapp", default="[WHATSAPP]")
    ap.add_argument("--sitio", default="[TUSITIO.COM]")
    ap.add_argument("--correo", default="[CORREO]")
    a = ap.parse_args()

    svg = construir(a.whatsapp, a.sitio, a.correo)
    salida = os.path.join(RAIZ, "b2b")
    os.makedirs(salida, exist_ok=True)
    base = os.path.join(salida, "one-pager-empresas")
    with open(base + ".svg", "w") as fh:
        fh.write(svg)
    cairosvg.svg2pdf(bytestring=svg.encode(), write_to=base + ".pdf")
    cairosvg.svg2png(bytestring=svg.encode(), write_to=base + ".png",
                     output_width=PW * 2, output_height=PH * 2)
    print(f"  ✓ b2b/one-pager-empresas.pdf  (carta, {PW}x{PH} pt)")
    print(f"  ✓ b2b/one-pager-empresas.png  (vista previa 2x)")

    faltantes = [n for n, v in [("WhatsApp", a.whatsapp), ("sitio", a.sitio),
                                ("correo", a.correo)] if "[" in v]
    print("\n  ⚠  Placeholders sin resolver: precios por altura" +
          (", " + ", ".join(faltantes) if faltantes else ""))
    print("     Ver PENDIENTES.md. No mandarlo a un cliente así.")


if __name__ == "__main__":
    main()

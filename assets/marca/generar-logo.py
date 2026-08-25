import cairosvg

VERDE_FONDO  = "#0E2A1C"
VERDE_MEDIO  = "#1B4630"
SALVIA       = "#BACDB4"   # estomas plateados del abeto noble
SALVIA_OSC   = "#8FA98A"
DORADO       = "#C9A227"
CREMA        = "#F2EFE6"

def tiers(cx, y_top, y_bot, n, w_max, w_min):
    """Ramas horizontales escalonadas: la firma real del abeto noble."""
    out = []
    span = y_bot - y_top
    for i in range(n):
        t = i / (n - 1)
        w = w_min + (w_max - w_min) * (t ** 1.12)
        yb = y_top + span * t + span * 0.16
        ya = y_top + span * t - span * 0.02
        d = (
            f"M {cx},{ya:.1f} "
            f"C {cx - w*0.28:.1f},{ya + (yb-ya)*0.5:.1f} {cx - w*0.62:.1f},{yb - 14:.1f} {cx - w:.1f},{yb:.1f} "
            f"L {cx - w*0.60:.1f},{yb - 7:.1f} "
            f"L {cx - w*0.30:.1f},{yb + 5:.1f} "
            f"L {cx},{yb - 6:.1f} "
            f"L {cx + w*0.30:.1f},{yb + 5:.1f} "
            f"L {cx + w*0.60:.1f},{yb - 7:.1f} "
            f"L {cx + w:.1f},{yb:.1f} "
            f"C {cx + w*0.62:.1f},{yb - 14:.1f} {cx + w*0.28:.1f},{ya + (yb-ya)*0.5:.1f} {cx},{ya:.1f} Z"
        )
        out.append((d, i))
    return out

def arbol_svg(size=1080, con_texto=False, fondo=True):
    cx = size / 2
    esc = size / 1080
    if con_texto:
        y_top, y_bot = 250*esc, 640*esc
        capas = tiers(cx, y_top, y_bot, 5, 268*esc, 48*esc)
    else:
        y_top, y_bot = 232*esc, 792*esc
        capas = tiers(cx, y_top, y_bot, 5, 372*esc, 60*esc)
    p = []
    if fondo:
        p.append(f'<rect width="{size}" height="{size}" fill="{VERDE_FONDO}"/>')
        p.append(f'<circle cx="{cx}" cy="{cx}" r="{size*0.455:.0f}" fill="none" stroke="{VERDE_MEDIO}" stroke-width="{3*esc:.1f}"/>')
    # tronco
    tw, th = (30 if not con_texto else 24)*esc, (58 if not con_texto else 46)*esc
    p.append(f'<rect x="{cx-tw/2:.1f}" y="{y_bot:.1f}" width="{tw:.1f}" height="{th:.1f}" rx="{5*esc:.1f}" fill="{SALVIA_OSC}"/>')
    # ramas de atras a adelante
    for d, i in reversed(capas):
        col = SALVIA if i % 2 == 0 else SALVIA_OSC
        p.append(f'<path d="{d}" fill="{col}"/>')
    # estrella dorada
    sy = y_top - (42 if not con_texto else 32)*esc
    r1, r2 = (38 if not con_texto else 28)*esc, (16 if not con_texto else 11.5)*esc
    import math
    pts = []
    for k in range(10):
        r = r1 if k % 2 == 0 else r2
        a = -math.pi/2 + k * math.pi/5
        pts.append(f"{cx + r*math.cos(a):.1f},{sy + r*math.sin(a):.1f}")
    p.append(f'<polygon points="{" ".join(pts)}" fill="{DORADO}"/>')
    if con_texto:
        p.append(f'<text x="{cx}" y="{838*esc:.0f}" font-family="Georgia,serif" font-size="{86*esc:.0f}" font-weight="bold" fill="{CREMA}" text-anchor="middle" letter-spacing="{1*esc:.1f}">ÁRBOLES</text>')
        p.append(f'<text x="{cx}" y="{906*esc:.0f}" font-family="Georgia,serif" font-size="{44*esc:.0f}" fill="{DORADO}" text-anchor="middle" letter-spacing="{9*esc:.1f}">DE NAVIDAD</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">{"".join(p)}</svg>'

base = "/home/claude/arbolesdenavidad/assets/marca/"
combos = [
    ("perfil-instagram.png",  dict(con_texto=False, fondo=True),  1080),
    ("logo-con-texto.png",    dict(con_texto=True,  fondo=True),  1080),
    ("isotipo-transparente.png", dict(con_texto=False, fondo=False), 1080),
]
for nombre, kw, s in combos:
    svg = arbol_svg(size=s, **kw)
    open(base + nombre.replace(".png", ".svg"), "w").write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=base + nombre, output_width=s, output_height=s)
    print("->", nombre)

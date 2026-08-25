import base64, cairosvg
from PIL import Image

W, H = 1080, 1350
VERDE = "#0E2A1C"; SALVIA = "#BACDB4"; DORADO = "#C9A227"; CREMA = "#F2EFE6"

# foto insignia recortada a 4:5
src = Image.open("/home/claude/arbolesdenavidad/assets/fotos-historicas/arbol-25.jpg").convert("RGB")
r = max(W/src.width, H/src.height)
src = src.resize((int(src.width*r), int(src.height*r)), Image.LANCZOS)
l = (src.width - W)//2; t = (src.height - H)//2
src.crop((l, t, l+W, t+H)).save("/home/claude/_bg.jpg", quality=92)
b64 = base64.b64encode(open("/home/claude/_bg.jpg","rb").read()).decode()

iso = open("/home/claude/arbolesdenavidad/assets/marca/isotipo-transparente.svg").read()
iso_inner = iso.split(">",1)[1].rsplit("</svg>",1)[0]

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
  <linearGradient id="vel" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%"   stop-color="{VERDE}" stop-opacity="0.95"/>
    <stop offset="37%"  stop-color="{VERDE}" stop-opacity="0.90"/>
    <stop offset="50%"  stop-color="{VERDE}" stop-opacity="0.26"/>
    <stop offset="62%"  stop-color="{VERDE}" stop-opacity="0.82"/>
    <stop offset="100%" stop-color="{VERDE}" stop-opacity="0.99"/>
  </linearGradient>
</defs>
<image href="data:image/jpeg;base64,{b64}" x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>
<rect width="{W}" height="{H}" fill="url(#vel)"/>
<rect x="34" y="34" width="{W-68}" height="{H-68}" fill="none" stroke="{DORADO}" stroke-width="2" opacity="0.5"/>

<g transform="translate(464,74) scale(0.144)">{iso_inner}</g>

<text x="540" y="300" font-family="Georgia,serif" font-size="66" font-weight="bold" fill="{CREMA}" text-anchor="middle">ÁRBOLES DE NAVIDAD</text>
<text x="540" y="360" font-family="Georgia,serif" font-size="66" font-weight="bold" fill="{CREMA}" text-anchor="middle">NATURALES</text>
<line x1="400" y1="398" x2="680" y2="398" stroke="{DORADO}" stroke-width="2"/>
<text x="540" y="452" font-family="Georgia,serif" font-size="40" fill="{DORADO}" text-anchor="middle" letter-spacing="4">ABETO NOBLE DE OREGON</text>

<text x="540" y="884" font-family="Georgia,serif" font-size="40" fill="{CREMA}" text-anchor="middle">De 1 a 6 metros · Entrega a domicilio</text>
<text x="540" y="936" font-family="Georgia,serif" font-size="34" fill="{SALVIA}" text-anchor="middle">CDMX y Estado de México</text>

<g font-family="Georgia,serif" font-size="29" fill="{SALVIA}">
  <rect x="126" y="1000" width="13" height="13" fill="{DORADO}" transform="rotate(45 132.5 1006.5)"/>
  <text x="164" y="1013">Retiene más del 90% de su aguja a 28 días</text>
  <rect x="126" y="1044" width="13" height="13" fill="{DORADO}" transform="rotate(45 132.5 1050.5)"/>
  <text x="164" y="1057">Rama rígida: aguanta adornos pesados</text>
  <rect x="126" y="1088" width="13" height="13" fill="{DORADO}" transform="rotate(45 132.5 1094.5)"/>
  <text x="164" y="1101">Importación verificada por PROFEPA</text>
</g>

<rect x="96" y="1136" width="888" height="96" rx="8" fill="{DORADO}"/>
<text x="540" y="1182" font-family="Georgia,serif" font-size="38" font-weight="bold" fill="{VERDE}" text-anchor="middle">PREVENTA: [XX]% DE DESCUENTO</text>
<text x="540" y="1218" font-family="Georgia,serif" font-size="28" fill="{VERDE}" text-anchor="middle">apartando antes del [XX DE MES]</text>

<text x="540" y="1276" font-family="Georgia,serif" font-size="31" fill="{CREMA}" text-anchor="middle">Aparta el tuyo en  [TUSITIO.COM]</text>
<text x="540" y="1318" font-family="Georgia,serif" font-size="27" fill="{DORADO}" text-anchor="middle">@arbolesdenavidad.mx</text>
</svg>'''

out = "/home/claude/arbolesdenavidad/assets/flyers/"
open(out+"flyer-preventa.svg","w").write(svg)
cairosvg.svg2png(bytestring=svg.encode(), write_to=out+"flyer-preventa.png", output_width=W, output_height=H)
print("flyer listo")

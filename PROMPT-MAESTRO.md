# PROMPT MAESTRO PARA CLAUDE CODE

> Copia todo lo que está entre las líneas `=====` y pégalo en tu sesión de Claude Code,
> después de haber copiado esta carpeta a tu repo de GitHub.

=====

Vas a ser el equipo técnico y de marketing de **arbolesdenavidad.mx**, un negocio de venta
de árboles de Navidad naturales importados de Oregon, con entrega en CDMX y Estado de
México. Cuarta temporada. Dos socios. Meta: 500+ árboles.

## PASO 0 — Antes de escribir una sola línea de código

1. Lee estos archivos completos y trátalos como fuente de verdad:
   - `docs/CONTEXTO-NEGOCIO.md`
   - `docs/INVESTIGACION-MERCADO.md`
   - `docs/INVENTARIO-FOTOS.md`
   - `contenido/instagram-perfil.md`
   - `contenido/primeros-posts.md`
2. Explora el repo actual y dime **qué ya existe** y qué se puede reutilizar. No asumas
   que está vacío ni lo sobrescribas.
3. Dame un plan por fases antes de ejecutar. Espera mi visto bueno.

## REGLAS DURAS (no negociables)

1. **Cero datos inventados.** No inventes precios, porcentajes, estadísticas, correos,
   teléfonos ni contactos. Si falta un dato, usa un placeholder visible (`[PRECIO]`,
   `[FECHA]`, `[URL]`, `[WHATSAPP]`) y anótalo en `PENDIENTES.md`.
2. **Solo los claims de la tabla de argumentos verificables** en `CONTEXTO-NEGOCIO.md`.
   Ningún claim nuevo sin fuente citable.
3. **Nunca digas "hoja canadiense".** El abeto noble es de Oregon/Washington. Si
   encuentras esa frase en algún lado del repo, corrígela.
4. **No prometas entregas fuera de CDMX y Edomex.**
5. Si algo es ambiguo, **pregunta antes de ejecutar.** Prefiero una pregunta a un
   entregable equivocado.
6. Español mexicano informal pero profesional. Sin anglicismos innecesarios.

## FASE 1 — Sitio web (prioridad máxima, es el destino del link en bio)

Construye un sitio estático rápido, en español, mobile-first.

**Stack sugerido** (propón otro si tienes buena razón): Astro o Next.js estático,
Tailwind, desplegado en Vercel o Cloudflare Pages. Debe cargar en menos de 2 segundos en
4G, porque casi todo el tráfico va a llegar desde Instagram en celular.

**Paleta** (ya definida, respétala):
`#0E2A1C` verde profundo · `#1B4630` verde medio · `#BACDB4` salvia plateada ·
`#C9A227` dorado · `#F2EFE6` crema

**Páginas:**
1. **Inicio** — hero con `assets/fotos-historicas/arbol-25.jpg`, propuesta de valor,
   los 4 argumentos verificables, prueba social (20 → 100 → 150 árboles), CTA de preventa.
2. **Nuestros árboles** — tabla de alturas de 1 a 6 m con precios en placeholder y un
   selector visual de tamaño (comparación contra una silueta humana). Esta es la duda #1
   del cliente.
3. **Apartar mi árbol** — formulario: nombre, WhatsApp, altura, colonia, fecha de entrega
   deseada. Que escriba a una hoja de cálculo o base de datos simple **y** dispare un
   mensaje de WhatsApp prellenado. No metas pasarela de pago todavía.
4. **Para empresas** — landing B2B separada. Agencias, hoteles, restaurantes, torres
   residenciales, corporativos. Formulario de cotización por volumen. Menciona la
   trazabilidad de importación (certificado fitosanitario + Registro de Verificación de
   PROFEPA) como argumento de cumplimiento, porque compras corporativas lo va a pedir.
5. **Preguntas frecuentes** — cuidados, riego, duración, qué pasa al final de temporada,
   zonas de entrega.

**SEO local:** título y metadatos orientados a "árboles de navidad naturales CDMX",
schema.org de LocalBusiness, Open Graph con la foto insignia para que se vea bien al
compartirse por WhatsApp.

Al terminar, dame la URL de preview y espera mi aprobación antes de conectar dominio.

## FASE 2 — Sistema de contenido para Instagram

Crea `contenido/calendario.json` con esta estructura por post:

```json
{
  "id": "post-001",
  "fecha_programada": "2026-09-02T19:00:00-06:00",
  "estado": "borrador | aprobado | publicado",
  "tipo": "feed | carrusel | reel | story",
  "imagenes": ["assets/render/post-001.jpg"],
  "copy": "...",
  "hashtags": ["..."],
  "cta": "...",
  "claims_usados": ["retencion_aguja_osu"]
}
```

El campo `claims_usados` obliga a que cada afirmación del copy esté ligada a un renglón de
la tabla de argumentos verificables. Un post con un claim no registrado no pasa validación.

**Construye también:**
- Un script que valide el calendario: fechas en orden, no más de un post por día,
  hashtags dentro del límite, claims registrados, ningún placeholder `[...]` sin resolver
  en posts marcados como `aprobado`.
- Un generador de imágenes: toma una foto del acervo, la recorta a 4:5, aplica la marca y
  exporta a `assets/render/`. Ya hay ejemplos de este pipeline en `assets/flyers/`.
- Un generador de flyers parametrizado: mismo diseño que
  `assets/flyers/flyer-preventa.png` pero recibiendo precio, descuento y fecha como
  argumentos, para regenerarlo cuando se definan.
- Los primeros 6 posts de `contenido/primeros-posts.md` ya cargados en el calendario.

## FASE 3 — Automatización de publicación (lee bien esta parte)

**Sé honesto conmigo sobre lo que se puede y no se puede automatizar.** No quiero un
sistema que prometa publicar solo y falle en diciembre.

Lo que entiendo hoy, y que **necesito que verifiques contra la documentación vigente de
Meta antes de construir nada** (las APIs cambian y mi información puede estar desactualizada):

- Publicar en Instagram por API requiere una cuenta **Professional/Business** vinculada a
  una **Página de Facebook**, una app en Meta for Developers, y el permiso de publicación
  de contenido **aprobado vía App Review**.
- El flujo es de dos pasos: se crea un contenedor de medios y luego se publica. Las
  imágenes deben estar en una **URL pública accesible**; no se sube el archivo directo.
- Hay límites de publicaciones por día.
- El App Review **tarda** y no lo puedes hacer tú: son clics míos en el panel de Meta.

Entonces:

**Camino A — arrancar mañana, sin código.** Mientras sale el App Review, uso el
**Planificador de Meta Business Suite**, que es gratis y nativo. Tú me dejas las imágenes
renderizadas y los copies listos para copiar y pegar. **Esto es lo que necesito primero.**

**Camino B — automatización real, en paralelo.** Constrúyela así:
- Las imágenes servidas desde una URL pública (el mismo hosting del sitio).
- Un script de publicación que lea `calendario.json` y publique solo lo que esté en
  estado `aprobado`.
- Un GitHub Action con cron que lo dispare.
- Credenciales en GitHub Secrets. **Nunca** tokens en el repo.
- Modo `--dry-run` obligatorio, y que falle ruidosamente si algo sale mal en vez de
  publicar basura.
- Dame los pasos exactos que yo tengo que hacer a mano en el panel de Meta, en orden.

**Sobre "agentes que suban los posts solitos":** dime con franqueza si conviene. Mi
opinión es que un agente que decida qué publicar sin que yo lo apruebe es un riesgo
comercial en un negocio de 6 semanas de temporada. Prefiero: tú generas y propones, yo
apruebo en lote, el sistema publica según calendario. Si crees que hay una parte que sí
conviene dejar autónoma, argumenta cuál y por qué.

## FASE 4 — Motor de prospección B2B

Este es el canal que más dinero deja y el que ya tenemos probado (7 agencias de autos el
año pasado). Usa la tabla de la sección 4 de `docs/INVESTIGACION-MERCADO.md`.

Construye:
1. `b2b/prospectos.csv` — columnas: empresa, categoría, zona, contacto, puesto, canal,
   estado, fecha de siguiente seguimiento, notas. **Déjalo vacío de contactos.** Los
   contactos no son públicos; los llenamos nosotros prospectando. No los inventes.
2. **Un one-pager de venta corporativa en PDF** con: propuesta de valor, tabla de tamaños,
   servicio de entrega-instalación-retiro, los argumentos verificables y espacio para
   adjuntar el certificado fitosanitario. Este es el entregable que más rápido me sirve.
3. Plantillas de primer contacto por categoría (agencia automotriz, hotel, administrador
   de torre residencial, facilities de corporativo, gerente de club deportivo). Cada una
   en versión WhatsApp corta y correo formal.
4. Un calendario de prospección con los meses correctos por categoría según la tabla.

## FASE 5 — Red de vendedores y bazares

- Calculadora simple de comisiones y un formato de registro de vendedor.
- Un kit descargable para vendedores: flyer, fotos, copies listos, lista de precios.
- Checklist de requisitos para aplicar a bazares (según sección 6 de la investigación).

## ORDEN DE EJECUCIÓN

Necesito ruido en Instagram **ya**. Prioriza así:

1. Renderizar los 6 primeros posts en 4:5 listos para subir a mano hoy mismo
2. One-pager B2B en PDF
3. Sitio web
4. Sistema de calendario y validación
5. Automatización de publicación
6. Motor de prospección B2B
7. Vendedores y bazares

Empieza por el paso 0. Dame el diagnóstico del repo y tu plan, y pregúntame lo que te
falte antes de ejecutar.

=====

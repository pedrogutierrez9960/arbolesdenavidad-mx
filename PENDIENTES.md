# PENDIENTES — datos que faltan y bloquean entregables

> Bitácora de la regla dura #1: cero datos inventados. Todo lo que aparece aquí
> va como placeholder visible (`[PRECIO]`, `[FECHA]`, `[URL]`, `[WHATSAPP]`)
> hasta que se confirme.
>
> Última actualización: 25 de agosto de 2026

## 🔴 Bloquean algo que ya está construido

| # | Dato | Qué bloquea | Placeholder actual |
|---|---|---|---|
| 1 | **% de descuento de preventa** | Post 6, flyer de preventa, kit de vendedores | `[XX]%` |
| 2 | **Fecha límite de preventa** | Post 6, flyer de preventa | `[XX DE MES]` |
| 3 | **Precios por altura (1 a 6 m), temporada 2026** | Página "Nuestros árboles", one-pager B2B, lista de precios de vendedores | `[PRECIO]` |
| 4 | **Número de WhatsApp de ventas** | Formulario "Apartar mi árbol", botón de contacto del perfil, plantillas B2B | `[WHATSAPP]` |
| 5 | **Dominio confirmado y activo** | Link en bio, Open Graph, flyer, one-pager | `[TUSITIO.COM]` |

**Referencia para fijar el precio (dato con fuente, no supuesto):** la tabla de
precios de navidadacasa.com en `docs/INVESTIGACION-MERCADO.md` §3. Ahí está el
benchmark premium real del competidor directo con entrega en CDMX, más el piso
de mercado de autocorte. El noble trae sobreprecio de ~40-60% sobre el Douglas
del mismo tamaño.

## 🟡 Bloquean fases siguientes

| # | Dato | Qué bloquea |
|---|---|---|
| 6 | **Nombre comercial legal / razón social** | Facturación B2B, contratos de bazar, alta como proveedor |
| 7 | **Dirección del punto físico** para que el cliente vea los árboles | Página de contacto, schema.org LocalBusiness, post 5 |
| 8 | **Dónde aterrizan los datos del formulario** (Google Sheet, Airtable, etc.) | Formulario de "Apartar mi árbol" y el B2B |
| 9 | **Repo de GitHub dedicado** para arbolesdenavidad.mx | Despliegue del sitio, GitHub Actions, secrets de la automatización |
| 10 | **Cuenta de Instagram en modo Profesional/Empresa + Página de Facebook** | Planificador de Meta Business Suite y toda la Fase 3 |

## 🟢 Decisiones de contenido pendientes

| # | Pregunta | Contexto |
|---|---|---|
| 11 | **¿Cuáles 4 argumentos verificables van al hero del sitio?** | El brief pide 4, pero la tabla de `CONTEXTO-NEGOCIO.md` tiene 5 renglones. Falta decidir cuál se queda fuera (o si van los 5). En el one-pager entraron 4 y quedó fuera "Importación verificada por PROFEPA" porque ese argumento ya tiene su propia sección de trazabilidad. |
| 12 | Confirmar si **"Citimarket"** es City Market (Grupo La Comer) | `INVESTIGACION-MERCADO.md` §5 lo marca como no verificado. Confirmar antes de invertir tiempo en ese canal. |
| 13 | 🚩 **¿De verdad ofrecen instalación y retiro?** | El brief pide que el one-pager diga "entrega-instalación-retiro", pero `CONTEXTO-NEGOCIO.md` solo documenta entrega a domicilio. Lo incluí como lo pediste **y ya está impreso en el PDF**. Si no dan retiro en enero, hay que quitarlo antes de mandárselo a un cliente: es una promesa de servicio, no un argumento de marketing. |
| 14 | **Correo de contacto del negocio** | Va en el one-pager y en el perfil. Hoy es `[CORREO]`. |

## 📸 Producción de fotografía (prioritario, no opcional)

`INVENTARIO-FOTOS.md` ya lo advierte y al medir las fotos lo confirmé: **solo 4
del acervo tienen resolución real para feed a sangre completa** (`arbol-25`,
`19`, `18`, `05`, todas de 960×1280). Las demás son de 720 o 591 px de ancho, o
están en horizontal.

Alcanza para arrancar. No alcanza para la temporada.

| # | Toma que falta | Para qué |
|---|---|---|
| 13 | **Macro de la aguja** mostrando el envés plateado | Es la prueba visual del argumento "abeto noble" y no existe ninguna |
| 14 | **Comparativa de escala real** — persona junto a árboles de 1, 2, 3 y 4 m | Hoy el post 4 usa un gráfico vectorial; una foto real convence más |
| 15 | **Proceso de entrega** — camioneta, árbol en malla, entrega en la puerta | Vende el servicio, que es tu diferenciador, no solo el producto |
| 16 | **Antes/después** — recién entregado vs. decorado | Contenido de alto rendimiento en redes |
| 17 | **Instalación B2B** — árbol grande en showroom u oficina | Es el material de venta corporativa y no existe ninguno |
| 18 | **Fondo limpio en el lote** — sin lonas azules, cables ni botes | Convierte fotos de Stories en fotos de feed |
| 19 | **Foto de los dos socios** en el lote | El post 2 la pide; hoy usa la banda de inventario |

## ✅ Resuelto

| Dato | Resolución |
|---|---|
| Prueba social | 20 → 100 → 150 árboles, confirmado contra `CONTEXTO-NEGOCIO.md` |
| Zona de entrega | CDMX y Estado de México, nunca fuera |
| "Hoja canadiense" | Revisado todo el repo: no se usa en ninguna pieza. El abeto noble es de Oregon/Washington |
| Tipografía de marca | EB Garamond (display) + Lato (cuerpo y todas las cifras). Georgia no existe en Linux y caía a una fallback genérica |

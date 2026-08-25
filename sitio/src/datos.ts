/**
 * DATOS DEL NEGOCIO — arbolesdenavidad.mx
 * ========================================
 * Punto único donde se llenan los datos pendientes. Cambiar aquí actualiza
 * TODO el sitio: no hay que buscar en las páginas.
 *
 * Lo que está en `null` sale en el sitio como placeholder visible amarillo
 * (`[WHATSAPP]`, `[PRECIO]`...), según la regla dura #1: cero datos
 * inventados. Ver PENDIENTES.md en la raíz del repo.
 */

// ── Pendientes de definir ──────────────────────────────────────────────
export const NEGOCIO = {
  /** Solo dígitos con lada país, ej: "5215512345678" */
  whatsapp: null as string | null,
  correo: null as string | null,
  /** Dirección del punto físico donde el cliente puede venir a ver los árboles */
  direccion: null as string | null,
  /** Porcentaje sin signo, ej: 15 */
  descuentoPreventa: null as number | null,
  /** Fecha límite de preventa, ej: "30 de septiembre" */
  fechaLimitePreventa: null as string | null,
  /**
   * URL del Web App de Google Apps Script (o endpoint equivalente) que
   * escribe las solicitudes a la hoja de cálculo. Mientras sea null, el
   * formulario funciona igual pero solo por WhatsApp.
   */
  endpointFormulario: null as string | null,
};

export const SITIO = {
  url: "https://arbolesdenavidad.mx",
  nombre: "Árboles de Navidad Naturales",
  instagram: "arbolesdenavidad.mx",
  instagramUrl: "https://instagram.com/arbolesdenavidad.mx",
};

// ── Datos confirmados (docs/CONTEXTO-NEGOCIO.md) ───────────────────────
export const HISTORIA = [
  { anio: "Año 1", arboles: 20 },
  { anio: "Año 2", arboles: 100 },
  { anio: "Año 3", arboles: 150 },
];

export const TOTAL_ENTREGADOS = HISTORIA.reduce((s, t) => s + t.arboles, 0); // 270

export const COBERTURA = "Ciudad de México y Estado de México";

/**
 * Argumentos verificables. SOLO estos, cada uno con su respaldo.
 * Fuente: tabla de docs/CONTEXTO-NEGOCIO.md. Ningún claim nuevo sin fuente.
 */
export const ARGUMENTOS = [
  {
    id: "retencion_aguja_osu",
    titulo: "Aguanta la temporada completa",
    texto: "Retiene más del 90% de su aguja a los 28 días, manteniéndolo hidratado.",
    fuente: "Christmas Tree Research Program, Oregon State University (~21 °C, 30-40% de humedad)",
  },
  {
    id: "rama_rigida",
    titulo: "La rama aguanta tus esferas",
    texto: "Rama rígida y horizontal: soporta adornos pesados sin doblarse.",
    fuente: "Característica estructural documentada del abeto noble",
  },
  {
    id: "oregon_mayor_productor",
    titulo: "Del mayor productor de EE.UU.",
    texto: "Oregon es el estado que más árboles de Navidad produce en Estados Unidos.",
    fuente: "Oregon Department of Agriculture / USDA",
  },
  {
    id: "plantaciones_comerciales",
    titulo: "Comprar natural no deforesta",
    texto: "Vienen de plantaciones comerciales sembradas para esto, no de bosque nativo.",
    fuente: "SEMARNAT",
  },
  {
    id: "profepa_verificado",
    titulo: "Importación verificada",
    texto: "Cada embarque es verificado por PROFEPA al entrar al país.",
    fuente: "NOM-013-SEMARNAT-2020",
  },
];

/** Alturas. El precio se llena cuando se defina (PENDIENTES.md #3). */
export const ALTURAS = [
  { rango: "1 a 1.5 m", metros: 1.25, uso: "Departamentos, mesas, oficinas chicas", precio: null },
  { rango: "1.8 a 2.2 m", metros: 2.0, uso: "Sala de casa normal. La medida más pedida", precio: null, destacado: true },
  { rango: "2.5 a 3 m", metros: 2.75, uso: "Salas de doble altura, entradas", precio: null },
  { rango: "4 a 6 m", metros: 5.0, uso: "Lobbies, showrooms, oficinas, plazas", precio: null },
];

// ── Utilidades ─────────────────────────────────────────────────────────

/** Liga de WhatsApp con mensaje prellenado. Si no hay número, va a null. */
export function ligaWhatsApp(mensaje: string): string | null {
  if (!NEGOCIO.whatsapp) return null;
  return `https://wa.me/${NEGOCIO.whatsapp}?text=${encodeURIComponent(mensaje)}`;
}

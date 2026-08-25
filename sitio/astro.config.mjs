import { defineConfig } from 'astro/config';
import tailwind from '@tailwindcss/vite';

// Sitio estático puro: Astro no manda JavaScript al cliente por defecto.
// Es la razón de elegirlo sobre Next: el tráfico llega de Instagram en 4G.
export default defineConfig({
  site: 'https://arbolesdenavidad.mx',
  vite: { plugins: [tailwind()] },
  build: { inlineStylesheets: 'always' },
  compressHTML: true,
});

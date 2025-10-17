import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  base: '/',
  preview: {
    port: 80,
    host: true,
    // SPA fallback:
    headers: {
      "Cache-Control": "no-cache"
    },
   },
   server: {
      host: true,
   },
   build: {
      outDir: "dist",
   },
})

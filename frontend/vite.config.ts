import { defineConfig} from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    watch: {
      usePolling: true, // Fixes hot reload in Docker
    },
    host: true, // Needed for Docker port mapping
    strictPort: true,
    port: 5173, 
  }
})

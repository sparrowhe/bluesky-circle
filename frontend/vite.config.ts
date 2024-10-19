import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"
 
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  base: "./",
  build: {
    assetsDir: 'static',
  },
  server: {
    port: 3000,
    cors: true,
    proxy: {
      "/generate": {
        target: "https://circle.sparrowhe.top/",
        changeOrigin: true,
        secure: false,
      },
    },
  },
})
import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  build: {
    manifest: true,
    outDir: resolve('./dist'),
    emptyOutDir: true,
    sourcemap: true,
    rollupOptions: {
      input: {
        main: resolve('src/main.js'),
      },
    },
  },
  plugins: [
    vue(),
    vuetify({
      autoImport: true,
    }),
  ],
  server: {
    port: 3000,
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  base: '/',
  test: {
    environment: 'jsdom',
    setupFiles: ['./__tests__/setupVuetify.js', './__tests__/setupPlugins.js'],
    deps: {
      inline: ['vuetify'],
    },
  },
})

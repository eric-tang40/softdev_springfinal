import { defineConfig } from "vite"; 
import vue from "@vitejs/plugin-vue";

const backendPath = '../billboard';
// https://vitejs.dev/config/ 
export default defineConfig({
  plugins: [vue()], 
  base: '/static/vite/', 
  server: {
  watch: { 
    ignored: [],
    },
  },
  build: {
    manifest: true,
    emptyOutDir: true,
    outDir: backendPath + '/core/static/vite/', rollupOptions: {
    input: {
      vue_song_show: "./src/apps/song_show/song_show.js",
      }, 
    },
  }, 
});
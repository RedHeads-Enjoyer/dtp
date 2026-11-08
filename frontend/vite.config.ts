import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    host: "0.0.0.0",
    port: Number(process.env.CLIENT_PORT),
    watch: {
      usePolling: true,
    },
    proxy: {
      "/api": `http://backend:${process.env.SERVER_PORT}`,
    },
  },
});
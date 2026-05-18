import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  preview: {
    allowedHosts: ["gma-frontend.up.railway.app"],
  },
});

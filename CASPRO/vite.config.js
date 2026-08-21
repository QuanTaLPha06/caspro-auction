import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Stamped into the bundle so you can tell at a glance which build a screen is
// actually running — the quickest way to spot a stale deployment.
const BUILD_STAMP = new Date().toISOString().slice(0, 16).replace('T', ' ') + ' UTC';

export default defineConfig({
  define: {
    __BUILD_STAMP__: JSON.stringify(BUILD_STAMP),
  },
  plugins: [react()],
  // Expose players.json from the project root so it can be imported in src/
  resolve: {
    alias: {},
  },
});

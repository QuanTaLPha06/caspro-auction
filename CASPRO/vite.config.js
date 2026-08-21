import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  // Expose players.json from the project root so it can be imported in src/
  resolve: {
    alias: {},
  },
});

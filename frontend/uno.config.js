import { defineConfig, presetUno, presetAttributify } from 'unocss'

export default defineConfig({
  presets: [
    presetUno(), // Tailwind-like utilities
    presetAttributify(), // Optional: attribute mode
  ],
})

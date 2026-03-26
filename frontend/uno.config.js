import { 
  defineConfig,
  presetUno,
  presetAttributify,
  presetIcons,
} from 'unocss'

export default defineConfig({
  presets: [
    presetUno(), // Tailwind-like utilities
    presetAttributify(), // Optional: attribute mode
    // Icons
    presetIcons({
      prefix: 'i-',
      extraProperties: {
        'display': 'inline-block',
        'vertical-align': 'middle'
      },
    }),
  ],
  theme: {
    fontFamily: {
      header: 'Tajawal, serif',
      body: 'Zain, sans-serif'
    },
    
    colors: {
      brand: {
        bg: 'var(--brand-bg)',
        text: 'var(--brand-text)',
        primary: 'var(--brand-primary)'
      }
    }
  }
})

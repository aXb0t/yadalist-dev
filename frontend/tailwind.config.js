/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './src/**/*.{html,js}',
    './stories/**/*.{html,js}',
    '../**/templates/**/*.html', // Include Django templates
  ],
  theme: {
    extend: {
      colors: {
        // Nord Theme Colors
        // Polar Night (dark backgrounds)
        nord0: '#2E3440',
        nord1: '#3B4252',
        nord2: '#434C5E',
        nord3: '#4C566A',

        // Snow Storm (light backgrounds)
        nord4: '#D8DEE9',
        nord5: '#E5E9F0',
        nord6: '#ECEFF4',

        // Frost (blues/cyans)
        nord7: '#8FBCBB',
        nord8: '#88C0D0',
        nord9: '#81A1C1',
        nord10: '#5E81AC',

        // Aurora (accent colors)
        nord11: '#BF616A', // red
        nord12: '#D08770', // orange
        nord13: '#EBCB8B', // yellow
        nord14: '#A3BE8C', // green
        nord15: '#B48EAD', // purple

        // Semantic aliases
        primary: '#5E81AC',     // nord10
        'primary-hover': '#81A1C1', // nord9
        secondary: '#88C0D0',   // nord8
        success: '#A3BE8C',     // nord14
        warning: '#EBCB8B',     // nord13
        error: '#BF616A',       // nord11
        info: '#8FBCBB',        // nord7

        // UI colors
        background: '#ECEFF4',  // nord6
        surface: '#E5E9F0',     // nord5
        card: '#FFFFFF',
        text: '#2E3440',        // nord0
        'text-muted': '#4C566A', // nord3
        border: '#D8DEE9',      // nord4
      },
      fontFamily: {
        sans: [
          'Inter',
          '-apple-system',
          'BlinkMacSystemFont',
          '"Segoe UI"',
          'Roboto',
          '"Helvetica Neue"',
          'Arial',
          'sans-serif',
        ],
        mono: [
          '"Fira Code"',
          '"SF Mono"',
          'Monaco',
          'Consolas',
          'monospace',
        ],
      },
      borderRadius: {
        DEFAULT: '0.375rem', // 6px
        'sm': '0.25rem',     // 4px
        'md': '0.5rem',      // 8px
        'lg': '0.75rem',     // 12px
      },
      boxShadow: {
        'sm': '0 1px 2px 0 rgba(46, 52, 64, 0.05)',
        DEFAULT: '0 2px 4px 0 rgba(46, 52, 64, 0.1)',
        'md': '0 4px 6px -1px rgba(46, 52, 64, 0.1), 0 2px 4px -1px rgba(46, 52, 64, 0.06)',
        'lg': '0 10px 15px -3px rgba(46, 52, 64, 0.1), 0 4px 6px -2px rgba(46, 52, 64, 0.05)',
      },
    },
  },
  plugins: [],
}

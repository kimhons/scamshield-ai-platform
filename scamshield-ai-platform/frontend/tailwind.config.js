/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'Monaco', 'Consolas', 'Liberation Mono', 'Courier New', 'monospace']
      },
      colors: {
        // Professional Enterprise Color Palette
        navy: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
          primary: '#1a1f36',
          secondary: '#232a47',
          tertiary: '#2d3656'
        },
        blue: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#0066cc', // Professional blue
          700: '#0052a3',
          800: '#1e40af',
          900: '#1e3a8a',
          primary: '#0066cc'
        },
        orange: {
          alert: '#ff6b35',
          'alert-light': '#ff8458',
          'alert-dark': '#e65528'
        }
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem'
      },
      borderRadius: {
        'xl': '0.75rem',
        '2xl': '1rem',
        '3xl': '1.5rem'
      },
      boxShadow: {
        'enterprise': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'enterprise-lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'enterprise-xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)'
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out'
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        },
        scaleIn: {
          '0%': { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' }
        }
      },
      typography: {
        DEFAULT: {
          css: {
            color: '#374151',
            maxWidth: 'none',
            '[class~="lead"]': {
              color: '#6b7280'
            },
            strong: {
              color: '#111827',
              fontWeight: '600'
            },
            'h1, h2, h3, h4': {
              color: '#111827',
              fontWeight: '700'
            }
          }
        }
      }
    }
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
    // Custom plugin for enterprise utilities
    function({ addUtilities }) {
      const newUtilities = {
        '.text-enterprise': {
          color: '#1a1f36'
        },
        '.bg-enterprise': {
          backgroundColor: '#1a1f36'
        },
        '.border-enterprise': {
          borderColor: '#1a1f36'
        },
        '.focus-enterprise': {
          '&:focus': {
            outline: 'none',
            boxShadow: '0 0 0 2px #0066cc',
            borderColor: '#0066cc'
          }
        }
      }
      addUtilities(newUtilities)
    }
  ]
}
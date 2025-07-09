/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ['class'],
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)'
      },
      colors: {
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))'
        },
        popover: {
          DEFAULT: 'hsl(var(--popover))',
          foreground: 'hsl(var(--popover-foreground))'
        },
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
          dark: 'hsl(var(--primary-dark))',
          light: 'hsl(var(--primary-light))',
          50: '#fff7ed',
          100: '#ffedd5',
          200: '#fed7aa',
          300: '#fdba74',
          400: '#fb923c',
          500: '#f97316',
          600: '#ea580c',
          700: '#c2410c',
          800: '#9a3412',
          900: '#7c2d12'
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))'
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
          light: 'hsl(var(--muted-light))'
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
          dark: 'hsl(var(--accent-dark))',
          light: 'hsl(var(--accent-light))',
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a'
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))'
        },
        success: {
          DEFAULT: 'hsl(var(--success))',
          foreground: 'hsl(var(--success-foreground))',
          50: '#ecfdf5',
          100: '#d1fae5',
          200: '#a7f3d0',
          300: '#6ee7b7',
          400: '#34d399',
          500: '#10b981',
          600: '#059669',
          700: '#047857',
          800: '#065f46',
          900: '#064e3b'
        },
        warning: {
          DEFAULT: 'hsl(var(--warning))',
          foreground: 'hsl(var(--warning-foreground))',
          50: '#fffbeb',
          100: '#fef3c7',
          200: '#fde68a',
          300: '#fcd34d',
          400: '#fbbf24',
          500: '#f59e0b',
          600: '#d97706',
          700: '#b45309',
          800: '#92400e',
          900: '#78350f'
        },
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        chart: {
          '1': 'hsl(var(--chart-1))',
          '2': 'hsl(var(--chart-2))',
          '3': 'hsl(var(--chart-3))',
          '4': 'hsl(var(--chart-4))',
          '5': 'hsl(var(--chart-5))'
        },
        // Premium Glass Colors
        glass: {
          light: 'rgba(255, 255, 255, 0.1)',
          medium: 'rgba(255, 255, 255, 0.05)',
          dark: 'rgba(0, 0, 0, 0.3)'
        }
      },
      animation: {
        // Entrance Animations
        'fade-in': 'fadeIn 0.6s ease-out',
        'fade-in-up': 'fadeInUp 0.6s ease-out',
        'fade-in-down': 'fadeInDown 0.6s ease-out',
        'fade-in-left': 'fadeInLeft 0.6s ease-out',
        'fade-in-right': 'fadeInRight 0.6s ease-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'slide-down': 'slideDown 0.4s ease-out',
        'scale-in': 'scaleIn 0.3s ease-out',
        'scale-up': 'scaleUp 0.3s ease-out',
        
        // Continuous Animations
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
        'pulse-glow-accent': 'pulse-glow-accent 2s ease-in-out infinite',
        'float': 'float 6s ease-in-out infinite',
        'float-delayed': 'float 6s ease-in-out infinite 3s',
        'rotate-slow': 'rotate-slow 10s linear infinite',
        'spin-slow': 'spin-slow 3s linear infinite',
        'bounce-subtle': 'bounce-subtle 2s ease-in-out infinite',
        
        // Interactive Animations
        'wiggle': 'wiggle 1s ease-in-out infinite',
        'shake': 'shake 0.82s cubic-bezier(.36,.07,.19,.97) both',
        'ping-soft': 'ping-soft 1s cubic-bezier(0, 0, 0.2, 1) infinite',
        
        // Loading Animations
        'loading-dots': 'loading-dots 1.4s ease-in-out infinite both',
        'loading-bars': 'loading-bars 1.2s ease-in-out infinite',
        'shimmer': 'shimmer 2s linear infinite',
        
        // Background Animations
        'gradient-x': 'gradient-x 15s ease infinite',
        'gradient-y': 'gradient-y 15s ease infinite',
        'gradient-xy': 'gradient-xy 15s ease infinite',
      },
      keyframes: {
        // Entrance Keyframes
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        },
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        },
        fadeInDown: {
          '0%': { opacity: '0', transform: 'translateY(-20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        },
        fadeInLeft: {
          '0%': { opacity: '0', transform: 'translateX(-20px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' }
        },
        fadeInRight: {
          '0%': { opacity: '0', transform: 'translateX(20px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' }
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' }
        },
        slideDown: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' }
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' }
        },
        scaleUp: {
          '0%': { transform: 'scale(1)', opacity: '0' },
          '100%': { transform: 'scale(1.05)', opacity: '1' }
        },
        
        // Continuous Keyframes
        'pulse-glow': {
          '0%, 100%': { boxShadow: '0 0 20px rgba(249, 115, 22, 0.4)' },
          '50%': { boxShadow: '0 0 30px rgba(249, 115, 22, 0.6)' }
        },
        'pulse-glow-accent': {
          '0%, 100%': { boxShadow: '0 0 20px rgba(59, 130, 246, 0.4)' },
          '50%': { boxShadow: '0 0 30px rgba(59, 130, 246, 0.6)' }
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' }
        },
        'rotate-slow': {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' }
        },
        'spin-slow': {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' }
        },
        'bounce-subtle': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-5px)' }
        },
        
        // Interactive Keyframes
        wiggle: {
          '0%, 7%, 14%, 21%': { transform: 'translateX(0)' },
          '3.5%, 10.5%, 17.5%': { transform: 'translateX(-2px)' },
          '7%, 14%, 21%': { transform: 'translateX(2px)' }
        },
        shake: {
          '10%, 90%': { transform: 'translate3d(-1px, 0, 0)' },
          '20%, 80%': { transform: 'translate3d(2px, 0, 0)' },
          '30%, 50%, 70%': { transform: 'translate3d(-4px, 0, 0)' },
          '40%, 60%': { transform: 'translate3d(4px, 0, 0)' }
        },
        'ping-soft': {
          '75%, 100%': { transform: 'scale(1.1)', opacity: '0' }
        },
        
        // Loading Keyframes
        'loading-dots': {
          '0%, 80%, 100%': { transform: 'scale(0)', opacity: '0.5' },
          '40%': { transform: 'scale(1)', opacity: '1' }
        },
        'loading-bars': {
          '0%, 40%, 100%': { transform: 'scaleY(0.4)' },
          '20%': { transform: 'scaleY(1.0)' }
        },
        shimmer: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' }
        },
        
        // Background Keyframes
        'gradient-x': {
          '0%, 100%': { transform: 'translateX(0%)' },
          '50%': { transform: 'translateX(100%)' }
        },
        'gradient-y': {
          '0%, 100%': { transform: 'translateY(0%)' },
          '50%': { transform: 'translateY(100%)' }
        },
        'gradient-xy': {
          '0%, 100%': { transform: 'translate(0%, 0%)' },
          '25%': { transform: 'translate(100%, 0%)' },
          '50%': { transform: 'translate(100%, 100%)' },
          '75%': { transform: 'translate(0%, 100%)' }
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', 'monospace'],
        tech: ['Orbitron', 'monospace'],
        display: ['Inter', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        '2xs': ['0.625rem', { lineHeight: '0.75rem' }],
        'xs': ['0.75rem', { lineHeight: '1rem' }],
        'sm': ['0.875rem', { lineHeight: '1.25rem' }],
        'base': ['1rem', { lineHeight: '1.5rem' }],
        'lg': ['1.125rem', { lineHeight: '1.75rem' }],
        'xl': ['1.25rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem', { lineHeight: '2rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
        '5xl': ['3rem', { lineHeight: '1.2' }],
        '6xl': ['3.75rem', { lineHeight: '1.1' }],
        '7xl': ['4.5rem', { lineHeight: '1.1' }],
        '8xl': ['6rem', { lineHeight: '1' }],
        '9xl': ['8rem', { lineHeight: '1' }],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
        '144': '36rem',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'gradient-premium': 'linear-gradient(135deg, #f97316 0%, #ef4444 50%, #ec4899 100%)',
        'gradient-cyber': 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #06b6d4 100%)',
        'gradient-glass': 'linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%)',
        'noise': "url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZGVmcz48ZmlsdGVyIGlkPSJub2lzZSI+PGZlVHVyYnVsZW5jZSB0eXBlPSJmcmFjdGFsTm9pc2UiIGJhc2VGcmVxdWVuY3k9IjAuOSIgbnVtT2N0YXZlcz0iNCIgc3RpdGNoVGlsZXM9InN0aXRjaCIvPjwvZmlsdGVyPjwvZGVmcz48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWx0ZXI9InVybCgjbm9pc2UpIiBvcGFjaXR5PSIwLjEiLz48L3N2Zz4=')",
      },
      backdropBlur: {
        xs: '2px',
        '4xl': '72px',
      },
      backdropBrightness: {
        25: '.25',
        175: '1.75',
      },
      boxShadow: {
        // Premium Shadows
        'premium': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        'premium-lg': '0 35px 60px -12px rgba(0, 0, 0, 0.35)',
        
        // Glow Effects
        'glow': '0 0 20px rgba(249, 115, 22, 0.4)',
        'glow-sm': '0 0 10px rgba(249, 115, 22, 0.3)',
        'glow-md': '0 0 20px rgba(249, 115, 22, 0.4)',
        'glow-lg': '0 0 30px rgba(249, 115, 22, 0.5)',
        'glow-xl': '0 0 40px rgba(249, 115, 22, 0.6)',
        
        // Accent Glows
        'glow-accent': '0 0 20px rgba(59, 130, 246, 0.4)',
        'glow-accent-lg': '0 0 30px rgba(59, 130, 246, 0.5)',
        
        // Inner Effects
        'inner-glow': 'inset 0 0 20px rgba(249, 115, 22, 0.1)',
        'inner-glow-accent': 'inset 0 0 20px rgba(59, 130, 246, 0.1)',
        
        // Colored Shadows
        'shadow-orange': '0 10px 25px -3px rgba(249, 115, 22, 0.3)',
        'shadow-blue': '0 10px 25px -3px rgba(59, 130, 246, 0.3)',
        'shadow-purple': '0 10px 25px -3px rgba(139, 92, 246, 0.3)',
        
        // Glass Morphism
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
        'glass-lg': '0 15px 35px 0 rgba(31, 38, 135, 0.2)',
      },
      dropShadow: {
        'glow': '0 0 20px rgba(249, 115, 22, 0.4)',
        'glow-accent': '0 0 20px rgba(59, 130, 246, 0.4)',
      },
      blur: {
        '4xl': '72px',
      }
    }
  },
  plugins: [require('@tailwindcss/typography')]
}
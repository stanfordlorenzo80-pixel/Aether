import type { Config } from 'tailwindcss';

export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        aether: {
          bg: '#0A0A0C',
          'surface-0': '#111115',
          'surface-1': '#18181D',
          'surface-2': '#1F1F26',
          border: '#2A2A35',
          'border-active': '#3D3D4D',
          'border-focus': 'rgba(124, 107, 255, 0.4)',
          'text-primary': '#F0F0F5',
          'text-secondary': '#8E8EA0',
          'text-tertiary': '#5C5C6E',
          accent: '#7C6BFF',
          'accent-hover': '#8D7EFF',
          'accent-glow': 'rgba(124, 107, 255, 0.2)',
          'accent-subtle': 'rgba(124, 107, 255, 0.08)',
          teal: '#3ECFCF',
          'teal-glow': 'rgba(62, 207, 207, 0.2)',
          coral: '#FF8B5E',
          'coral-glow': 'rgba(255, 139, 94, 0.2)',
          success: '#34D399',
          error: '#F87171',
          warning: '#FBBF24',
        },
      },
      fontFamily: {
        sans: [
          'Inter',
          '-apple-system',
          'BlinkMacSystemFont',
          'Segoe UI',
          'Roboto',
          'sans-serif',
        ],
        mono: [
          'JetBrains Mono',
          'Fira Code',
          'Cascadia Code',
          'Consolas',
          'monospace',
        ],
      },
      fontSize: {
        '2xs': ['0.625rem', { lineHeight: '0.875rem' }],  // 10px
        xs: ['0.6875rem', { lineHeight: '1rem' }],         // 11px
        sm: ['0.8125rem', { lineHeight: '1.25rem' }],      // 13px
        base: ['0.9375rem', { lineHeight: '1.5rem' }],     // 15px
        lg: ['1.0625rem', { lineHeight: '1.75rem' }],      // 17px
        xl: ['1.25rem', { lineHeight: '1.75rem' }],        // 20px
        '2xl': ['1.5rem', { lineHeight: '2rem' }],         // 24px
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],    // 30px
      },
      letterSpacing: {
        tighter: '-0.03em',
        tight: '-0.02em',
      },
      borderRadius: {
        DEFAULT: '0.5rem',
        lg: '0.75rem',
        xl: '1rem',
        '2xl': '1.25rem',
      },
      boxShadow: {
        glow: '0 0 20px rgba(124, 107, 255, 0.15)',
        'glow-sm': '0 0 10px rgba(124, 107, 255, 0.1)',
        'glow-lg': '0 0 40px rgba(124, 107, 255, 0.2)',
        'glow-teal': '0 0 20px rgba(62, 207, 207, 0.15)',
        'surface-1': '0 1px 3px rgba(0, 0, 0, 0.3), 0 1px 2px rgba(0, 0, 0, 0.2)',
        'surface-2': '0 4px 6px rgba(0, 0, 0, 0.3), 0 2px 4px rgba(0, 0, 0, 0.2)',
        'surface-3': '0 10px 15px rgba(0, 0, 0, 0.3), 0 4px 6px rgba(0, 0, 0, 0.2)',
      },
      animation: {
        'fade-in': 'fadeIn 300ms ease-out',
        'fade-out': 'fadeOut 200ms ease-in',
        'slide-up': 'slideUp 300ms ease-out',
        'slide-down': 'slideDown 200ms ease-in',
        'slide-in-left': 'slideInLeft 250ms ease-out',
        'scale-in': 'scaleIn 200ms ease-out',
        shimmer: 'shimmer 2s infinite linear',
        pulse: 'pulse 2s infinite ease-in-out',
        breathe: 'breathe 4s infinite ease-in-out',
        spin: 'spin 1s infinite linear',
        'glow-pulse': 'glowPulse 2s infinite ease-in-out',
        'cursor-blink': 'cursorBlink 1s infinite step-end',
      },
      keyframes: {
        fadeIn: {
          from: { opacity: '0', transform: 'translateY(8px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
        fadeOut: {
          from: { opacity: '1', transform: 'translateY(0)' },
          to: { opacity: '0', transform: 'translateY(8px)' },
        },
        slideUp: {
          from: { opacity: '0', transform: 'translateY(16px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
        slideDown: {
          from: { opacity: '1', transform: 'translateY(0)' },
          to: { opacity: '0', transform: 'translateY(16px)' },
        },
        slideInLeft: {
          from: { opacity: '0', transform: 'translateX(-16px)' },
          to: { opacity: '1', transform: 'translateX(0)' },
        },
        scaleIn: {
          from: { opacity: '0', transform: 'scale(0.95)' },
          to: { opacity: '1', transform: 'scale(1)' },
        },
        shimmer: {
          from: { backgroundPosition: '-200% 0' },
          to: { backgroundPosition: '200% 0' },
        },
        pulse: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.7' },
        },
        breathe: {
          '0%, 100%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.02)' },
        },
        glowPulse: {
          '0%, 100%': { boxShadow: '0 0 10px rgba(124, 107, 255, 0.1)' },
          '50%': { boxShadow: '0 0 25px rgba(124, 107, 255, 0.3)' },
        },
        cursorBlink: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0' },
        },
      },
      backdropBlur: {
        xs: '2px',
      },
      transitionDuration: {
        '150': '150ms',
        '200': '200ms',
        '250': '250ms',
        '300': '300ms',
      },
    },
  },
  plugins: [],
} satisfies Config;

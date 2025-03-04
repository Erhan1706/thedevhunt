/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/templates/**/*.html"],
  theme: {
    extend: {
      fontFamily: {
        gothic: ["Century Gothic", "sans-serif"],
        kanit: ["Kanit-Bold", "sans-serif"],
      },
      fontSize: {
        xxs: ['0.625rem', '0.625rem']
      },
      animation: {
        'pop': 'animate-pop 0.5s cubic-bezier(.26, .53, .74, 1.48) forwards',
      },
      keyframes: {
        'animate-pop': {
          '0%': {
            opacity: '0',
            transform: 'scale(0.3, 0.3)',
          },
          '100%': {
            opacity: '1',
            transform: 'scale(1, 1)',
          },
        },
      }
    },
  },
  plugins: [require("@tailwindcss/typography")],
};

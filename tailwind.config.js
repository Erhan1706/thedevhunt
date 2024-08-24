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
    },
  },
  plugins: [require("@tailwindcss/typography")],
};

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/templates/**/*.html"],
  theme: {
    extend: {
      fontFamily: {
        gothic: ["Century Gothic", "sans-serif"],
        kanit: ["Kanit-Bold", "sans-serif"],
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};

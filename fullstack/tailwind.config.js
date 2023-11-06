/** @type {import('tailwindcss').Config} */

module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/js/*.js",
    "./static/node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin'),
    require('@tailwindcss/aspect-ratio'),
    require('@tailwindcss/forms'),
  ],
}

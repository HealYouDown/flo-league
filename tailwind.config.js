module.exports = {
  mode: "jit",
  purge: {
    content: [
      "./app/templates/**/*.html",
    ],
  },
  darkMode: true,
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

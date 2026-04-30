/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html",           // ← الـ HTML في الـ root
        "./src/JS/**/*.js",       // ← الـ JS files
        "./src/pages/**/*.html"], // ← الـ HTML files في الصفحات
  theme: {
    extend: {},
  },
  plugins: [],
}


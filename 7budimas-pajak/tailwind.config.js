/** @type {import('tailwindcss').Config} */
export default {
  prefix: "tw-",
  content: ["./public/index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      keyframes: {
        xSlide: {
          "0%": { left: "-80%" },
          "100%": { left: "150%" },
        },
      },
      animation: {
        xSlide: "xSlide 1.5s ease-in-out infinite",
      },
      colors: {
        primary: "#01579B",
        background: "#EDF0F2"
      },
    },
  },
  plugins: [],
};

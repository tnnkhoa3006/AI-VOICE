import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}"
  ],
  theme: {
    extend: {
      colors: {
        ink: "#171717",
        paper: "#f7f3ea",
        panel: "#fffaf0",
        line: "#ded6c9",
        moss: "#24594c",
        coral: "#c8563f",
        brass: "#b9852e"
      },
      boxShadow: {
        panel: "0 14px 40px rgba(23, 23, 23, 0.08)"
      }
    }
  },
  plugins: []
};

export default config;


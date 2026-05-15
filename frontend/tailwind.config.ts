import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["var(--font-inter)", "system-ui", "sans-serif"],
      },
      colors: {
        positive: { DEFAULT: "#10b981", soft: "#d1fae5" },
        neutral: { DEFAULT: "#6b7280", soft: "#e5e7eb" },
        negative: { DEFAULT: "#ef4444", soft: "#fee2e2" },
      },
    },
  },
  plugins: [],
};

export default config;

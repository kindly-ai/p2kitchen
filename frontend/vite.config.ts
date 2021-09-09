/* eslint-disable import/no-extraneous-dependencies */
import reactRefresh from "@vitejs/plugin-react-refresh";
import { defineConfig } from "vite";
import reactSvgPlugin from "vite-plugin-react-svg";


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [reactRefresh(), reactSvgPlugin()],
  define: {
    __DEV__: process.env.NODE_ENV !== 'prodution'
  }
});

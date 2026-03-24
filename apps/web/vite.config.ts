import { defineConfig } from 'vite';
import preact from '@preact/preset-vite';
import UnoCSS from 'unocss/vite';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [
		UnoCSS({
			configFile: './uno.config.ts',
		}),
		preact(),
	],
	resolve: {
		alias: {
			'@': path.resolve(__dirname, './src'),
			'@comps': path.resolve(__dirname, './src/components'),
			'@types': path.resolve(__dirname, './src/types'),
			'@hooks': path.resolve(__dirname, './src/hooks'),
			'@assets': path.resolve(__dirname, './src/assets'),
			'@images': path.resolve(__dirname, './src/assets/images'),
		}
	}
});

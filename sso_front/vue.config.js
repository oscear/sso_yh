// import config from "./public/config"

module.exports = {

	devServer: {
		open: false,
		proxy: {
			'/bi': {
				target: "http://192.168.0.187:8094/",
				changeOrigin: true,
				// pathRewrite: { '^/api': 'http://localhost:8066/' }
			}
		}
	}
}
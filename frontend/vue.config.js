const { defineConfig } = require('@vue/cli-service')
module.exports = {
  devServer: {
    allowedHosts: [
      '.localhost'
    ],
    proxy: {
      '^/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        ws: true
      },
    },
  }
}

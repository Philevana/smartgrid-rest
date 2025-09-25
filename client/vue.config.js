const { defineConfig } = require('@vue/cli-service')
const path = require('path')

module.exports = defineConfig({
  transpileDependencies: true,
  
  publicPath: './', // 相对路径，适合各种部署环境
  
  // 输出目录
  outputDir: 'dist',
  
  // 静态资源目录
  assetsDir: 'static',
  
  devServer: {
    port: 5001,
    host: '0.0.0.0',
    allowedHosts: 'all',
    open: true,
    hot: true, // 热更新
    
    proxy: {
      [process.env.VUE_APP_API_PREFIX || '/api']: {
        target: process.env.VUE_APP_API_BASE?.replace(/\/api$/, '') || 'https://www.hideosonn.online',
        changeOrigin: true,
        secure: true,
        ws: true,
        pathRewrite: {
          [`^${process.env.VUE_APP_API_PREFIX || '/api'}`]: process.env.VUE_APP_API_BASE?.includes('/api') 
            ? '/elen90061/api' 
            : '/api'
        },
        logLevel: 'debug'
      }
    },
    
    // 客户端配置
    client: {
      overlay: {
        warnings: false,
        errors: true
      }
    }
  },

  publicPath: './',
  
  lintOnSave: process.env.NODE_ENV === 'development',
  
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src')
      }
    }
  },
  
  chainWebpack: config => {
    // 修改html标题
    config.plugin('html').tap(args => {
      args[0].title = 'client'
      return args
    })
  }
})

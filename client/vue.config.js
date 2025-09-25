const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: ['marked'],

  outputDir: 'demo/dist',
  assetsDir: 'demo/static',  // 静态资源目录，这会影响js/css等文件的存放路径
  
  devServer: {
    port: 5001,  // 设置端口为5001
    host: '0.0.0.0',  // 允许外部访问
    
    // 解决WebSocket安全问题
    client: {
      webSocketURL: {
        protocol: 'wss',  // 使用安全的WebSocket
        hostname: 'www.hideosonn.online',
        port: 443,
        pathname: '/ws'
      }
    },
    
    // 解决Invalid Host header问题
    allowedHosts: [
      'www.hideosonn.online',
      'hideosonn.online',
      '.hideosonn.online',  // 匹配所有子域名
      'localhost',
      '127.0.0.1',
      '159.75.77.100'  // 你的服务器IP
    ],
    
    // 热重载配置
    hot: true,
    liveReload: true,
    
    // 代理配置
    proxy: {
      '/api': {
        target: 'http://localhost:5000',  // Flask后端
        changeOrigin: true,
        ws: true,  // 启用WebSocket代理
        secure: false
      }
    }
  }
})

// const { defineConfig } = require('@vue/cli-service')
// const path = require('path')

// module.exports = defineConfig({
//   transpileDependencies: true,
  
//   publicPath: './', // 相对路径，适合各种部署环境
  
//   // 输出目录
//   outputDir: 'dist',
  
//   // 静态资源目录
//   assetsDir: 'static',
  
//   devServer: {
//     port: 5001,
//     host: '0.0.0.0',
//     allowedHosts: 'all',
//     // open: true,
//     hot: true, // 热更新

//     client: {
//       webSocketURL: {
//         hostname: 'www.hideosonn.online',
//         protocol: 'wss',  // 使用安全的WebSocket
//         port: 443
//       }
//     },
    
//     proxy: {
//       '/api': {
//         target: 'http://localhost:5000',
//         changeOrigin: true,
//         ws: true,
//         secure: false,
//         pathRewrite: {
//           '^/api': ''
//         },
//         onProxyReq: (proxyReq, req, res) => {
//           console.log('Proxying:', req.method, req.url)
//         }
//       },
//       '/ws': {  // 如果有单独的WebSocket路径
//         target: 'http://159.75.77.100:5001',
//         changeOrigin: true,
//         ws: true,
//         secure: false
//       }
//     },
    
//     // 客户端配置
//     client: {
//       overlay: {
//         warnings: false,
//         errors: true
//       }
//     }
//   },
  
//   lintOnSave: process.env.NODE_ENV === 'development',
  
//   configureWebpack: {
//     resolve: {
//       alias: {
//         '@': path.resolve(__dirname, 'src')
//       }
//     }
//   },
  
//   chainWebpack: config => {
//     // 修改html标题
//     config.plugin('html').tap(args => {
//       args[0].title = 'client'
//       return args
//     })
//   }
// })

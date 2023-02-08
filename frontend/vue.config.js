const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  devServer: { //This is neccessary to publish to 8080 port for pods service
    host: '127.0.0.1',
    port: 8080
  },
  transpileDependencies: [
    'vuetify'
  ],
  lintOnSave: false,
  publicPath: '/',    //local development
  // publicPath: '/ICICLE', //deployment.
  configureWebpack:{
    resolve:{
      fallback:{
        "https": require.resolve("https-browserify"),
        "http": require.resolve("stream-http"),
        "url": require.resolve("url/")
      }
    }
  }
  
})


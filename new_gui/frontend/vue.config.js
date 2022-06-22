const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: [
    'vuetify'
  ],
  lintOnSave: false,
  publicPath: '/',    //local development
  // publicPath: '/ICICLE' //deployment.
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


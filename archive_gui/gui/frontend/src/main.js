// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import 'element-ui/lib/theme-chalk/index.css'
// import BootstrapVue from "bootstrap-vue";
import ElementUI from 'element-ui'
import locale from 'element-ui/lib/locale/lang/en'
import {store} from './store/store'
import './assets/css/main.css';
import  "tabulator-tables/dist/css/tabulator_modern.min.css"


// require('./')
// require('./css/neo4jd3.css')
require('./css/neo4jd3.css')
Vue.config.productionTip = false
// Vue.use(BootstrapVue);
Vue.use(ElementUI, {locale})
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
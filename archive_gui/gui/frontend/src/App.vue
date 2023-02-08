<template>
  <div id="app">
    <el-row :style="{'height': HEIGHT, 'width': WIDTH}" >
      <el-col :span="10" class="classComponent"><filter-table/></el-col>
      <el-col :span="14" class="classComponent"><kg/></el-col>
    </el-row>
  </div>
</template>

<script>
import Kg from './components/Kg.vue'
import FilterTable from './components/FilterTable.vue'
export default {
  name: 'App',
  components:{
    Kg,
    FilterTable
  },
  created(){

  },
  computed:{
    HEIGHT(){
      return window.innerHeight+"px"
    },
    WIDTH(){
      return window.innerWidth+"px"
    }
  }
}

</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>

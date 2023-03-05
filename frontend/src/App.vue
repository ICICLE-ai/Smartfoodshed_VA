<template>
  <div>
    <v-app>
      <NavBar />
      <v-main>
        <dataset/>
        <!-- <transition name="slide-fade" mode="out-in">
          <keep-alive>
            <router-view />
          </keep-alive>
        </transition> -->
      </v-main>
    </v-app>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar";
import Dataset from '@/views/Dashboard.vue'
export default {
  data() {
    return {};
  },
  components: {
    NavBar,Dataset
  },
};
</script>

<style>
/* .svg-canvas{
    position: absolute; 
    width: 100%; 
    height: 100%;
    z-index: -1;
  } */
</style>

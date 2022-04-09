<template>
  <div>
    <v-app>
      <NavBar />
      <v-main>
        <transition name="slide-fade" mode="out-in">
          <router-view />
        </transition>
      </v-main>
    </v-app>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar";
export default {
  data() {
    return {};
  },
  components: {
    NavBar,
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

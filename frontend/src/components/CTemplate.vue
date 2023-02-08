<template>
  <div>
    <v-hover v-slot="{ hover }">
      <v-card
        :elevation="hover ? 12 : 5"
        class="card-tabular"
        :draggable="draggable"
        @dragstart="dragStart"
        outlined
        :id="componentId"
        ref="cardComp"
        @contextmenu="rightClickMenuShow"
        :style="{
          top: marginTop + 'px',
          left: marginLeft + 'px',
          width: `${width}px`,
          height: `${height}px`,
          position: 'absolute',
        }"
      > 
        <slot name="core">
            <v-card-text class="card-name">
                Empty Container
            </v-card-text>      
        </slot> 

        <div class="resizer resizer-r" @mousedown="mouseDownHandler"></div>
        <div class="resizer resizer-b" @mousedown="mouseDownHandler"></div>
      </v-card>
    </v-hover>
    <!-- <v-menu
      v-model="showRightClickMenu"
      :position-x="rightMenuX"
      :position-y="rightMenuY"
      absolute
      offset-y
    >
      <RightClickMenu
        :vue="this"
        :container="container"
        :itemProps="itemProps"
        store="documents"
      />
    </v-menu> -->
  </div>
</template>

<script>
import { mapState } from "vuex";
// import RightClickMenu from "@/components/RightClickMenu";
// import InoutputBtns from "@/components/InoutputBtns";
export default {
  data() {
    return {
      dataStatus: false,
      resizeX: undefined,
      resizeY: undefined,
      // draggable: true,
      width: 500,
      height: 1000,
      resizeWidth: 0, //
      resizeHeight: 0,
      marginTop: 0,
      marginLeft: 0,
      topMargin: window.innerHeight / 2,
      leftMargin: window.innerWidth / 2,
      resizingStatus: false,

    //   showRightClickMenu: false,
      rightMenuX: 0,
      rightMenuY: 0,
      loadingStatus: undefined,
      componentId: "tabular-0",
      // for right click menu
      items: [{ title: "Remove node" }],

      container: ".documents-components-list",

      selected: [],
     
      sheets: [], 
      
      currentDataBase: [],
      answerBasedRetrieval: {},
      flag: false,
      tableItemKey: "",
      //-----
      search: "",
      calories: '', 
      desserts: [],
      headers: [],
      
      selected_rows:[],
      singleSelect: false,
      sheetNames: [],
      tab: null,
      sheetItemKey: null, 
      currentSheet: null, 
      currentData: null,
    };
  },
  methods: {
    dragStart(e) {
      const el = document.querySelector(`#${e.target.id}`);
      const initialLeft = parseInt(el.style.left.split("px")[0]) - e.clientX;
      const initialTop = parseInt(el.style.top.split("px")[0]) - e.clientY;
      e.dataTransfer.setData("item-id", e.target.id);
      e.dataTransfer.setData("initialLeft", initialLeft);
      e.dataTransfer.setData("initialTop", initialTop);
      this.$store.dispatch("changeCurrentDraggingVM", this);
    },

    mouseDownHandler(e) {
      // this.$store.dispatch('changeResizerStatus', true);
      this.resizeX = e.clientX;
      this.resizeY = e.clientY;
      document.addEventListener("mousemove", this.mouseMoveHandler);
      document.addEventListener("mouseup", this.mouseUpHandler);
      this.resizingStatus = true;
    },

    mouseMoveHandler(e) {
      const dx = e.clientX - this.resizeX;
      const dy = e.clientY - this.resizeY;
      this.width = this.resizeWidth + dx;
      this.height = this.resizeHeight + dy;
    },

    mouseUpHandler(e) {
      this.resizeWidth = this.width;
      this.resizeHeight = this.height;
      document.removeEventListener("mousemove", this.mouseMoveHandler);
      document.removeEventListener("mouseup", this.mouseUpHandler);
      // this.$store.dispatch('changeResizerStatus', false)
      this.resizingStatus = false;
    },

    rightClickMenuShow(e) {
      e.preventDefault();
      this.showRightClickMenu = true;
      this.rightMenuX = e.clientX;
      this.rightMenuY = e.clientY;
    },
 
  },

  created() {
    // Initialize initial position
    this.marginTop = 50;
    this.marginLeft = 100;
    this.resizeWidth = this.width;
    this.resizeHeight = this.height;
  },

  computed: {
    // Determine Whether the component is draggable
    // Not allowed when resizing and drawling link
    draggable() {
      return !(this.resizingStatus);
    },
  },

  components: {
  },

  watch: {
      height(newVal) {
          this.$store.dispatch('containerSizeChange', {'container': 'tableContainer', 'height': this.height})
      }, 
  },
};
</script>

<style scoped>
.card-name {
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  height: 100%;
}


.resizer {
  position: absolute;
}

.resizer-r {
  cursor: col-resize;
  height: 100%;
  right: -1%;
  top: 0;
  width: 5px;
}

/* Placed at the bottom side */
.resizer-b {
  bottom: -1%;
  cursor: row-resize;
  height: 5px;
  left: 0;
  width: 100%;
}

</style>                                                                   
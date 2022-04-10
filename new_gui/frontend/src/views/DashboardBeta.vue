<template>
  <div
    class="dashboard-beta-container"
    @dragover="dragOver"
    @drop="dropHandler"
  >
    <menu-bar/>
    <!-- <c-table-viewer/> -->
    <!-- <c-template/> -->
    <TemplateTable/>
  </div>
</template>

<script>
import MenuBar from '@/components/MenuBar.vue'
import CTableViewer from '@/components/CTableViewer.vue'
import CTemplate from '@/components/CTemplate.vue'
import TemplateTable from '@/components/tableview/TemplateTable.vue'
import { mapState } from 'vuex';
export default {
    components: {
        MenuBar,
        CTableViewer,
        CTemplate,
        TemplateTable
    },
    methods: {
      dragOver(e){
        e.preventDefault();
        return false;
        // console.log(e)
      },
      dropHandler(e){
        console.log(1)
        const currentX = e.clientX;
        const currentY = e.clientY; 
        if(!e.dataTransfer.getData('item-id')){
          return false; 
        }
        const initialLeft = e.dataTransfer.getData('initialLeft');
        const initialTop = e.dataTransfer.getData('initialTop');
        const id = e.dataTransfer.getData('item-id'); //
        const el = document.querySelector(`#${id}`);
        // this.updatePos(currentX-initialX, currentY-initialY, el);
        el.style.left = (currentX + parseInt(initialLeft)) + 'px';
        el.style.top = (currentY + parseInt(initialTop)) + 'px';
        console.log(this.currentDragging)
        if(this.currentDragging){
          console.log(this.currentDragging)
          this.currentDragging.marginLeft = el.style.left;
          this.currentDragging.marginTop = el.style.top;
        }
        e.preventDefault();
        return false;
      }, 
    }, 
    computed: {
      ...mapState(['currentDragging']),
    }

}
  
</script>

<style>
.dashboard-beta-container{
  height: 100%;
  width: 100%;
}
 
</style>
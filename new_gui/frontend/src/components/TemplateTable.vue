<template>
  <CTemplate>
        <template v-slot:core>
            <TableViewerCore/>
        </template>
  </CTemplate>
</template>

<script>
import CTemplate from '@/components/CTemplate.vue'
import TableViewerCore from '@/components/TableViewerCore.vue'
export default {
    data(){
        return {
            containerId: 'tableContainer',
        }
    }, 
    components: {
        // template comp
        CTemplate,
        // core comp
        TableViewerCore
    },
}
</script>

<style>

</style>
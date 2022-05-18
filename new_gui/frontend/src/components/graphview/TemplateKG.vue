<template>
    <c-template>
        <template v-slot:core>
            <KgViewerCore/>
        </template>
    </c-template>
</template>

<script>
import CTemplate from '@/components/CTemplate.vue'
import KgViewerCore from './KgViewerCore.vue'
export default {
    components: {
        CTemplate, 
        KgViewerCore, 
    }
}
</script>

<style>

</style>
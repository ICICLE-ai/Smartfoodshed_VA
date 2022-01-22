<template>
    <div class="fullHeight">
        <div id="div_graph" class="fullHeight" :style="{'height': HEIGHT}"></div>
    </div>
</template>

<script>
import * as Neo4jd3 from '../js/Neo4D3'
export default{
    components:{

    },
    data(){
        return {
            // graphData:{}
        }
    },
    created(){
        this.$store.dispatch('getGraphData')
    },
    methods:{
        test(){
            console.log(Neo4jd3)
        },
        drawNeo4jd3(){
            console.log(this.graphData)
            var that = this
            var neo4jd3 = Neo4jd3.default('#div_graph', {
                neo4jData: that.graphData,
                nodeRadius: 30,
                infoPanel: false,
                
                onNodeDoubleClick: function(node){
                    that.dbclick(node)
                },
                onNodeMouseEnter: function(node){
                    that.hover_node = node
                },
                onNodeClick: function(node){
                    if(node['status']=="unclicked"){
                        node['status'] = 'clicked'
                        that.clicked_nodes_list.push(node)
                    }else{
                        that.removeFromArray(node, that.clicked_nodes_list)
                        node['status'] = 'unclicked'
                    }
                    
                    that.clicked_one_node = node
                    var all_nodes = d3.selectAll('#div_graph .node .outline')
                    // var all_nodes_stroke = d3.selectAll('#div_graph .node .ring')
                    all_nodes.style('fill', function(d){
                        if(that.clicked_nodes_list.includes(d)){
                            return '#ebab7b'
                        }else{
                            return '#78b3d0'
                        }
                    })
                    all_nodes.style('stroke',function(d){
                        if(that.clicked_nodes_list.includes(d)){
                            return '#e28743'
                        }else{
                            return '#358eb8'
                        }
                    })
                }
            });

        },
    },
    watch:{
        graphData(){
            this.graphData['results'][0]['data'][0]['graph']['nodes'].forEach(function(d){
            // this.graphData['nodes'].forEach(function(d){
                d['status']='unclicked'
            })
            this.drawNeo4jd3()
        }
    },
    mounted(){

    },
    computed:{
        graphData(){
            return this.$store.state.graphData
        },
        HEIGHT(){
            return window.innerHeight+"px"
        },
    }
}
</script>
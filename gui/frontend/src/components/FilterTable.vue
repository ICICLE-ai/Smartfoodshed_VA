<template>
    <div>

        <div ref="tabulator">
            <el-input
            v-model="search"
            size="mini"
            placeholder="search"/>
        
            <el-table :data = dados max-height="800">
                <el-table-column v-for="column in options" 
                :key="column.value"
                :prop="column.value"
                sortable
                :label="column.label"
                >
                </el-table-column>
            </el-table>
        </div>
    </div>
</template>

<script>

export default{
    data(){
        return{
            dados:[],
            
            options: [
                {   'label': 'Origin',
                    'value':'Origin County',
                    'type': 'string'
                },{
                    'label': 'Destination',
                    'value':'Destination County',
                    'type': 'string'
                },
                {
                    'label': 'Weight',
                    'value': 'Weight',
                    'type': 'number'
                },{
                    'label': "Value",
                    'value': "Value",
                    "type": 'number'
                }
            ],
            search:''
        }
    },
    created(){
        // this.test()
        this.$store.dispatch('getTableData')
        
    },
    methods:{   
       
    },
    watch:{
        
        tableData(){
            this.dados = this.tableData['data']
            console.log(this.dados)
        },
        search(){
      
            var that =this
            if(this.search==""){

                this.dados = this.tableData['data']
            }else{
                this.dados = this.dados.filter(d=>{
                    return d['Origin County'].toLowerCase().includes(that.search.toLowerCase())
                })
            }
            
        }
    },
    mounted(){
    
    },
    computed:{
        tableData(){
            return this.$store.state.tableData
        }
    }
}
</script>
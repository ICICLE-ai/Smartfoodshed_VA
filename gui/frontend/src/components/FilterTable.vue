/* eslint-disable indent */
<template>
    <div>
        <el-row>
            <el-col :span="6">
                <el-select v-model="selected_sheet" placeholder="Please Select" size="mini">
                    <el-option
                    v-for="item in sheetNames"
                    :key="item"
                    :label="item"
                    :value="item">
                    </el-option>
                </el-select>
            </el-col>
            <el-col :span="10">
                <el-input
                v-model="search"
                size="mini"
                placeholder="search"/>
            </el-col>
            <el-col :span="2">
                <el-button size="mini" @click="GraphFiltering">Query</el-button>
            </el-col>
        </el-row>

        <div>
            <el-table :data="dados" max-height="800" @select-all="handleSelectionChange" @select="handleSelectionChange" ref="multipleTable" lazy>
                <el-table-column
                    type="selection"
                    width="55">
                </el-table-column>
                <el-table-column v-for="column in options"
                    :key="column.value"
                    :prop="column.value"
                    sortable
                    :label="column.label"
                    show-overflow-tooltip>
                </el-table-column>
            </el-table>
        </div>
    </div>
</template>

<script>
import {mapState} from 'vuex'
export default{
  data () {
    return {
      sheetNames: [], // selector options
      selected_sheet: null, // selector selected
      selected_rows: null,
      dados: [], // table data
      options: [ // table info
      ],
      search: '', // table filter
      stringCols: null, // search function apply to which cols
      oldsheet: ''
    }
  },
  created () {
    this.$store.dispatch('getTableData')
  },
  methods: {
    GraphFiltering () {
      this.$refs.multipleTable.toggleRowSelection(this.dados[0], true)
      console.log(this.selected_rows)
    },
    handleSelectionChange (val) {
      // once change, we save the changes to the global
      console.log('checking here')
      console.log(val)
      console.log(this.selected_sheet)
      //   let tableSelection_copy = this.tableSelection
      //   tableSelection_copy[this.selected_sheet] = val

      this.$store.dispatch('setTableSelected', {sheetName: this.selected_sheet, value: val})

    //   this.selected_rows = val
    },
    getStringCol () {
      let temp = []
      this.options.forEach(d => {
        if (d['type'] == 'str') {
          temp.push(d['value'])
        }
      })
      this.stringCols = temp
    }
  },
  watch: {
    tableData () {
      console.log(this.tableData)
      this.sheetNames = this.tableData['sheet']
      this.selected_sheet = this.sheetNames[0]
      this.options = this.tableData['data'][this.selected_sheet]['tableInfo']
      this.dados = this.tableData['data'][this.selected_sheet]['tableData']
      this.getStringCol()
      // console.log(this.options, this.dados)
    },
    search () {
      var that = this
      if (this.search == '') {
        this.dados = this.tableData['data'][this.selected_sheet]['tableData']
      } else {
        this.dados = this.dados.filter(d => {
          let flag = false
          that.stringCols.forEach(col => {
            if (d[col].toLowerCase().includes(that.search.toLowerCase())) {
              flag = true
            }
          })
          return flag
        })
      }
    },
    selected_sheet () {
      this.options = this.tableData['data'][this.selected_sheet]['tableInfo']
      this.dados = this.tableData['data'][this.selected_sheet]['tableData']
      this.getStringCol()
    },
    dados () {
    //   var that = this
    //   // check whether you already selected something before
    //   // console.log(this.tableSelection[this.selected_sheet])
    //   let pre_selected = this.tableSelection[this.selected_sheet]
    //   if (pre_selected.length > 0) {
    //     pre_selected.forEach(p => {
    //       console.log(p)
    //       that.$refs.multipleTable.toggleRowSelection(p, true)
    //     })
    //   }
      this.$nextTick().then(() => {
        const selected = this.tableSelected[this.selected_sheet]
        if (selected) {
          selected.forEach(row => {
            console.log('!!!!!!!!!!!!')
            console.log(row)
            let targetId = null
            this.$refs.multipleTable.toggleRowSelection(row, true)
            // for (let i = 0; i < this.dados.length; i++) {
            //   if (this.dados[i].id == row.id) {
            //     targetId = i
            //     break
            //   }
            // }
            // if (targetId) {
            //   alert('found!')
              
            // } else {
            //   alert('not found')
            //   console.log('not found!')
            //   console.log(row)
            // }
          })
        }
      })
    },
    selected_rows () {

    }
  },
  mounted () {

  },
  computed: {
    ...mapState(['tableData', 'tableSelection', 'tableSelected'])
  }
}
</script>

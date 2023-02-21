<template>
  <v-row>
    <v-dialog v-model="dialog" class="dialog" @close="closeClicked">
      <v-card class="card">
        <v-row class="left-pad mt-2 mx-2">
          <div>
            <h2>Customize Columns</h2>
            <small>Drag and Drop Columns to Change Order</small>
          </div>
          <v-spacer />
          <div>
            <v-btn
              @click="addColumn"
              color="primary"
              size="large"
              class="pt-2"
              variant="text"
            >
              <v-icon left>mdi-plus</v-icon>
              Add
            </v-btn>
          </div>
        </v-row>
        <v-row>
          <v-col cols="12" sm="10">
            <v-card-text>
              <draggable
                :list="cols"
                :animation="200"
                ghost-class="ghost-card"
                group="col.id"
                id="col"
              >
                <ColumnCard
                  v-for="col in cols"
                  :key="col.id"
                  :column="col"
                  @deleteColumn="deleteColumn"
                  @updateColumn="updateColumn"
                  :tryError="invalidColumns"
                />
              </draggable>
            </v-card-text>
          </v-col>
        </v-row>
        <h4 class="error-message left-pad" v-if="unableToDeleteCol">
          ** Unable to Delete Non-Empty Column **
        </h4>
        <h4 class="error-message left-pad" v-if="maxColumnsReached">
          ** A Maximum of {{ MAX_COLS }} Columns Are Supported **
        </h4>
        <h4 class="error-message left-pad" v-if="minColumnsReached">
          ** A Minimum of {{ MIN_COLS }} Column is Required **
        </h4>
        <h4 class="error-message left-pad" v-if="invalidColumns">
          ** Ensure Each Column Has a Non-Empty Title **
        </h4>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue-darken-1"
            variant="text"
            @click="this.closeClicked()"
          >
            Close
          </v-btn>
          <v-btn
            color="blue-darken-1"
            variant="text"
            @click="this.saveClicked()"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import ColumnCard from './ColumnCard.vue'
import { VueDraggableNext } from 'vue-draggable-next'
import { ref } from 'vue'

const MAX_COLS = 8
const MIN_COLS = 1
const cols = ref([])

export default {
  components: {
    ColumnCard,
    draggable: VueDraggableNext,
  },
  emits: ['close', 'updateColumns'],
  props: {
    columns: {
      type: Object,
      default: undefined,
    },
    jobsByColumn: {
      type: Object,
      default: undefined,
    },
  },
  data: () => ({
    dialog: true,
    cols,
    unableToDeleteCol: false,
    maxColumnsReached: false,
    minColumnsReached: false,
    MAX_COLS,
    MIN_COLS,
    invalidColumns: false,
  }),
  setup(props) {
    cols.value = []
    props.columns.forEach((col) => {
      cols.value.push(col)
    })
  },
  watch: {
    // eslint-disable-next-line func-names
    dialog: function (val) {
      if (!val) {
        this.closeClicked()
      }
    },
  },
  methods: {
    hideWarnings() {
      this.maxColumnsReached = false
      this.minColumnsReached = false
      this.unableToDeleteCol = false
      this.invalidColumns = false
    },
    deleteColumn(colId) {
      this.hideWarnings()
      if (!this.jobsByColumn[colId] || this.jobsByColumn[colId].length === 0) {
        if (cols.value.length > MIN_COLS) {
          let updatedCols = []
          cols.value.forEach((col) => {
            if (col.id !== colId) {
              updatedCols.push(col)
            }
          })
          cols.value = updatedCols
        } else {
          this.minColumnsReached = true
        }
      } else {
        this.unableToDeleteCol = true
      }
    },
    updateColumn(column) {
      this.hideWarnings()
      let updatedCols = []
      cols.value.forEach((col) => {
        if (col.id !== column.id) {
          updatedCols.push(col)
        } else {
          updatedCols.push(column)
        }
      })
      cols.value = updatedCols
    },
    addColumn() {
      this.hideWarnings()
      if (cols.value.length < MAX_COLS) {
        this.cols.push({ id: -1, column_number: -1, name: '' })
      } else {
        this.maxColumnsReached = true
      }
    },
    saveClicked() {
      this.hideWarnings()
      this.validateColumns()
      if (!this.invalidColumns) {
        let index = 0
        let indexedCols = []
        cols.value.forEach((column) => {
          let col = column
          col.column_number = index++
          indexedCols.push(col)
        })
        indexedCols = indexedCols.sort(
          (a, b) => a.column_number - b.column_number,
        )
        this.$emit('updateColumns', indexedCols)
        this.$emit('close')
      }
    },
    closeClicked() {
      this.$emit('close')
    },
    validateColumns() {
      this.invalidColumns = false
      cols.value.forEach((col) => {
        if (col.name.length === 0) {
          this.invalidColumns = true
        }
      })
    },
  },
}
</script>

<style scoped>
.card {
  padding: 1rem;
}
.error-message {
  color: red;
}
.number-rows {
  padding-top: 25px;
  height: 90px;
  padding-left: 40px;
}
.left-pad {
  padding-left: 10px;
}
.dialog {
  max-width: 700px;
}
</style>

<template>
  <v-row>
    <v-dialog v-model="dialog" persistent>
      <v-card class="card">
        <v-row justify="center">
          <v-col cols="12" sm="4">
            <h3>Customize Columns</h3>
          </v-col>
          <v-col cols="12" sm="4">
            <v-btn @click="addColumn"> Add Column </v-btn>
          </v-col>
        </v-row>
        <v-row justify="center">
          <v-col cols="12" sm="1">
            <v-row v-for="i in cols.length" :key="i" class="number-rows">
              <v-col cols="12" sm="1">
                <h3>{{ i }}</h3>
              </v-col>
            </v-row>
          </v-col>
          <v-col cols="12" sm="8">
            <v-card-text>
              <draggable
                :list="cols"
                :animation="200"
                ghost-class="ghost-card"
                group="column.id"
                id="column"
              >
                <ColumnCard
                  v-for="column in cols"
                  :key="column.id"
                  :column="column"
                  :deleteColumn="deleteColumn"
                  @updateColumn="updateColumn"
                  :tryError="invalidColumns"
                />
              </draggable>
            </v-card-text>
          </v-col>
        </v-row>
        <h4 class="error-message" v-if="unableToDeleteCol">
          ** Unable to Delete Non-Empty Column **
        </h4>
        <h4 class="error-message" v-if="maxColumnsReached">
          ** A Maximum of 8 Columns Are Supported **
        </h4>
        <h4 class="error-message" v-if="invalidColumns">
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
import ColumnCard from "./ColumnCard.vue";
import { VueDraggableNext } from "vue-draggable-next";
import { ref } from "vue";

const MAX_COLS = 8;
const cols = ref([]);
const nextColId = ref(0); // set to max of existing cols + 1

export default {
  components: {
    ColumnCard,
    draggable: VueDraggableNext,
  },
  emits: ["close"],
  props: {
    columns: {
      type: Object,
      default: undefined,
    },
    jobsByColumn: {
      type: Object,
      default: undefined,
    },
    updateColumns: {
      type: Function,
      default: undefined,
    },
  },
  data: () => ({
    dialog: true,
    cols,
    unableToDeleteCol: false,
    maxColumnsReached: false,
    MAX_COLS,
    invalidColumns: false,
  }),
  setup(props) {
    cols.value = [];
    for (var col in props.columns) {
      if (props.columns[col].id >= nextColId.value) {
        nextColId.value = props.columns[col].id + 1;
      }
      cols.value.push(props.columns[col]);
    }
  },
  computed: {
    getColumns() {
      return this.columns;
    },
  },
  methods: {
    hideWarnings() {
      this.maxColumnsReached = false;
      this.unableToDeleteCol = false;
      this.invalidColumns = false;
    },
    deleteColumn(colId) {
      this.hideWarnings();
      if (!this.jobsByColumn[colId] || this.jobsByColumn[colId].length == 0) {
        var updatedCols = [];
        for (var colIndex in cols.value) {
          if (cols.value[colIndex].id != colId) {
            updatedCols.push(cols.value[colIndex]);
          }
        }
        cols.value = updatedCols;
      } else {
        this.unableToDeleteCol = true;
      }
    },
    updateColumn(col) {
      this.hideWarnings();
      var updatedCols = [];
      for (var colIndex in cols.value) {
        if (cols.value[colIndex].id != col.id) {
          updatedCols.push(cols.value[colIndex]);
        } else {
          updatedCols.push(col);
        }
      }
      cols.value = updatedCols;
    },
    addColumn() {
      this.hideWarnings();
      if (cols.value.length < MAX_COLS) {
        this.cols.push({ id: nextColId.value++, name: "", position: -1 });
      } else {
        this.maxColumnsReached = true;
      }
    },
    saveClicked() {
      this.hideWarnings();
      this.validateColumns();
      if (!this.invalidColumns) {
        var index = 0;
        for (var colIndex in cols.value) {
          cols.value[colIndex].columnId = index++;
        }
        this.updateColumns(cols.value);
        this.$emit("close");
      }
    },
    closeClicked() {
      this.$emit("close");
    },
    validateColumns() {
      this.invalidColumns = false;
      for (var colIndex in cols.value) {
        if (cols.value[colIndex].name.length == 0) {
          this.invalidColumns = true;
          return;
        }
      }
    },
  },
};
</script>

<style scoped>
.card {
  padding: 1rem;
}
.error-message {
  color: red;
}

.number-rows {
  padding-top: 30px;
  height: 78px;
  padding-left: 40px;
}
</style>

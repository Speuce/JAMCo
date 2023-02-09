<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent>
      <v-card class="card">
        <v-row>
          <v-col cols="12" sm="4">
            <h3>Customize Columns</h3>
          </v-col>
          <v-col cols="12" sm="4">
            <v-btn @click="addColumn"> Add Column </v-btn>
          </v-col>
        </v-row>
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
            />
          </draggable>
          <h4 class="error-message" v-if="unableToDeleteCol">
            Unable to Delete Non-Empty Column
          </h4>
        </v-card-text>
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

const cols = ref([]);

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
    createOrUpdateColumn: {
      type: Function,
      default: undefined,
    },
  },
  data: () => ({
    dialog: true,
    cols,
    unableToDeleteCol: false,
  }),
  setup(props) {
    for (var col in props.columns) {
      cols.value.push(props.columns[col]);
    }
  },
  computed: {
    getColumns() {
      return this.columns;
    },
  },
  methods: {
    deleteColumn(colId) {
      console.log(this.jobsByColumn);
      if (
        !this.jobsByColumn.get(colId) ||
        this.jobsByColumn[colId].length == 0
      ) {
        var updatedCols = [];
        for (var col in cols) {
          if (col.id != colId) {
            updatedCols.push(col);
          }
        }
        cols.value = updatedCols;
      } else {
        this.unableToDeleteCol = true;
      }
      console.log(colId);
      console.log("delete");
    },
    addColumn() {
      this.cols.push({ id: -1, name: "", position: -1 });
    },
    saveClicked() {
      // iterate through cols.value, assign ordering values

      this.$emit("close", cols.value);
    },
    closeClicked() {
      this.$emit("close");
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
</style>

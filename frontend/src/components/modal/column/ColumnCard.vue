<template>
  <v-card class="col-card">
    <v-row>
      <v-col cols="12" sm="6">
        <v-text-field v-model="columnModel.name"></v-text-field>
      </v-col>
      <v-col cols="12" sm="3">
        <v-btn @click="this.deleteColumn(columnModel.id)">X</v-btn>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
export default {
  emits: ["close"],
  props: {
    column: {
      type: Object,
      default: undefined,
      id: {
        type: Number,
        default: -1,
      },
      name: {
        type: String,
        default: "",
      },
    },
    deleteColumn: {
      type: Function,
      default: undefined,
    },
  },
  data: (props) => ({
    columnModel: { ...props.column },
    selectedColumnId: -1,
  }),
  methods: {},
};
</script>

<style scoped>
.col-card {
  width: auto;
}
</style>

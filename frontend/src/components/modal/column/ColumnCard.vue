<template>
  <v-card class="col-card">
    <v-row>
      <v-col cols="12" sm="8">
        <v-text-field
          v-model="columnModel.name"
          @change="updateColumn"
          label="Column Title"
          :style="{
            color: this.tryError && columnModel.name.length == 0 ? 'red' : '',
          }"
        ></v-text-field>
      </v-col>
      <v-col cols="12" sm="4">
        <v-btn @click="this.deleteColumn(columnModel.id)">X</v-btn>
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
export default {
  emits: ["close", "updateColumn"],
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
    tryError: {
      type: Boolean,
      default: false,
    },
  },
  data: (props) => ({
    columnModel: { ...props.column },
    selectedColumnId: -1,
  }),
  methods: {
    updateColumn(event) {
      console.log(event);
      this.columnModel.title = event.target._value;
      this.$emit("updateColumn", this.columnModel);
    },
  },
};
</script>

<style scoped>
.col-card {
  width: auto;
}
</style>

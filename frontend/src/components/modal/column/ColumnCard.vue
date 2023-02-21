<template>
  <div class="col-card">
    <v-row>
      <v-col cols="12" sm="2">
        <v-btn icon flat disabled>
          <v-icon size="large" color="grey">
            mdi-drag-horizontal-variant
          </v-icon>
        </v-btn>
      </v-col>
      <v-col cols="12" sm="8">
        <v-text-field
          v-model="columnModel.name"
          @change="updateColumn"
          label="Column Title"
          :style="{
            color: this.tryError && columnModel.name.length == 0 ? 'red' : '',
          }"
          variant="outlined"
          maxlength="30"
        />
      </v-col>
      <v-col cols="12" sm="2">
        <v-btn
          @click="this.$emit('deleteColumn', columnModel.id)"
          size="medium"
          flat
          class="button-pad pt-2"
          id="delete-col-btn"
        >
          <v-icon color="red"> mdi-trash-can-outline </v-icon>
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  emits: ['change', 'close', 'updateColumn', 'deleteColumn'],
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
        default: '',
      },
      column_number: {
        type: Number,
        default: -1,
      },
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
      this.columnModel.name = event.target._value
      this.$emit('updateColumn', this.columnModel)
    },
  },
}
</script>

<style scoped>
.col-card {
  width: auto;
}
.button-pad {
  margin-top: 8px;
}
</style>

<template>
  <v-row>
    <v-col cols="12" sm="5">
      <v-text-field
        label="Deadline"
        v-model="deadlineModel.title"
        @change="updateDeadline"
        :style="{
          color: this.tryError && deadlineModel.title.length == 0 ? 'red' : '',
        }"
        maxlength="50"
      />
    </v-col>
    <v-col cols="12" sm="5" class="center-offset">
      <Datepicker
        v-model="deadlineModel.date"
        :enable-time-picker="false"
        @update:model-value="updateDate"
        :style="{
          '--dp-background-color':
            this.tryError && !deadlineModel.date ? '#FEF7F6' : '',
          '--dp-border-color':
            this.tryError && !deadlineModel.date ? 'red' : '',
          '--dp-icon-color': this.tryError && !deadlineModel.date ? 'red' : '',
        }"
      />
    </v-col>
    <v-col cols="12" sm="2" class="center-offset">
      <v-btn
        class="remove-btn"
        @click="this.$emit('deleteDeadline', this.deadline.id)"
        size="x-small"
        icon="mdi-trash-can-outline"
      />
    </v-col>
  </v-row>
</template>

<script>
import Datepicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";

export default {
  components: {
    Datepicker,
  },
  emits: ["updateDeadline"],
  props: {
    deadline: {
      type: Object,
      default: null,
      id: {
        type: Number,
        default: -1,
      },
      title: {
        type: String,
        default: "",
      },
      date: {
        type: String,
        default: "",
      },
    },
    tryError: {
      type: Boolean,
      default: false,
    },
  },
  data: (props) => ({
    deadlineModel: {
      id: props.deadline.id,
      title: props.deadline.title,
      date: props.deadline.date,
    },
  }),
  methods: {
    updateDate(date) {
      this.deadlineModel.date = date;
      this.$emit("updateDeadline", this.deadlineModel);
    },
    updateDeadline(event) {
      this.deadlineModel.title = event.target._value;
      this.$emit("updateDeadline", this.deadlineModel);
    },
  },
};
</script>

<style scoped>
.center-offset {
  padding-top: 20px;
  margin-left: -15px;
}

.remove-btn {
  margin-top: 2px;
}
</style>

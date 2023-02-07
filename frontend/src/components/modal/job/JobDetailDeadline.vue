<template>
  <v-row>
    <v-col cols="12" sm="5">
      <v-text-field
        label="Deadline"
        v-model="deadlineModel.title"
        @change="updateDeadline"
      >
      </v-text-field>
    </v-col>
    <v-col cols="12" sm="5" class="center-offset">
      <Datepicker
        v-model="deadlineModel.date"
        :enable-time-picker="false"
        @update:model-value="updateDate"
      ></Datepicker>
    </v-col>
    <v-col cols="12" sm="1" class="center-offset">
      <v-btn class="remove-btn" @click="this.deleteDeadline(this.deadline.id)"
        ><b>X</b></v-btn
      >
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
    deleteDeadline: {
      type: Function,
      default: undefined,
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
      this.updateDeadline({ event: "dateChange", newDate: date });
    },
    updateDeadline(event) {
      if (event.event == "dateChange") {
        this.deadlineModel.date = event.newDate;
      } else {
        this.deadlineModel.title = event.target._value;
      }
      this.$emit("updateDeadline", this.deadlineModel);
    },
  },
};
</script>

<style scoped>
.center-offset {
  padding-top: 18px;
}

.remove-btn {
  width: 12em;
  padding: 0;
  margin: 0;
}
</style>

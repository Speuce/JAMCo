<template>
  <v-row>
    <v-col cols="12" sm="5">
      <v-text-field label="Deadline" v-model="titleModel"> </v-text-field>
    </v-col>
    <v-col cols="12" sm="5" class="center-offset">
      <Datepicker v-model="dateModel" :enable-time-picker="false"></Datepicker>
    </v-col>
    <v-col cols="12" sm="1" class="center-offset">
      <v-btn class="remove-btn" @click="this.deleteDeadline"><b>X</b></v-btn>
    </v-col>
  </v-row>
</template>

<script>
import Datepicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
import { ref } from "vue";

const dateModel = ref(null);
const titleModel = ref(null);

export default {
  components: {
    Datepicker,
  },
  props: {
    title: {
      type: String,
      default: "",
    },
    date: {
      type: String,
      default: "",
    },
    deleteDeadline: {
      type: Function,
      default: () => {},
    },
  },
  data: () => ({
    dateModel,
    titleModel,
  }),
  setup(props) {
    dateModel.value = { ...props }.date;
    titleModel.value = { ...props }.title;
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

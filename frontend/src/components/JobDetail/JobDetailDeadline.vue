<template>
  <v-row>
    <v-col cols="12" sm="6">
      <v-text-field label="Deadline" class="text-h5" v-model="titleModel">
      </v-text-field>
    </v-col>
    <v-col cols="12" sm="5">
      <Datepicker v-model="dateModel" :enable-time-picker="false"></Datepicker>
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

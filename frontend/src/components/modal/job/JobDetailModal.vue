<!--
  TODO:
  - Make description, cover letter, comments scrollable
  - Limit number of deadlines?
  - Populate Status options correctly
  - Make Add new Deadline button populate correctly
  - Add delete X beside each deadline?
  - Link Modal to 'New Application' button
  - Link Modal to application cards
  - Test All Additions
-->

<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent>
      <template v-slot:activator="{ props }">
        <v-btn color="primary" v-bind="props"> Open Dialog </v-btn>
      </template>
      <v-card>
        <v-card-text>
          <v-row>
            <v-col cols="" sm="7">
              <v-row>
                <v-col cols="12" sm="6">
                  <v-text-field
                    label="Position*"
                    class="text-h5"
                    v-model="prefill.position"
                  ></v-text-field
                ></v-col>

                <v-col cols="12" sm="1"></v-col>

                <v-col cols="12" sm="4">
                  <v-text-field
                    label="Type"
                    v-model="prefill.type"
                  ></v-text-field>
                </v-col>
              </v-row>

              <v-row
                ><v-col cols="12" sm="6">
                  <v-text-field
                    label="Company*"
                    required
                    v-model="prefill.company"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" sm="1"></v-col>

                <v-col cols="12" sm="4">
                  <v-select
                    :items="colList"
                    item-text="name"
                    item-value="id"
                    label="Status*"
                    return-object
                  ></v-select>
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="12" sm="">
                  <v-textarea
                    auto-grow
                    class="text-area-box"
                    label="Description"
                    shaped
                    v-model="prefill.description"
                  ></v-textarea
                ></v-col>
              </v-row>

              <v-row>
                <v-col cols="12" sm="">
                  <v-textarea
                    auto-grow
                    class="text-area-box"
                    label="Cover Letter"
                    shaped
                    v-model="prefill.coverLetter"
                  ></v-textarea
                ></v-col>
              </v-row>

              <v-row>
                <v-col cols="12" sm="">
                  <v-textarea
                    auto-grow
                    class="text-area-box"
                    label="Comments"
                    shaped
                    v-model="prefill.comments"
                  ></v-textarea
                ></v-col>
              </v-row>
            </v-col>

            <v-col cols="8" sm="5">
              <v-row class="pad-deadlines">
                <v-col cols="12" sm="9">
                  <h2>Deadlines</h2>
                </v-col>

                <v-col cols="12" sm="3">
                  <v-btn @click="newDeadline">Add Deadline</v-btn>
                </v-col>
              </v-row>
              <v-col class="scroll-deadlines">
                <v-row v-for="deadline in deadlines" :key="deadline.title">
                  <JobDetailDeadline
                    :id="deadline.title"
                    :title="deadline.title"
                    :date="deadline.date"
                  />
                </v-row>
              </v-col>
            </v-col>
          </v-row>
          <small>* indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue-darken-1" variant="text" @click="dialog = false">
            Close
          </v-btn>
          <v-btn color="blue-darken-1" variant="text" @click="dialog = false">
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import sampleColumns from "../../../../__tests__/test_data/test_column_mapping.json";
import JobDetailDeadline from "../job/JobDetailDeadline.vue";
import { ref } from "vue";

const deadlines = ref([{ title: "testDeadline", date: "02/12/2023" }]);

export default {
  components: {
    JobDetailDeadline,
  },
  props: {
    job: {
      type: Object,
      default: () => {
        return {
          user: -1,
          id: -1,
          company: "",
          date: "",
          type: "",
          columnId: -1,
          position: "",
          description: "",
          coverLetter: "",
          comments: "",
          deadlines: [],
        };
      },
    },
    columns: {
      type: Object,
      default: sampleColumns,
    },
    saveJob: {
      type: Function,
      default: () => {},
    },
  },
  data: () => ({
    dialog: false,
    prefill: {
      id: 10,
      company: "Wework",
      date: "Sep 9",
      type: "Backend",
      columnId: 1,
      position: "Software Engineer",
      comments: "This is a comment",
      description:
        "This is a really long job description that will be scrollable. This is a really long job description that will be scrollable. This is a really long job description that will be scrollable. This is a really long job description that will be scrollable. This is a really long job description that will be scrollable. This is a really long job description that will be scrollable. This is a really long job description that will be scrollable. This is a really long job description that will be scrollable. This is a really long job description that will be scrollable. ",
    },
    colList: sampleColumns,
    deadlines,
  }),
  methods: {
    newDeadline() {
      deadlines.value.push({ title: "", date: "" });
      console.log(deadlines.value);
    },
  },
};
</script>

<style scoped>
.pad-deadlines {
  padding-bottom: 1rem;
  padding-left: 0.5rem;
}
.scroll-deadlines {
  overflow-y: auto;
  overflow-x: hidden;
  height: 60vh;
  padding: 20px;
}
.text-area-box {
  max-height: 15vh;
  overflow-y: auto;
  overflow-x: hidden;
}
</style>

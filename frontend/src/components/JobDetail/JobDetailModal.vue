<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent>
      <template v-slot:activator="{ props }">
        <v-btn color="primary" v-bind="props"> Open Dialog </v-btn>
      </template>
      <v-card>
        <v-card-text>
          <v-row>
            <v-col cols="8" sm="8">
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
                    label="Description"
                    rows="2"
                    row-height="30"
                    shaped
                    no-resize
                    v-model="prefill.description"
                  ></v-textarea
                ></v-col>
              </v-row>

              <v-row>
                <v-col cols="12" sm="">
                  <v-textarea
                    auto-grow
                    label="Cover Letter"
                    rows="2"
                    row-height="30"
                    shaped
                    no-resize
                    v-model="prefill.coverLetter"
                  ></v-textarea
                ></v-col>
              </v-row>
            </v-col>
            <v-col cols="12" sm="4">
              <v-row>
                <v-col cols="12" sm="6">
                  <h2>Deadlines</h2>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-btn>Add Deadline</v-btn>
                </v-col>
              </v-row>
              <v-row></v-row>
              <div v-for="deadline in prefill.deadlines" :key="deadline.title">
                <JobDetailDeadline
                  :title="deadline.title"
                  :date="deadline.date"
                />
              </div>
            </v-col>
          </v-row>
          <v-row> </v-row>
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
import sampleColumns from "../../../__tests__/test_data/test_column_mapping.json";
import JobDetailDeadline from "../JobDetail/JobDetailDeadline.vue";

export default {
  components: {
    JobDetailDeadline,
  },
  props: {
    job: {
      type: Object,
      default: () => {
        return {
          id: 10,
          company: "Wework",
          date: "Sep 9",
          type: "Backend",
          columnId: 1,
          position: "Software Engineer",
        };
      },
    },
    columns: {
      type: Object,
      default: sampleColumns,
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
      description:
        "This is a really long job description that will be scrollable. This is a really long job description that will be scrollable. This is a really long job description that will be scrollable. This is a really long job description that will be scrollable. This is a really long job description that will be scrollable. This is a really long job description that will be scrollable. This is a really long job description that will be scrollable. This is a really long job description that will be scrollable. This is a really long job description that will be scrollable. ",
      deadlines: [{ title: "testDeadline", date: "02/12/2023" }],
    },
    colList: sampleColumns,
  }),
};
</script>

<style scoped></style>

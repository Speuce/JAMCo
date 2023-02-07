<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent>
      <v-card>
        <v-card-text>
          <v-row>
            <v-col cols="" sm="7">
              <v-row>
                <v-col cols="12" sm="6">
                  <v-text-field
                    label="Position*"
                    class="text-h5"
                    v-model="jobData.position"
                  ></v-text-field
                ></v-col>

                <v-col cols="12" sm="1"></v-col>

                <v-col cols="12" sm="4">
                  <v-text-field
                    label="Type"
                    v-model="jobData.type"
                  ></v-text-field>
                </v-col>
              </v-row>

              <v-row
                ><v-col cols="12" sm="6">
                  <v-text-field
                    label="Company*"
                    required
                    v-model="jobData.company"
                  ></v-text-field>
                </v-col>

                <v-col cols="12" sm="1"></v-col>

                <v-col cols="12" sm="4">
                  <v-select
                    :items="getColumns"
                    item-title="name"
                    item-value="id"
                    label="Status*"
                    v-model="selectedColumnId"
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
                    v-model="jobData.description"
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
                    v-model="jobData.coverLetter"
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
                    v-model="jobData.comments"
                  ></v-textarea
                ></v-col>
              </v-row>
            </v-col>

            <v-col cols="8" sm="5">
              <v-row class="pad-deadlines">
                <v-col cols="12" sm="8">
                  <h2>Deadlines</h2>
                </v-col>

                <v-col cols="12" sm="4">
                  <v-btn @click="newDeadline" class="add-deadline"
                    >Add Deadline</v-btn
                  >
                </v-col>
              </v-row>
              <v-col class="scroll-deadlines">
                <v-row v-for="deadline in deadlines" :key="deadline.id">
                  <JobDetailDeadline
                    :deadline="deadline"
                    :deleteDeadline="deleteDeadline"
                    @updateDeadline="handleDeadlineUpdate"
                  />
                </v-row>
              </v-col>
            </v-col>
          </v-row>
          <small>* indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue-darken-1"
            variant="text"
            @click="() => $emit('close')"
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
import JobDetailDeadline from "../job/JobDetailDeadline.vue";
import { ref } from "vue";

const nextDeadlineId = ref(0); // set to max of existing deadlines + 1
const deadlines = ref([]);
const selectedColumnId = ref(-1);

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
      default: () => {},
    },
    createOrUpdateJob: {
      type: Function,
      default: () => {},
    },
  },
  data: (props) => ({
    dialog: true,
    jobData: props.job,
    deadlines,
    nextDeadlineId,
    selectedColumnId,
  }),
  setup(props) {
    deadlines.value = props.job.deadlines ? props.job.deadlines : [];
    selectedColumnId.value = props.job.columnId
      ? props.job.columnId
      : props.columns[0].id;
  },
  computed: {
    getColumns() {
      return this.columns;
    },
  },
  methods: {
    newDeadline() {
      deadlines.value.push({
        id: nextDeadlineId.value++,
        title: "",
        date: "",
      });
    },
    deleteDeadline(id) {
      var updatedDeadlines = [];
      deadlines.value.forEach((deadline) => {
        if (deadline.id != id) updatedDeadlines.push(deadline);
      });
      deadlines.value = updatedDeadlines;
    },
    saveClicked() {
      this.jobData.deadlines = deadlines.value;
      this.jobData.columnId = selectedColumnId.value;
      this.createOrUpdateJob(this.jobData);
      this.$emit("close");
    },
    handleDeadlineUpdate(updatedDeadline) {
      var updatedDeadlines = [];
      deadlines.value.forEach((deadline) => {
        if (deadline.id == updatedDeadline.id) {
          updatedDeadlines.push(updatedDeadline);
        } else {
          updatedDeadlines.push(deadline);
        }
      });
      deadlines.value = updatedDeadlines;
    },
  },
};
</script>

<style scoped>
.pad-deadlines {
  padding-bottom: 1rem;
  padding-left: 0.5rem;
}

.add-deadline {
  min-width: 165px;
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

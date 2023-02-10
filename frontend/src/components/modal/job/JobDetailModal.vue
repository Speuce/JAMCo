<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent>
      <v-card>
        <v-card-text>
          <v-row>
            <v-col class="info-col">
              <v-row>
                <v-col cols="12" sm="6">
                  <v-text-field
                    label="Position*"
                    class="text-h5"
                    v-model="jobData.position"
                    :style="{ color: this.positionErrorIndicator }"
                    maxlength="50"
                  />
                </v-col>

                <v-col cols="12" sm="1" />

                <v-col cols="12" sm="5">
                  <v-text-field
                    label="Type"
                    v-model="jobData.type"
                    maxlength="12"
                  />
                </v-col>
              </v-row>

              <v-row
                ><v-col cols="12" sm="6">
                  <v-text-field
                    label="Company*"
                    required
                    v-model="jobData.company"
                    :style="{ color: this.companyErrorIndicator }"
                    maxlength="50"
                  />
                </v-col>

                <v-col cols="12" sm="1" />

                <v-col cols="12" sm="5">
                  <v-select
                    :items="getColumns"
                    item-title="name"
                    item-value="id"
                    label="Status*"
                    v-model="selectedColumnId"
                  />
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
                    maxlength="10000"
                  />
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="12" sm="">
                  <v-textarea
                    auto-grow
                    class="text-area-box"
                    label="Cover Letter"
                    shaped
                    v-model="jobData.coverLetter"
                    maxlength="10000"
                  />
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="12" sm="">
                  <v-textarea
                    auto-grow
                    class="text-area-box"
                    label="Comments"
                    shaped
                    v-model="jobData.comments"
                    maxlength="10000"
                  />
                </v-col>
              </v-row>
            </v-col>

            <v-col class="deadline-col">
              <v-row class="pad-deadlines">
                <v-col cols="12" sm="6">
                  <h2>Deadlines</h2>
                </v-col>

                <v-col cols="12" sm="6">
                  <v-btn @click="newDeadline" class="add-deadline"
                    >Add Deadline</v-btn
                  >
                </v-col>
              </v-row>
              <v-col class="scroll-deadlines">
                <v-row v-for="deadline in deadlines" :key="deadline.id">
                  <JobDetailDeadline
                    :deadline="deadline"
                    @deleteDeadline="deleteDeadline"
                    @updateDeadline="handleDeadlineUpdate"
                    :tryError="deadlineError"
                  />
                </v-row>
              </v-col>
            </v-col>
          </v-row>
          <small>* indicates required field</small>
          <h4
            v-if="
              this.positionErrorIndicator ||
              this.companyErrorIndicator ||
              this.deadlineError
            "
            class="errorMessage"
          >
            Ensure Required (*) Fields Are Filled
          </h4>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="blue-darken-1"
            variant="text"
            @click="this.closeClicked"
          >
            Close
          </v-btn>
          <v-btn color="blue-darken-1" variant="text" @click="this.saveClicked">
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import JobDetailDeadline from '../job/JobDetailDeadline.vue'
import { ref } from 'vue'

const nextDeadlineId = ref(0) // set to max of existing deadlines + 1
const deadlines = ref([])
const selectedColumnId = ref(-1)

export default {
  components: {
    JobDetailDeadline,
  },
  emits: ['close', 'createOrUpdateJob'],
  props: {
    job: {
      type: Object,
      default: () => {
        return {
          user: -1,
          id: -1,
          company: '',
          type: '',
          columnId: -1,
          position: '',
          description: '',
          coverLetter: '',
          comments: '',
        }
      },
    },
    columns: {
      type: Object,
      default: undefined,
    },
  },
  data: (props) => ({
    dialog: true,
    jobData: props.job,
    deadlines,
    nextDeadlineId,
    selectedColumnId,
    positionErrorIndicator: null,
    companyErrorIndicator: null,
    deadlineError: false,
  }),
  setup(props) {
    deadlines.value = props.job.deadlines ? props.job.deadlines : []
    selectedColumnId.value = props.job.columnId
      ? props.job.columnId
      : props.columns[0].id
  },
  computed: {
    getColumns() {
      return this.columns
    },
  },
  methods: {
    newDeadline() {
      this.deadlineError = false
      deadlines.value.push({
        id: nextDeadlineId.value++,
        title: '',
        date: '',
      })
    },
    deleteDeadline(id) {
      let updatedDeadlines = []
      deadlines.value.forEach((deadline) => {
        if (deadline.id != id) updatedDeadlines.push(deadline)
      })
      deadlines.value = updatedDeadlines
    },
    validateDeadlines() {
      this.deadlineError = false
      deadlines.value.forEach((deadline) => {
        if (
          !deadline.title ||
          !deadline.date ||
          deadline.title.length == 0 ||
          deadline.date.length == 0
        ) {
          this.deadlineError = true
          return
        }
      })
      return
    },
    saveClicked() {
      this.positionErrorIndicator = null
      this.companyErrorIndicator = null

      this.validateDeadlines()

      if (
        !this.deadlineError &&
        this.jobData.position &&
        this.jobData.company &&
        this.jobData.position.length > 0 &&
        this.jobData.company.length > 0
      ) {
        this.positionErrorIndicator = null
        this.companyErrorIndicator = null
        this.deadlineError = false
        this.jobData.deadlines = deadlines.value
        this.jobData.columnId = selectedColumnId.value
        this.$emit('createOrUpdateJob', this.jobData)
        this.$emit('close')
      } else {
        if (!this.jobData.position || this.jobData.position.length == 0) {
          this.positionErrorIndicator = 'red'
        }
        if (!this.jobData.company || this.jobData.company.length == 0) {
          this.companyErrorIndicator = 'red'
        }
      }
    },
    closeClicked() {
      this.positionErrorIndicator = null
      this.companyErrorIndicator = null
      this.$emit('close')
    },
    handleDeadlineUpdate(updatedDeadline) {
      let updatedDeadlines = []
      deadlines.value.forEach((deadline) => {
        if (deadline.id == updatedDeadline.id) {
          updatedDeadlines.push(updatedDeadline)
        } else {
          updatedDeadlines.push(deadline)
        }
      })
      deadlines.value = updatedDeadlines
    },
  },
}
</script>

<style scoped>
.deadline-col {
  min-width: 420px;
}

.info-col {
  min-width: 360px;
}
.errorMessage {
  color: red;
}
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

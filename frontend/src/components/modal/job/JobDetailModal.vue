<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="1300px">
      <v-card id="job-detail-modal-card">
        <v-card-text>
          <v-row>
            <v-col class="info-col" cols="7">
              <v-row>
                <v-col cols="12" sm="6">
                  <v-text-field
                    id="job-title"
                    label="Position*"
                    class="text-h5"
                    v-model="jobData.position_title"
                    :style="{ color: this.positionErrorIndicator }"
                    :readonly="this.deactivated"
                    maxlength="50"
                    variant="outlined"
                  />
                </v-col>

                <v-col cols="12" sm="1" />

                <v-col cols="12" sm="5">
                  <v-text-field
                    id="job-type"
                    label="Type"
                    v-model="jobData.type"
                    :readonly="this.deactivated"
                    maxlength="10"
                    variant="outlined"
                  />
                </v-col>
              </v-row>

              <v-row
                ><v-col cols="12" sm="6">
                  <v-text-field
                    id="job-company"
                    label="Company*"
                    required
                    v-model="jobData.company"
                    :readonly="this.deactivated"
                    :style="{ color: this.companyErrorIndicator }"
                    maxlength="50"
                    variant="outlined"
                  />
                </v-col>

                <v-col cols="12" sm="1" />

                <v-col cols="12" sm="5">
                  <v-select
                    id="job-status"
                    :items="getColumns"
                    :readonly="this.deactivated"
                    item-title="name"
                    item-value="id"
                    label="Status*"
                    v-model="selectedColumnId"
                    variant="outlined"
                  />
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="12" sm="">
                  <v-textarea
                    id="job-description"
                    auto-grow
                    class="text-area-box"
                    label="Description"
                    shaped
                    v-model="jobData.description"
                    :readonly="this.deactivated"
                    maxlength="10000"
                    variant="outlined"
                    rows="3"
                  />
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="12" sm="">
                  <v-textarea
                    id="job-cover-letter"
                    auto-grow
                    class="text-area-box"
                    label="Cover Letter"
                    shaped
                    v-model="jobData.cover_letter"
                    :readonly="this.deactivated"
                    maxlength="10000"
                    variant="outlined"
                    rows="3"
                  />
                </v-col>
              </v-row>

              <v-row v-if="!isNew && !deactivated" class="mt-n8">
                <v-col cols="12" sm="" class="text-right">
                  <v-btn
                    color="blue-darken-1"
                    variant="text"
                    :disabled="reviewRequestButtonDisabled"
                    @click="
                      () => {
                        if (!deactivated) ReviewRequestModalVisible = true
                      }
                    "
                  >
                    Request Review
                  </v-btn>
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="12" sm="">
                  <v-textarea
                    id="job-notes"
                    auto-grow
                    class="text-area-box"
                    label="Notes"
                    shaped
                    v-model="jobData.notes"
                    :readonly="this.deactivated"
                    maxlength="10000"
                    variant="outlined"
                    rows="3"
                  />
                </v-col>
              </v-row>
            </v-col>
            <v-divider vertical class="mt-8 mb-12 mx-2" />
            <v-col class="deadline-col">
              <v-row class="my-2 mx-4">
                <h2 class="mr-2">Deadlines</h2>
                <v-spacer></v-spacer>
                <v-btn
                  v-if="!this.deactivated"
                  id="add-deadline"
                  @click="
                    () => {
                      if (!deactivated) newDeadline()
                    }
                  "
                  color="primary"
                  size="large"
                  class="pt-2"
                  variant="text"
                >
                  <v-icon left>mdi-plus</v-icon>
                  Add
                </v-btn>
              </v-row>
              <v-col class="scroll-deadlines">
                <v-row v-for="deadline in deadlines" :key="deadline.id">
                  <JobDetailDeadline
                    :id="`deadline-${deadline.id}`"
                    :deadline="deadline"
                    :viewingOther="deactivated"
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
          <v-btn
            v-if="!this.deactivated"
            id="job-save-button"
            color="blue-darken-1"
            variant="text"
            @click="
              () => {
                if (!this.deactivated) this.saveClicked()
              }
            "
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
  <div class="page-container flex-grow-1">
    <ReviewRequestModal
      v-if="ReviewRequestModalVisible"
      :job="this.jobData"
      :user="this.user"
      @close="this.ReviewRequestModalVisible = false"
    />
  </div>
</template>

<script>
import JobDetailDeadline from '../job/JobDetailDeadline.vue'
import { ref } from 'vue'
import ReviewRequestModal from './ReviewRequestModal.vue'

const nextDeadlineId = ref(0) // TODO: remove once backend integration complete
const deadlines = ref([])
const selectedColumnId = ref(-1)

export default {
  components: {
    JobDetailDeadline,
    ReviewRequestModal,
  },
  emits: ['close', 'createOrUpdateJob'],
  props: {
    job: {
      type: Object,
      default: () => {
        return {
          id: -1,
          company: '',
          type: '',
          kcolumn_id: -1,
          user_id: -1,
          position_title: '',
          description: '',
          cover_letter: '',
          notes: '',
        }
      },
    },
    columns: {
      type: Object,
      default: undefined,
    },
    user: {
      type: Object,
      default: undefined,
    },
    isNew: {
      type: Boolean,
      default: true,
    },
    viewingOther: {
      type: Boolean,
      default: false,
    },
  },
  data: (props) => ({
    dialog: true,
    jobData: { ...props.job },
    deadlines,
    nextDeadlineId,
    selectedColumnId,
    positionErrorIndicator: null,
    companyErrorIndicator: null,
    deadlineError: false,
    ReviewRequestModalVisible: false,
    activeUser: props.user,
    deactivated: props.viewingOther,
  }),
  setup(props) {
    deadlines.value = props.job.deadlines ? props.job.deadlines : []
    selectedColumnId.value = props.job.kcolumn_id
      ? props.job.kcolumn_id
      : props.columns[0].id
  },
  computed: {
    getColumns() {
      return this.columns
    },

    reviewRequestButtonDisabled() {
      return this.jobData.cover_letter.trim() === ''
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
        if (deadline.id !== id) updatedDeadlines.push(deadline)
      })
      deadlines.value = updatedDeadlines
    },
    validateDeadlines() {
      this.deadlineError = false
      deadlines.value.forEach((deadline) => {
        if (
          !deadline.title ||
          !deadline.date ||
          deadline.title.length === 0 ||
          deadline.date.length === 0
        ) {
          this.deadlineError = true
        }
      })
    },
    sortDeadlines() {
      deadlines.value = deadlines.value.sort((a, b) => {
        return (
          new Date(a.date) - new Date(b.date) || a.title.localeCompare(b.title)
        )
      })
    },
    saveClicked() {
      this.positionErrorIndicator = null
      this.companyErrorIndicator = null

      this.validateDeadlines()

      if (
        !this.deadlineError &&
        this.jobData.position_title &&
        this.jobData.company &&
        this.jobData.position_title.length > 0 &&
        this.jobData.company.length > 0
      ) {
        this.sortDeadlines()
        this.positionErrorIndicator = null
        this.companyErrorIndicator = null
        this.deadlineError = false
        this.jobData.deadlines = deadlines.value
        this.jobData.kcolumn_id = selectedColumnId.value
        this.$emit('createOrUpdateJob', this.jobData)
        this.$emit('close')
      } else {
        if (
          !this.jobData.position_title ||
          this.jobData.position_title.length === 0
        ) {
          this.positionErrorIndicator = 'red'
        }
        if (!this.jobData.company || this.jobData.company.length === 0) {
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
        if (deadline.id === updatedDeadline.id) {
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
.errorMessage {
  color: red;
}
.scroll-deadlines {
  overflow-y: auto;
  overflow-x: hidden;
  height: 60vh;
  padding: 20px;
}
.text-area-box {
  padding-top: 10px;
  overflow-y: auto;
  overflow-x: hidden;
}
</style>

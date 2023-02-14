<template>
  <div>
    <JobDetailModal
      v-if="detailModalVisible"
      @createOrUpdateJob="createOrUpdateJob"
      @close="closeDetailModal"
      :job="this.selectedJob"
      :columns="colList"
    />
    <ColumnOptionModal
      v-if="boardOptionModalVisible"
      @close="closeBoardOptionModal"
      @updateColumns="updateColumns"
      :columns="colList"
      :jobsByColumn="jobsByColumn"
    />
    <AccountSetupModal
      v-if="setupModalVisible"
      @updateUser="updateUserAccount"
      :user="activeUser"
    />
    <div class="header-container">
      <h2 class="internal">Your Applications</h2>
      <div>
        <v-btn class="internal" @click="showDetailModal()"
          >Add New Application</v-btn
        >
        <v-btn class="settings" @click="showBoardOptionModal()">
          Board Options
        </v-btn>
      </div>
    </div>
    <div class="kanban">
      <KanbanBoard
        :columns="colList"
        :jobs="jobsByColumn"
        @showDetailModal="showDetailModal"
      />
    </div>
  </div>
</template>

<script>
import KanbanBoard from '../components/kanban/KanbanBoard.vue'
import sampleColumnMapping from '../../__tests__/test_data/test_column_mapping.json'
import sampleJobs from '../../__tests__/test_data/test_jobs.json'
import JobDetailModal from '../components/modal/job/JobDetailModal.vue'
import ColumnOptionModal from '../components/modal/column/ColumnOptionModal.vue'
import { ref } from 'vue'
import AccountSetupModal from '../components/modal/setup/AccountSetupModal.vue'

const jobsByColumn = ref({})
const colList = ref([])
const nextJobId = ref(0) // TODO: remove when backend integration complete
const isNewJob = ref(false)

export default {
  components: {
    KanbanBoard,
    JobDetailModal,
    ColumnOptionModal,
    AccountSetupModal,
  },
  data() {
    return {
      detailModalVisible: false,
      boardOptionModalVisible: false,
      setupModalVisible: true,
      selectedJob: {},
      nextJobId, // temp nextId which will be replaced by backend
      isNewJob,
      colList,
      jobsByColumn,
      activeUser: {}, // to be populated on login
    }
  },
  setup() {
    var maxId = 0 // TODO: remove when backend interated
    jobsByColumn.value = []
    colList.value = []

    // TODO: get columns from backend instead of sampleColumnMapping
    // Populate colList with KanbanColumns
    sampleColumnMapping.forEach((colMapping) => {
      colList.value.push(colMapping)
    })
    // TODO: Remove since get_columns sorts columns by number already
    colList.value = colList.value.sort((a, b) => a.number - b.number)

    // TODO: populate from backend instead of sampleJobs
    // Populate jobsByColumn, mapping each job to their columnId
    sampleJobs.forEach((job) => {
      // TODO: remove maxId check
      if (job.id > maxId) {
        maxId = job.id
      }
      if (!jobsByColumn.value[job.columnId]) {
        jobsByColumn.value[job.columnId] = []
      }
      jobsByColumn.value[job.columnId].push(job)
    })

    // Order jobs within a column by job.id (initial, default vertical order)
    // Same process as sortColumnJobsById method below (setup can't call methods)
    colList.value.forEach((column) => {
      if (
        jobsByColumn.value[column.id] &&
        jobsByColumn.value[column.id].length > 0
      ) {
        jobsByColumn.value[column.id] = jobsByColumn.value[column.id].sort(
          (a, b) => a.id - b.id,
        )
      }
    })

    nextJobId.value = maxId + 1
  },
  methods: {
    createOrUpdateJob(job) {
      if (isNewJob.value) {
        // TODO: add backend job record
        // retrieve job (with backend-populated id)
        // retrieved job will have Deadline objects with properly populated id fields
        isNewJob.value = false
      } else {
        // Remove job from jobsByColumn
        colList.value.forEach((column) => {
          if (jobsByColumn.value[column.id]) {
            jobsByColumn.value[column.id] = jobsByColumn.value[
              column.id
            ].filter((item) => item.id !== job.id)
          }
        })
      }
      // TODO: post to backend update_job
      // populate jobsByColumn.value[job.id] with reponse job
      jobsByColumn.value[job.columnId].push(job)
    },
    updateColumns(columns) {
      // TODO: post columns to update_columns
      // update colList.value with response

      colList.value = columns

      this.sortColumnJobsById()

      // Initialize any empty columns with empty array
      colList.value.forEach((col) => {
        if (!jobsByColumn.value[col.id]) {
          jobsByColumn.value[col.id] = []
        }
      })
    },
    showDetailModal(job) {
      if (job) {
        // editing job
        this.selectedJob = job
      } else {
        // creating new job
        isNewJob.value = true
        // TODO: set id to -1
        this.selectedJob = { id: nextJobId.value++ }
      }
      this.detailModalVisible = true
    },
    sortColumnJobsById() {
      colList.value.forEach((column) => {
        if (
          jobsByColumn.value[column.id] &&
          jobsByColumn.value[column.id].length > 0
        ) {
          jobsByColumn.value[column.id] = jobsByColumn.value[column.id].sort(
            (a, b) => a.id - b.id,
          )
        }
      })
    },
    updateUserAccount(userData) {
      this.activeUser = userData
      // post to backend update_user
      this.setupModalVisible = false
    },
    closeDetailModal() {
      this.detailModalVisible = false
    },
    closeBoardOptionModal() {
      this.boardOptionModalVisible = false
    },
    showBoardOptionModal() {
      this.boardOptionModalVisible = true
    },
  },
}
</script>

<style scoped>
.kanban {
  overflow-x: auto;
  margin: 0.5rem 0rem;
}
h2 {
  color: rgba(74, 85, 104, var(--text-opacity));
  font-weight: 600;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
    'Helvetica Neue', Arial, 'Noto Sans', sans-serif, 'Apple Color Emoji',
    'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
}

.header-container {
  color: black;
  display: flex;
  margin: 1.5rem 1rem 1.5rem 0;
  justify-content: space-between;
}
.internal {
  margin-right: 2rem;
}
</style>

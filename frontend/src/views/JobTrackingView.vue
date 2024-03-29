<template>
  <div>
    <JobDetailModal
      v-if="detailModalVisible"
      @createOrUpdateJob="createOrUpdateJob"
      @close="closeDetailModal"
      :job="this.selectedJob"
      :user="this.user"
      :columns="colList"
      :isNew="this.isNewJob"
      :viewingOther="this.deactivated"
    />
    <ColumnOptionModal
      v-if="boardOptionModalVisible"
      @close="closeBoardOptionModal"
      @updateColumns="updateColumns"
      :columns="colList"
      :jobsByColumn="jobsByColumn"
    />
    <div class="kanban">
      <KanbanBoard
        :columns="colList"
        :jobs="jobsByColumn"
        :viewingOther="deactivated"
        @showDetailModal="showDetailModal"
        @columnChanged="createOrUpdateJob"
        @showBoardOptionModal="showBoardOptionModal"
      />
    </div>
    <div class="floating">
      <v-btn
        v-if="!this.deactivated"
        id="add-job-button"
        size="x-large"
        icon
        class="internal"
        @click="
          () => {
            if (!deactivated) showDetailModal()
          }
        "
        color="primary"
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </div>
  </div>
</template>

<script>
import KanbanBoard from '../components/kanban/KanbanBoard.vue'
import JobDetailModal from '../components/modal/job/JobDetailModal.vue'
import ColumnOptionModal from '../components/modal/column/ColumnOptionModal.vue'
import { ref } from 'vue'
import { postRequest } from '@/helpers/requests.js'

const jobsByColumn = ref({})
const colList = ref([])
const isNewJob = ref(false)

export default {
  components: {
    KanbanBoard,
    JobDetailModal,
    ColumnOptionModal,
  },
  emits: ['fetchUserData'],
  props: {
    user: {
      type: Object,
      default: undefined,
    },
    viewingOther: {
      type: Boolean,
      default: false,
    },
  },
  data(props) {
    return {
      detailModalVisible: false,
      boardOptionModalVisible: false,
      selectedJob: {},
      isNewJob,
      colList,
      jobsByColumn,
      activeUser: props.user,
      deactivated: props.viewingOther,
    }
  },

  setup() {
    jobsByColumn.value = {}
    colList.value = []
  },

  async mounted() {
    let columnResponse = await postRequest('column/api/get_columns', {
      user_id: this.user.id,
    })

    columnResponse.columns.forEach((colMapping) => {
      colList.value.push(colMapping)
    })

    // Setup Empty Arrays for Jobs foreach Column
    colList.value.forEach((col) => {
      jobsByColumn.value[col.id] = []
    })

    let jobResponse = await postRequest('job/api/get_minimum_jobs', {
      user_id: this.user.id,
    })

    let jobJSON = jobResponse.jobs

    // Populate jobsByColumn, mapping each job to their kcolumn_id
    jobJSON.forEach((job) => {
      let jobWithKColId = { ...job, kcolumn_id: job.kcolumn }
      delete jobWithKColId.kcolumn

      jobsByColumn.value[jobWithKColId.kcolumn_id].push(jobWithKColId)
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
  },

  methods: {
    async createOrUpdateJob(job) {
      if (isNewJob.value) {
        let userJob = job
        userJob.user_id = this.activeUser.id
        await postRequest('job/api/create_job', userJob).then((newJob) => {
          isNewJob.value = false
          // Push New Job To Bottom of Column
          jobsByColumn.value[newJob.job.kcolumn_id].push(newJob.job)
        })
      } else {
        // Remove job from jobsByColumn
        colList.value.forEach((column) => {
          if (jobsByColumn.value[column.id]) {
            jobsByColumn.value[column.id] = jobsByColumn.value[
              column.id
            ].filter((item) => item.id !== job.id)
          }
        })
        await postRequest('job/api/update_job', job).then(() => {
          jobsByColumn.value[job.kcolumn_id].push(job)
          jobsByColumn.value[job.kcolumn_id] = jobsByColumn.value[
            job.kcolumn_id
          ].sort((a, b) => a.id - b.id)
        })
      }
    },
    async updateColumns(columns) {
      await postRequest('column/api/update_columns', {
        user_id: this.activeUser.id,
        payload: columns,
      }).then((updatedColumns) => {
        colList.value = updatedColumns.columns
        this.sortColumnJobsById()

        // Initialize any empty columns with empty array
        colList.value.forEach((col) => {
          if (!jobsByColumn.value[col.id]) {
            jobsByColumn.value[col.id] = []
          }
        })
      })
    },
    async showDetailModal(job) {
      this.$emit('fetchUserData')
      if (job) {
        // editing job
        if (job.deadlines === undefined) {
          // only get from backend if job not populated
          await postRequest('job/api/get_job_by_id', {
            user_id: this.activeUser.id,
            job_id: job.id,
          }).then((completeJob) => {
            jobsByColumn.value[job.kcolumn_id] = jobsByColumn.value[
              job.kcolumn_id
            ].filter((item) => item.id !== job.id)
            jobsByColumn.value[job.kcolumn_id].push(completeJob.job_data)

            jobsByColumn.value[job.kcolumn_id] = jobsByColumn.value[
              job.kcolumn_id
            ].sort((a, b) => a.id - b.id)

            isNewJob.value = false
            this.selectedJob = completeJob.job_data
            this.detailModalVisible = true
          })
        } else {
          this.selectedJob = job
          this.detailModalVisible = true
        }
      } else {
        // creating new job
        isNewJob.value = true
        this.selectedJob = { id: -1 }
        this.detailModalVisible = true
      }
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
  height: 99%;
}
h2 {
  color: rgba(74, 85, 104, var(--text-opacity));
  font-weight: 600;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
    'Helvetica Neue', Arial, 'Noto Sans', sans-serif, 'Apple Color Emoji',
    'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
}

.floating {
  position: fixed;
  bottom: 20px;
  right: 0px;
  z-index: 100;
}
.internal {
  margin-right: 2rem;
}
</style>

<template>
  <div class="page-container">
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

const jobsByColumn = ref({})
const colList = ref([])
const nextJobId = ref(0)
const isNewJob = ref(false)

export default {
  components: {
    KanbanBoard,
    JobDetailModal,
    ColumnOptionModal,
  },
  data() {
    return {
      detailModalVisible: false,
      boardOptionModalVisible: false,
      selectedJob: {},
      nextJobId,
      isNewJob,
      colList,
      jobsByColumn,
    }
  },
  setup() {
    var maxId = 0
    jobsByColumn.value = []
    colList.value = []

    sampleColumnMapping.forEach((colMapping) => {
      colList.value.push(colMapping)
    })
    colList.value = colList.value.sort((a, b) => a.number - b.number)

    sampleJobs.forEach((job) => {
      if (job.id > maxId) {
        maxId = job.id
      }
      if (!jobsByColumn.value[job.columnId]) {
        jobsByColumn.value[job.columnId] = []
      }
      jobsByColumn.value[job.columnId].push(job)
    })

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
        isNewJob.value = false
      } else {
        colList.value.forEach((column) => {
          if (jobsByColumn.value[column.id]) {
            jobsByColumn.value[column.id] = jobsByColumn.value[
              column.id
            ].filter((item) => item.id !== job.id)
          }
        })
      }
      jobsByColumn.value[job.columnId].push(job)

      // Post to database
    },
    updateColumns(columns) {
      colList.value = columns

      colList.value.forEach((column) => {
        if (jobsByColumn.value[column.id]) {
          jobsByColumn.value[column.id] = jobsByColumn.value[column.id].sort(
            (a, b) => a.id - b.id,
          )
        }
      })

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
        this.selectedJob = { id: nextJobId.value++ }
      }
      this.detailModalVisible = true
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
.page-container {
  margin: 1rem 2rem 2rem 2rem;
  min-width: 100vw;
  padding-right: 3.5rem;
  overflow: auto;
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

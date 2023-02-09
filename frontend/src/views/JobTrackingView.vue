<template>
  <div class="page-container">
    <JobDetailModal
      v-if="detailModalVisible"
      @createOrUpdateJob="createOrUpdateJob"
      @close="closeDetailModal"
      :createOrUpdateJob="createOrUpdateJob"
      :job="selectedJob"
      :columns="colList"
    />
    <ColumnOptionModal
      v-if="columnOptionModalVisible"
      @close="closeColumnModal"
      :createOrUpdateColumn="createOrUpdateColumn"
      :columns="colList"
      :jobsByColumn="jobList"
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
        :jobs="jobList"
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

const jobList = ref([])
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
      columnOptionModalVisible: false,
      selectedJob: {},
      nextJobId,
      isNewJob,
      jobList, // switch jobList to jobByColumn (pull up from Kanban)
      colList,
    }
  },
  setup() {
    let maxId = 0
    sampleJobs.forEach((job) => {
      jobList.value.push(job)
      if (job.id > maxId) {
        maxId = job.id
      }
    })
    sampleColumnMapping.forEach((colMapping) => {
      colList.value.push(colMapping)
    })
    nextJobId.value = maxId + 1
  },
  methods: {
    createOrUpdateJob(job) {
      if (isNewJob.value) {
        isNewJob.value = false
        jobList.value.push(job)
      }
      // Post to database
    },
    createOrUpdateColumn(col) {
      console.log(col)
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
    closeColumnModal() {
      this.columnOptionModalVisible = false
    },
    showBoardOptionModal() {
      this.columnOptionModalVisible = true
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

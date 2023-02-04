<template>
  <JobDetailModal />
  <div class="page-container">
    <div class="header-container">
      <h2 class="internal">Your Applications</h2>
      <div>
        <v-btn class="internal">Add New Application</v-btn>
        <v-btn class="settings"> Tracking Settings </v-btn>
      </div>
    </div>
    <div class="kanban">
      <KanbanBoard :columns="columns" :jobs="jobs" />
    </div>
  </div>
</template>

<script>
import KanbanBoard from '../components/kanban/KanbanBoard.vue'
import sampleColumnMapping from '../../__tests__/test_data/test_column_mapping.json'
import sampleJobs from '../../__tests__/test_data/test_jobs.json'
import JobDetailModal from '../components/JobDetail/JobDetailModal.vue'

export default {
  components: {
    KanbanBoard,
    JobDetailModal,
  },
  data() {
    return {
      columns: sampleColumnMapping,
      jobs: sampleJobs,
    }
  },
}
</script>

<style scoped>
.kanban {
  overflow-x: scroll;
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

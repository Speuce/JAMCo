<template>
  <div class="page-container">
    <div class="header-container">
      <h2 class="internal">Your Applications</h2>
      <div>
        <v-btn class="internal">Add New Application</v-btn>
        <v-btn class="settings"> Tracking Settings </v-btn>
      </div>
    </div>
    <KanbanBoard :columns="columns" :jobs="jobs" />
  </div>
</template>

<script>
import KanbanBoard from "../components/kanban/KanbanBoard.vue";
import sampleColumnMapping from "../../__tests__/test_data/test_column_mapping.json";
import sampleJobs from "../../__tests__/test_data/test_jobs.json";

export default {
  components: {
    KanbanBoard,
  },
  data() {
    return {
      columns: sampleColumnMapping,
      jobs: sampleJobs,
    };
  },
};
</script>

<style scoped>
h2 {
  color: rgba(74, 85, 104, var(--text-opacity));
  font-weight: 600;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji",
    "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
}
.page-container {
  padding: 1rem;
}
.header-container {
  display: flex;
  color: black;
  padding: 1rem 2rem 1rem 1rem;
  justify-content: space-between;
}

.internal {
  margin-right: 2rem;
}
</style>

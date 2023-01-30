<!-- Vue2 Kanban Implementation Template: https://codesandbox.io/s/animated-draggable-kanban-board-with-tailwind-and-vue-1ry0p?ref=madewithvuejs.com&file=/src/App.vue-->

<template>
  <div id="app">
    <div class="flex justify-center">
      <div class="min-h-screen flex overflow-x-scroll py-12">
        <div
          v-for="column in columns"
          :key="column.id"
          class="bg-gray-100 rounded-lg px-3 py-3 column-width rounded mr-4"
        >
          <p
            class="text-gray-700 font-semibold font-sans tracking-wide text-sm"
          >
            {{ column.name }}
          </p>
          <draggable
            :list="jobs[column.id]"
            :animation="200"
            ghost-class="ghost-card"
            group="column.id"
            @change="handle($event, column.id)"
            class="min-h-screen"
            id="column"
          >
            <JobCard
              v-for="job in jobs[column.id]"
              :key="job.id"
              :job="job"
              class="mt-3 cursor-move"
            ></JobCard>
          </draggable>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { VueDraggableNext } from "vue-draggable-next";
import JobCard from "./JobCard.vue";
import sampleColumnMapping from "../../../__tests__/test_data/test_column_mapping.json";
import sampleJobs from "../../../__tests__/test_data/test_jobs.json";

export default {
  name: "KanbanBoard",
  components: {
    JobCard,
    draggable: VueDraggableNext,
  },
  data() {
    return {
      columns: sampleColumnMapping,
      jobs: this.processJobsByColumn(sampleJobs),
    };
  },
  methods: {
    handle(event, colId) {
      if (event.added) {
        event.added.element.columnId = colId;
        // Post Update to Job Model, update ColumnId field
      }
    },
    processJobsByColumn(sampleJobs) {
      var jobsByColumn = {};

      for (var job in sampleJobs) {
        if (jobsByColumn[sampleJobs[job].columnId] == null) {
          jobsByColumn[sampleJobs[job].columnId] = [];
        }
        jobsByColumn[sampleJobs[job].columnId].push(sampleJobs[job]);
      }
      return jobsByColumn;
    },
  },
};
</script>

<style scoped>
.column-width {
  min-width: 320px;
  width: 320px;
}
.ghost-card {
  opacity: 0.5;
  background: #f7fafc;
  border: 1px solid #4299e1;
}
</style>

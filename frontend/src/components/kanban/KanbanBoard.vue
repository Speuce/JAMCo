<!-- Vue2 Kanban Implementation Template: https://codesandbox.io/s/animated-draggable-kanban-board-with-tailwind-and-vue-1ry0p?ref=madewithvuejs.com&file=/src/App.vue-->

<template>
  <div id="app">
    <div class="flex justify-center">
      <div class="min-h-screen flex overflow-x-scroll py-12">
        <div
          v-for="column in columns"
          :key="column.title"
          class="bg-gray-100 rounded-lg px-3 py-3 column-width rounded mr-4"
        >
          <p
            class="text-gray-700 font-semibold font-sans tracking-wide text-sm"
          >
            {{ column.title }}
          </p>
          <!-- TODO: Make draggable groups full column height -->
          <draggable
            :list="column.jobs"
            :animation="200"
            ghost-class="ghost-card"
            group="jobs"
          >
            <JobCard
              v-for="job in column.jobs"
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
import sampleData from "./sample_data.json";

export default {
  name: "KanbanBoard",
  components: {
    JobCard,
    draggable: VueDraggableNext,
  },
  data() {
    const columns = sampleData;
    return {
      columns: columns,
    };
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

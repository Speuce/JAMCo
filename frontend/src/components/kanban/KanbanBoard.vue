<!-- Vue2 Kanban Implementation Template: https://codesandbox.io/s/animated-draggable-kanban-board-with-tailwind-and-vue-1ry0p?ref=madewithvuejs.com&file=/src/App.vue-->

<template>
  <div class="page">
    <div class="board-container">
      <div class="min-h-screen column-container">
        <div
          v-for="column in getColumns"
          :key="column.id"
          class="column-width column"
        >
          <p class="column-title">
            {{ column.name }}
          </p>
          <draggable
            :list="this.getJobsByColumn[column.id]"
            :animation="200"
            ghost-class="ghost-card"
            group="column.id"
            @change="handle($event, column.id)"
            class="min-h-screen"
            id="column"
          >
            <JobCard
              v-for="job in this.getJobsByColumn[column.id]"
              :key="job.id"
              :job="job"
              class="job-card"
              @click="this.showDetailModal(job)"
            ></JobCard>
          </draggable>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { VueDraggableNext } from 'vue-draggable-next'
import JobCard from './JobCard.vue'

export default {
  name: 'KanbanBoard',
  components: {
    JobCard,
    draggable: VueDraggableNext,
  },
  props: {
    columns: {
      type: Object,
      default: null,
    },
    jobs: {
      type: Object,
      default: null,
    },
    showDetailModal: {
      type: Function,
      default: undefined,
    },
  },
  computed: {
    getJobsByColumn() {
      return this.processJobsByColumn(this.jobs)
    },
    getColumns() {
      return this.columns
    },
  },
  methods: {
    handle(event, colId) {
      if (event.added) {
        event.added.element.columnId = colId
        // Post Update to Job Model, update ColumnId field
      }
    },
    processJobsByColumn() {
      var jobsByColumn = {}

      for (var col in this.columns) {
        if (jobsByColumn[this.columns[col].id] == null) {
          jobsByColumn[this.columns[col].id] = []
        }
      }

      for (var job in this.jobs) {
        jobsByColumn[this.jobs[job].columnId].push(this.jobs[job])
      }

      for (col in this.columns) {
        jobsByColumn[this.columns[col].id] = jobsByColumn[
          this.columns[col].id
        ].sort((a, b) => {
          a.id > b.id ? 1 : -1
        })
      }

      return jobsByColumn
    },
  },
}
</script>

<style scoped>
.page {
  display: inline-block;
}
.board-container {
  display: flex;
  justify-content: center;
}

.min-h-screen {
  min-height: 80vh;
}

.column-container {
  display: flex;
}

.column {
  --bg-opacity: 1;
  background-color: #f7fafc;
  background-color: rgba(220, 220, 220, var(--bg-opacity));
  border-radius: 0.25rem;
  padding: 0.75rem;
  margin-right: 1rem;
}

.column-title {
  --text-opacity: 1;
  color: #4a5568;
  color: rgba(74, 85, 104, var(--text-opacity));
  font-weight: 600;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
    'Helvetica Neue', Arial, 'Noto Sans', sans-serif, 'Apple Color Emoji',
    'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
  letter-spacing: 0.025em;
  font-size: 0.875rem;
}

.job-card {
  margin-top: 0.75rem;
  cursor: move;
}
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

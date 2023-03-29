<!-- Vue2 Kanban Implementation Template: https://codesandbox.io/s/animated-draggable-kanban-board-with-tailwind-and-vue-1ry0p?ref=madewithvuejs.com&file=/src/App.vue-->

<template>
  <div class="page">
    <div class="board-container">
      <div class="min-h-screen column-container px-4">
        <div
          v-for="column in this.columns"
          :key="column.id"
          class="column-width column"
        >
          <v-hover v-slot="{ isHovering, props }">
            <div class="column-header" v-bind="props">
              <div class="d-flex justify-between align-center">
                <p class="column-title">
                  {{ column.name }}
                </p>
                <v-btn
                  v-if="!this.deactivated"
                  @click="
                    () => {
                      if (!deactivated) this.$emit('showBoardOptionModal')
                    }
                  "
                  color="greytext"
                  icon="mdi-pencil"
                  variant="text"
                  size="small"
                  :style="{ opacity: isHovering ? 1 : 0 }"
                />
              </div>
            </div>
          </v-hover>
          <draggable
            :list="this.jobs[column.id]"
            :animation="200"
            :disabled="this.deactivated"
            ghost-class="ghost-card"
            group="column.id"
            @change="handle($event, column.id)"
            class="min-h-screen"
            id="column"
          >
            <JobCard
              v-for="job in this.jobs[column.id]"
              :key="job.id"
              :job="job"
              class="job-card"
              @click="this.$emit('showDetailModal', job)"
            />
          </draggable>
        </div>
        <v-btn
          v-if="!this.deactivated"
          @click="
            () => {
              if (!deactivated) this.$emit('showBoardOptionModal')
            }
          "
          color="greytext"
          icon="mdi-plus"
          variant="text"
          size="small"
          class="ml-n2"
        />
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
  emits: ['showDetailModal', 'columnChanged', 'showBoardOptionModal'],
  props: {
    columns: {
      type: Object,
      default: null,
    },
    jobs: {
      type: Object,
      default: null,
    },
    viewingOther: {
      type: Boolean,
      default: false,
    },
  },
  data(props) {
    return { deactivated: props.viewingOther }
  },
  methods: {
    handle(event, colId) {
      if (event.added) {
        let updatedJob = event.added.element
        // eslint-disable-next-line no-param-reassign
        updatedJob.kcolumn_id = colId
        this.$emit('columnChanged', updatedJob)
      }
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
  padding: 5px 15px 10px 15px;
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

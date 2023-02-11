import { mount } from '@vue/test-utils'
import { VueDraggableNext } from 'vue-draggable-next'
import KanbanBoard from '../src/components/kanban/KanbanBoard.vue'
import JobCard from '../src/components/kanban/JobCard.vue'
import { expect, beforeEach, describe, it } from 'vitest'
import testColumnMapping from './test_data/test_column_mapping.json'
import testJobs from './test_data/test_jobs.json'

describe('KanbanBoard', () => {
  let wrapper

  beforeEach(async () => {
    wrapper = mount(KanbanBoard, {
      props: {
        jobs: getJobsByColumn(),
        columns: testColumnMapping,
      },
    })
  })

  // Processing in JobTrackingView
  function getJobsByColumn() {
    let jobsByColumn = []

    testJobs.forEach((job) => {
      if (!jobsByColumn[job.columnId]) {
        jobsByColumn[job.columnId] = []
      }
      jobsByColumn[job.columnId].push(job)
    })

    testColumnMapping.forEach((column) => {
      if (jobsByColumn[column.id].length > 0) {
        jobsByColumn[column.id] = jobsByColumn[column.id].sort(
          (a, b) => a.id - b.id
        )
      }
    })
    return jobsByColumn
  }

  it('has the correct number of columns', () => {
    let columns = wrapper.findAllComponents(VueDraggableNext)
    expect(columns.length).toBe(Object.keys(testColumnMapping).length)
  })

  it('updates the column of a job when it is moved', () => {
    let column = wrapper.findAllComponents(VueDraggableNext)
    let job = wrapper.findComponent(JobCard)

    expect(job.vm.job.columnId).toBe(12)

    column[4].vm.$emit('change', { added: { element: job.vm.job } }, 8)
    expect(job.vm.job.columnId).toBe(8)
  })

  it('emits showDetailModal when card clicked', () => {
    let card = wrapper.findComponent(JobCard)
    card.trigger('click')
    expect(wrapper.emitted('showDetailModal')).toBeTruthy()
  })
})

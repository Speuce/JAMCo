import { mount } from '@vue/test-utils'
import { VueDraggableNext } from 'vue-draggable-next'
import KanbanBoard from '../src/components/kanban/KanbanBoard.vue'
import JobCard from '../src/components/kanban/JobCard.vue'
import { expect, beforeEach, describe, it, vi } from 'vitest'
import testColumnMapping from './test_data/test_column_mapping.json'
import testJobs from './test_data/test_jobs.json'

describe('KanbanBoard', () => {
  let wrapper
  let showDetailModal = vi.fn()

  beforeEach(async () => {
    wrapper = mount(KanbanBoard, {
      props: {
        jobs: testJobs,
        columns: testColumnMapping,
        showDetailModal,
      },
    })
  })

  it('has the correct number of columns', () => {
    let columns = wrapper.findAllComponents(VueDraggableNext)
    expect(columns.length).toBe(Object.keys(testColumnMapping).length)
  })

  it('updates the column of a job when it is moved', () => {
    let column = wrapper.findAllComponents(VueDraggableNext)
    let job = wrapper.findComponent(JobCard)
    expect(job.vm.job.columnId).toBe(1)

    column[1].vm.$emit('change', { added: { element: job.vm.job } }, 2)
    expect(job.vm.job.columnId).toBe(2)
  })

  it('emits showDetailModal when card clicked', () => {
    let card = wrapper.findComponent(JobCard)
    card.trigger('click')
    expect(wrapper.emitted('showDetailModal')).toBeTruthy()
  })
})

import { mount } from '@vue/test-utils'
import { VueDraggableNext } from 'vue-draggable-next'
import KanbanBoard from '../src/components/kanban/KanbanBoard.vue'
import JobCard from '../src/components/kanban/JobCard.vue'
import { expect, beforeEach, describe, it } from 'vitest'
import testColumnMapping from './test_data/test_column_mapping.json'
import testJobsByColumn from './test_data/test_jobs_by_column.json'

describe('KanbanBoard', () => {
  let wrapper

  beforeEach(async () => {
    wrapper = mount(KanbanBoard, {
      props: {
        jobs: testJobsByColumn,
        columns: testColumnMapping,
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

    expect(job.vm.job.kcolumn_id).toBe(12)

    column[4].vm.$emit('change', { added: { element: job.vm.job } }, 8)
    expect(job.vm.job.kcolumn_id).toBe(8)
  })

  it('emits showDetailModal when card clicked', () => {
    let card = wrapper.findComponent(JobCard)
    card.trigger('click')
    expect(wrapper.emitted('showDetailModal')).toBeTruthy()
  })
})

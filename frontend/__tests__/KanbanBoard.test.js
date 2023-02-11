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
})

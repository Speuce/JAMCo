import { mount } from '@vue/test-utils'
import JobTrackingView from '../src/views/JobTrackingView.vue'
import { expect, beforeEach, describe, it } from 'vitest'
import testJobs from './test_data/test_jobs.json'
import testCols from './test_data/test_column_mapping.json'
import JobCard from '../src/components/kanban/JobCard.vue'

describe('JobTrackingView', () => {
  let wrapper

  beforeEach(async () => {
    wrapper = mount(JobTrackingView, {})
  })

  it('renders the correct number of jobs', () => {
    expect(wrapper.findAllComponents(JobCard).length).toBe(testJobs.length)
  })

  it('opens JobDetailModal when card clicked', () => {
    expect(wrapper.vm.detailModalVisible).toBe(false)
    wrapper.findComponent(JobCard).trigger('click')
    expect(wrapper.vm.detailModalVisible).toBe(true)
  })

  it('assigns selectedJob when card clicked', () => {
    expect(wrapper.vm.selectedJob).toEqual({})
    let job = wrapper.findComponent(JobCard)
    job.trigger('click')
    expect(wrapper.vm.selectedJob).toEqual(job.vm.job)
  })

  it('opens JobDetailModal when New Job clicked', () => {
    expect(wrapper.vm.selectedJob).toEqual({})
    expect(wrapper.vm.detailModalVisible).toBe(false)
    let buttons = wrapper.findAllComponents({ name: 'v-btn' })
    buttons.forEach((button) => {
      if (button.text() === 'Add New Application') {
        button.trigger('click')
      }
    })
    // interacted with via modal
    wrapper.vm.createOrUpdateJob({ ...testJobs[0] })

    expect(wrapper.vm.selectedJob).toEqual({ id: 633 })
    expect(wrapper.vm.detailModalVisible).toBe(true)
  })

  it('closes the detail modal when the close event is emitted', async () => {
    expect(wrapper.vm.detailModalVisible).toBe(false)
    wrapper.vm.showDetailModal()
    expect(wrapper.vm.detailModalVisible).toBe(true)
    wrapper.vm.closeDetailModal()
    expect(wrapper.vm.detailModalVisible).toBe(false)
  })

  it('opens ColumnOptionModal when Board Options clicked', () => {
    expect(wrapper.vm.boardOptionModalVisible).toBe(false)
    let buttons = wrapper.findAllComponents({ name: 'v-btn' })
    buttons.forEach((button) => {
      if (button.text() === 'Board Options') {
        button.trigger('click')
      }
    })
    expect(wrapper.vm.boardOptionModalVisible).toBe(true)
  })

  it('closes the board option modal when the close event is emitted', async () => {
    expect(wrapper.vm.boardOptionModalVisible).toBe(false)
    wrapper.vm.showBoardOptionModal()
    expect(wrapper.vm.boardOptionModalVisible).toBe(true)
    wrapper.vm.closeBoardOptionModal()
    expect(wrapper.vm.boardOptionModalVisible).toBe(false)
  })

  it('updates colList when param passed to updateColumns', () => {
    expect(wrapper.vm.colList).toEqual(
      testCols.sort((col1, col2) => col1.column_number - col2.column_number),
    )
    wrapper.vm.updateColumns([{ id: 8 }, { id: 0 }])
    expect(wrapper.vm.colList).toEqual([{ id: 8 }, { id: 0 }])
  })

  it('updates jobsByColumn when job edited', () => {
    wrapper.vm.isNewJob = false
    wrapper.vm.createOrUpdateJob({ id: 0, kcolumn_id: 8 })
    expect(wrapper.vm.jobsByColumn[8]).toEqual([
      {
        id: 12,
        company: 'Minisoft',
        type: 'Frontend',
        position: 'Senior Software Engineer',
        kcolumn_id: 8,
        deadlines: [],
        cover_letter: 'Test',
        description: 'Description',
        notes: 'Test',
      },
      { id: 0, kcolumn_id: 8 },
    ])
  })
})

import { mount } from '@vue/test-utils'
import JobTrackingView from '../src/views/JobTrackingView.vue'
import { expect, beforeEach, describe, it } from 'vitest'
import testJobs from './test_data/test_jobs.json'
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
        return
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
    wrapper.vm.closeDetailModal()
    expect(wrapper.vm.detailModalVisible).toBe(false)
  })

  it('opens ColumnOptionModal Board Options clicked', () => {
    expect(wrapper.vm.columnOptionModal).toBe(false)
    let buttons = wrapper.findAllComponents({ name: 'v-btn' })
    buttons.forEach((button) => {
      if (button.text() === 'Board Options') {
        button.trigger('click')
        return
      }
    })
    expect(wrapper.vm.detailModalVisible).toBe(true)
  })
})

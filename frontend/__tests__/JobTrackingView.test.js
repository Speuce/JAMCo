import { mount } from '@vue/test-utils'
import JobTrackingView from '../src/views/JobTrackingView.vue'
import { expect, beforeEach, describe, it, vi, afterEach } from 'vitest'
import testJobs from './test_data/test_jobs.json'
import testCols from './test_data/test_column_mapping.json'
import { postRequest } from '@/helpers/requests.js'
vi.mock('@/helpers/requests.js', () => ({
  postRequest: vi.fn(),
}))

const mostPostRequest = (url) => {
  if (url === 'account/api/get_columns') {
    return Promise.resolve({ columns: testCols })
  }
  if (url === 'job/api/get_minimum_jobs') {
    return Promise.resolve({ jobs: testJobs })
  }
  if (url === 'job/api/create_job') {
    return Promise.resolve({ job: testJobs[0] })
  }
  if (url === 'job/api/update_job') {
    return Promise.resolve({ data: { id: 633 } })
  }
  if (url === 'account/api/update_columns') {
    return Promise.resolve({ columns: [{ id: 8 }, { id: 2 }, { id: 1 }] })
  }
  if (url === 'job/api/get_job_by_id') {
    return Promise.resolve({ job_data: testJobs[1] })
  }
  return Promise.resolve({ data: {} })
}

describe('JobTrackingView', () => {
  let wrapper
  let mockuser = {
    id: 1,
  }

  beforeEach(() => {
    postRequest.mockImplementation(mostPostRequest)
    wrapper = mount(JobTrackingView, {
      props: {
        user: mockuser,
      },
    })
  })

  afterEach(() => {
    vi.resetAllMocks()
  })

  // it('opens JobDetailModal when New Job clicked', () => {
  //   expect(wrapper.vm.selectedJob).toEqual({})
  //   expect(wrapper.vm.detailModalVisible).toBe(false)

  //   // interacted with via modal
  //   wrapper.vm.createOrUpdateJob({ ...testJobs[0] })

  //   expect(wrapper.vm.selectedJob).toEqual({ id: 633 })
  //   expect(wrapper.vm.detailModalVisible).toBe(true)
  // })

  // it('sorts jobs into jobsByColumn', () => {
  //   // ensure there are the correct number of columns
  //   expect(Object.keys(wrapper.vm.jobsByColumn).length).toBe(5)

  //   // ensure each column has the correct  number of jobs
  //   expect(wrapper.vm.jobsByColumn[1].length).toBe(4)
  //   expect(wrapper.vm.jobsByColumn[2].length).toBe(3)
  //   expect(wrapper.vm.jobsByColumn[7].length).toBe(4)
  //   expect(wrapper.vm.jobsByColumn[8].length).toBe(1)
  //   expect(wrapper.vm.jobsByColumn[12].length).toBe(2)

  //   // ensure each column has the correct jobs
  //   expect(wrapper.vm.jobsByColumn[1]).toEqual([
  //     testJobs[0],
  //     testJobs[1],
  //     testJobs[2],
  //     testJobs[3],
  //   ])
  //   expect(wrapper.vm.jobsByColumn[2]).toEqual([
  //     testJobs[4],
  //     testJobs[5],
  //     testJobs[6],
  //   ])
  //   expect(wrapper.vm.jobsByColumn[7]).toEqual([
  //     testJobs[7],
  //     testJobs[8],
  //     testJobs[9],
  //     testJobs[10],
  //   ])
  //   expect(wrapper.vm.jobsByColumn[8]).toEqual([testJobs[11]])
  //   expect(wrapper.vm.jobsByColumn[12]).toEqual([testJobs[12], testJobs[13]])
  // })

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

  it('updateColumns makes a post request', async () => {
    expect(wrapper.vm.colList).toEqual([
      { column_number: 4, id: 12, name: 'Test' },
      { column_number: 0, id: 1, name: 'To Apply' },
      { column_number: 1, id: 3, name: 'Application Submitted' },
      { column_number: 2, id: 7, name: 'OA' },
      { column_number: 3, id: 8, name: 'Interview' },
    ])
    await wrapper.vm.updateColumns([{ id: 8 }, { id: 2 }, { id: 1 }])
    expect(postRequest).toHaveBeenCalledWith('account/api/update_columns', {
      payload: [{ id: 8 }, { id: 2 }, { id: 1 }],
      user_id: mockuser.id,
    })

    expect(wrapper.vm.colList).toEqual([{ id: 8 }, { id: 2 }, { id: 1 }])
    // expect(wrapper.vm.jobsByColumn[8]).toEqual([])

    // TODO assert 2 and 1 aren't empty
  })

  it('posts a request to get_job_by_id when job detail opened', async () => {
    await wrapper.vm.showDetailModal(testJobs[1])

    expect(postRequest).toHaveBeenCalledWith('job/api/get_job_by_id', {
      job_id: testJobs[1].id,
      user_id: mockuser.id,
    })

    expect(wrapper.vm.selectedJob).toEqual(testJobs[1])
    expect(wrapper.vm.detailModalVisible).toBe(true)
  })

  // it('updates jobsByColumn when job edited', () => {
  //   wrapper.vm.isNewJob = false
  //   wrapper.vm.createOrUpdateJob({ id: 0, kcolumn_id: 8 })
  //   expect(wrapper.vm.jobsByColumn[8]).toEqual([
  //     {
  //       id: 12,
  //       company: 'Minisoft',
  //       type: 'Frontend',
  //       position: 'Senior Software Engineer',
  //       kcolumn_id: 8,
  //       deadlines: [],
  //       cover_letter: 'Test',
  //       description: 'Description',
  //       notes: 'Test',
  //     },
  //     { id: 0, kcolumn_id: 8 },
  //   ])
  // })
})

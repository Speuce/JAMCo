import { mount } from '@vue/test-utils'
import { expect, describe, it, afterEach } from 'vitest'
import JobDetailModal from '../src/components/modal/job/JobDetailModal.vue'

describe('JobDetailModal', () => {
  let wrapper
  const job = {
    id: 1,
    company: 'Test Company',
    date: '2022-01-01',
    type: 'Full-time',
    position: 'Test Position',
    description: 'Test description',
    coverLetter: 'Test cover letter',
    comments: 'Test comments',
    deadlines: [],
  }

  function mountModal(job) {
    wrapper = mount(JobDetailModal, {
      props: {
        job,
        columns: [
          { id: 1, name: 'Applied' },
          { id: 2, name: 'Interviewing' },
        ],
      },
    })
  }

  afterEach(() => {
    job.deadlines = []
    wrapper.vm.nextDeadlineId = 0
    wrapper.vm.positionErrorIndicator = null
    wrapper.vm.companyErrorIndicator = null
    wrapper.vm.deadlineError = false
  })

  it('populates with default values when no props provided', () => {
    mountModal()
    expect(wrapper.vm.jobData).toEqual({
      user: -1,
      id: -1,
      company: '',
      type: '',
      columnId: -1,
      position: '',
      description: '',
      coverLetter: '',
      comments: '',
    })

    expect(wrapper.vm.deadlines).toEqual([])
  })

  it('displays error when position is empty & save is pressed', () => {
    expect(wrapper.vm.positionErrorIndicator).toBe(null)
    expect(wrapper.vm.companyErrorIndicator).toBe(null)

    let testJob = { ...job }
    testJob.position = null
    testJob.company = 'non-empty'
    mountModal(testJob)

    wrapper.vm.saveClicked()

    expect(wrapper.vm.positionErrorIndicator).toBe('red')
    expect(wrapper.vm.companyErrorIndicator).toBe(null)
  })

  it('displays error when company is empty & save is pressed', () => {
    expect(wrapper.vm.positionErrorIndicator).toBe(null)
    expect(wrapper.vm.companyErrorIndicator).toBe(null)

    let testJob = { ...job }
    testJob.company = null
    testJob.position = 'non-empty'
    mountModal(testJob)

    wrapper.vm.saveClicked()

    expect(wrapper.vm.positionErrorIndicator).toBe(null)
    expect(wrapper.vm.companyErrorIndicator).toBe('red')
  })

  it('displays error when deadline fields empty & save clicked', () => {
    mountModal(job)
    wrapper.vm.newDeadline()

    expect(wrapper.vm.deadlineError).toBe(false)

    let buttons = wrapper.findAllComponents({ name: 'v-btn' })

    buttons.forEach((button) => {
      if (button.text() === 'Save') {
        button.trigger('click')
      }
    })

    expect(wrapper.emitted('createOrUpdateJob')).toBeFalsy()
    expect(wrapper.vm.deadlineError).toBe(true)
  })

  it('emits close when close button clicked', () => {
    mountModal(job)
    let buttons = wrapper.findAllComponents({ name: 'v-btn' })

    buttons.forEach((button) => {
      if (button.text() === 'Close') {
        button.trigger('click')
      }
    })

    expect(wrapper.emitted('close')).toBeTruthy()
  })

  it('adds deadline to list when Add Deadline clicked', () => {
    mountModal(job)
    wrapper.vm.newDeadline()
    expect(wrapper.vm.deadlines).toHaveLength(1)
  })

  it('deletes deadline from list when delete clicked', () => {
    mountModal(job)
    wrapper.vm.newDeadline()
    wrapper.vm.deleteDeadline(0)
    expect(wrapper.vm.deadlines).toHaveLength(0)
  })

  it('deletes correct deadline from multiple when delete clicked', () => {
    mountModal(job)
    wrapper.vm.newDeadline()
    wrapper.vm.newDeadline()
    wrapper.vm.newDeadline()
    wrapper.vm.deleteDeadline(1)
    expect(wrapper.vm.deadlines).toEqual([
      { id: 0, title: '', date: '' },
      { id: 2, title: '', date: '' },
    ])
  })

  it('saves job fields when save clicked', () => {
    mountModal(job)
    wrapper.vm.newDeadline()

    wrapper.vm.handleDeadlineUpdate({
      id: 0,
      title: 'Test Title',
      date: '2022-01-01',
    })

    wrapper.vm.saveClicked()

    expect(wrapper.emitted('createOrUpdateJob')).toBeTruthy()
    expect(wrapper.emitted().createOrUpdateJob[0][0]).toEqual({
      id: 1,
      company: 'Test Company',
      date: '2022-01-01',
      type: 'Full-time',
      position: 'Test Position',
      description: 'Test description',
      coverLetter: 'Test cover letter',
      comments: 'Test comments',
      deadlines: [{ id: 0, title: 'Test Title', date: '2022-01-01' }],
      columnId: 1,
    })
  })

  it('updates deadline when modified', () => {
    mountModal(job)
    wrapper.vm.newDeadline()
    wrapper.vm.handleDeadlineUpdate({
      id: 0,
      title: 'Test Title',
      date: '2022-01-01',
    })
    expect(wrapper.vm.deadlines[0]).toEqual({
      id: 0,
      title: 'Test Title',
      date: '2022-01-01',
    })
  })

  it('updates correct deadline in list when modified', () => {
    mountModal(job)
    wrapper.vm.newDeadline()
    wrapper.vm.newDeadline()
    wrapper.vm.newDeadline()
    wrapper.vm.handleDeadlineUpdate({
      id: 1,
      title: 'Test Title',
      date: '2022-01-01',
    })
    expect(wrapper.vm.deadlines).toEqual([
      { id: 0, title: '', date: '' },
      {
        id: 1,
        title: 'Test Title',
        date: '2022-01-01',
      },
      { id: 2, title: '', date: '' },
    ])
  })
})

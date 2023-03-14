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
    position_title: 'Test Position',
    description: 'Test description',
    cover_letter: 'Test cover letter',
    notes: 'Test comments',
    deadlines: [],
  }

  function mountModal(jobProp) {
    wrapper = mount(JobDetailModal, {
      props: {
        job: jobProp,
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
      id: -1,
      company: '',
      type: '',
      kcolumn_id: -1,
      user_id: -1,
      position_title: '',
      description: '',
      cover_letter: '',
      notes: '',
    })

    expect(wrapper.vm.deadlines).toEqual([])
  })

  it('displays error when position is empty & save is pressed', () => {
    expect(wrapper.vm.positionErrorIndicator).toBe(null)
    expect(wrapper.vm.companyErrorIndicator).toBe(null)

    let testJob = { ...job }
    testJob.position_title = null
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
    testJob.position_title = 'non-empty'
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
      position_title: 'Test Position',
      description: 'Test description',
      cover_letter: 'Test cover letter',
      notes: 'Test comments',
      deadlines: [{ id: 0, title: 'Test Title', date: '2022-01-01' }],
      kcolumn_id: 1,
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

  it('sorts deadlines in list by date', () => {
    mountModal(job)
    wrapper.vm.newDeadline()
    wrapper.vm.newDeadline()
    wrapper.vm.newDeadline()
    wrapper.vm.newDeadline()
    wrapper.vm.handleDeadlineUpdate({
      id: 0,
      title: 'Latest',
      date: '2022-05-05',
    })
    wrapper.vm.handleDeadlineUpdate({
      id: 1,
      title: 'Earliest',
      date: '2022-01-01',
    })
    wrapper.vm.handleDeadlineUpdate({
      id: 3,
      title: 'Middle-copy',
      date: '2022-03-03',
    })
    wrapper.vm.handleDeadlineUpdate({
      id: 2,
      title: 'Middle',
      date: '2022-03-03',
    })
    wrapper.vm.saveClicked()
    expect(wrapper.vm.deadlines).toEqual([
      {
        id: 1,
        title: 'Earliest',
        date: '2022-01-01',
      },
      {
        id: 2,
        title: 'Middle',
        date: '2022-03-03',
      },
      {
        id: 3,
        title: 'Middle-copy',
        date: '2022-03-03',
      },
      {
        id: 0,
        title: 'Latest',
        date: '2022-05-05',
      },
    ])
  })
  it('updates a deadline in a sorted list', () => {
    mountModal(job)
    wrapper.vm.newDeadline()
    wrapper.vm.newDeadline()
    wrapper.vm.handleDeadlineUpdate({
      id: 0,
      title: 'Latest',
      date: '2022-05-05',
    })
    wrapper.vm.handleDeadlineUpdate({
      id: 1,
      title: 'Earliest',
      date: '2022-01-01',
    })
    wrapper.vm.saveClicked()
    wrapper.vm.handleDeadlineUpdate({
      id: 1,
      title: 'Earliest-edited',
      date: '2022-01-01',
    })
    expect(wrapper.vm.deadlines).toEqual([
      {
        id: 1,
        title: 'Earliest-edited',
        date: '2022-01-01',
      },
      {
        id: 0,
        title: 'Latest',
        date: '2022-05-05',
      },
    ])
  })
})

import { mount } from '@vue/test-utils'
import { expect, describe, it, afterEach, vi } from 'vitest';
import ReviewRequestModal from '../src/components/modal/job/ReviewRequestModal.vue'
import { postRequest } from '@/helpers/requests.js'

vi.mock('@/helpers/requests.js', () => ({
  postRequest: vi.fn(),
}))

describe('ReviewRequestModal', () => {
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
    user_id: 0,
  }

  function mountModal(jobProp, userProp) {
    wrapper = mount(ReviewRequestModal, {
      props: {
        job: jobProp,
        user: userProp,
      },
    })
  }

  afterEach(() => {
    wrapper.vm.messageErrorIndicator = null
    wrapper.vm.recipientErrorIndicator = null
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
  })

  it('emits close when cancel button clicked', () => {
    mountModal(job)
    let buttons = wrapper.findAllComponents({ name: 'v-btn' })

    buttons.forEach((button) => {
      if (button.text() === 'Cancel') {
        button.trigger('click')
      }
    })

    expect(wrapper.emitted('close')).toBeTruthy()
  })

  it('emits close when send button clicked', () => {
    mountModal(job)
    let buttons = wrapper.findAllComponents({ name: 'v-btn' })
    wrapper.vm.selectedFriendIds = [-1]

    buttons.forEach((button) => {
      if (button.text() === 'Send') {
        button.trigger('click')
      }
    })

    expect(wrapper.emitted('close')).toBeTruthy()
  })

  it('displays error when send button is pressed without any recipients', () => {
    expect(wrapper.vm.recipientErrorIndicator).toBe(null)
    expect(wrapper.vm.messageErrorIndicator).toBe(null)

    mountModal(job)
    wrapper.vm.selectedFriendIds = []
    wrapper.vm.sendClicked()

    expect(wrapper.vm.recipientErrorIndicator).toBe('red')
    expect(wrapper.vm.messageErrorIndicator).toBe(null)
  })

  it('displays error when send button is pressed without any message', () => {
    expect(wrapper.vm.recipientErrorIndicator).toBe(null)
    expect(wrapper.vm.messageErrorIndicator).toBe(null)

    mountModal(job)
    wrapper.vm.selectedFriendIds = [-1]
    wrapper.vm.message = ''
    wrapper.vm.sendClicked()

    expect(wrapper.vm.recipientErrorIndicator).toBe(null)
    expect(wrapper.vm.messageErrorIndicator).toBe('red')
  })

  it('sends a review request when send button clicked', () => {
    mountModal(job)
    postRequest.mockImplementation(() => Promise.resolve())
    let buttons = wrapper.findAllComponents({ name: 'v-btn' })

    wrapper.vm.selectedFriendIds = [1, 2]

    buttons.forEach((button) => {
      if (button.text() === 'Send') {
        button.trigger('click')
      }
    })

    wrapper.vm.selectedFriendIds.forEach((id) => {
      expect(postRequest).toHaveBeenCalledWith(
        'job/api/create_review_request',
        {
          job_id: job.id,
          reviewer_id: id,
          message: wrapper.vm.message,
        },
      )
    })
  })
})

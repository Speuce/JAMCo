import { mount } from '@vue/test-utils'
import { expect, describe, it } from 'vitest';
import ReviewRequestModal from '../src/components/modal/job/ReviewRequestModal.vue'

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
  }

  function mountModal(jobProp) {
    wrapper = mount(ReviewRequestModal, {
      props: {
        job: jobProp,
      },
    })
  }

  it('populates with default values when no props provided', () => {
    mountModal()
    expect(wrapper.vm.jobData).toEqual({
      user: -1,
      id: -1,
      company: '',
      type: '',
      kcolumn_id: -1,
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
    wrapper.vm.sendClicked()

    expect(wrapper.vm.recipientErrorIndicator).toBe('red')
    expect(wrapper.vm.messageErrorIndicator).toBe(null)
  })

  it('displays error when send button is pressed without any message', () => {
    expect(wrapper.vm.recipientErrorIndicator).toBe(null)
    expect(wrapper.vm.messageErrorIndicator).toBe(null)

    mountModal(job)
    wrapper.vm.sendClicked()

    expect(wrapper.vm.recipientErrorIndicator).toBe(null)
    expect(wrapper.vm.messageErrorIndicator).toBe('red')
  })

  it('sends a review request when send button clicked', () => {
    mountModal(job)
    let buttons = wrapper.findAllComponents({ name: 'v-btn' })

    buttons.forEach((button) => {
      if (button.text() === 'Cancel') {
        button.trigger('click')
      }
    })

    expect(wrapper.emitted('sendReviewRequest')).toBeTruthy()
  })
})

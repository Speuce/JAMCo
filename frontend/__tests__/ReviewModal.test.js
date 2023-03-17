import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest';
import ReviewModal from '../src/components/modal/job/ReviewModal.vue'
import { postRequest } from '@/helpers/requests.js'

vi.mock('@/helpers/requests.js', () => ({
  postRequest: vi.fn(),
}))

describe('ReviewModal', () => {
  let wrapper

  function mountModal() {
    wrapper = mount(ReviewModal, {})
  }

  beforeEach(() => {
    postRequest.mockImplementation(() => Promise.resolve({ job_data: {} }))
    mountModal()
  })

  it('emits close when close button clicked', () => {
    const buttons = wrapper.findAllComponents({ name: 'v-btn' })

    buttons.forEach((button) => {
      if (button.text() === 'Cancel') {
        button.trigger('click')
      }
    })

    expect(wrapper.emitted('close')).toBeTruthy()
  })

  it('sends a review and closes when send button clicked', async () => {
    wrapper.vm.review = '4.85 / 5 - 97 %'
    await wrapper.vm.sendClicked()

    expect(postRequest).toHaveBeenCalledWith('job/api/create_review', {
      request_id: wrapper.vm.request.id,
      response: wrapper.vm.review,
    })
    expect(wrapper.emitted('close')).toBeTruthy()
    expect(wrapper.vm.messageErrorIndicator).toBe(null)
  })

  it('displays an error when send button is clicked without any review', () => {
    expect(wrapper.vm.messageErrorIndicator).toBe(null)
    wrapper.vm.sendClicked()
    expect(wrapper.vm.messageErrorIndicator).toBe('red')
  })

  it('treats a whitespace-only review as empty', () => {
    expect(wrapper.vm.messageErrorIndicator).toBe(null)
    wrapper.vm.review = '\n\n\n\n\n\n\t\t\t\t\t\t\t\t\t\t                  '
    wrapper.vm.sendClicked()
    expect(wrapper.vm.messageErrorIndicator).toBe('red')
  })
})

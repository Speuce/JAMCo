import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest';
import ReviewModal from '../src/components/modal/job/ReviewModal.vue'

describe('ReviewModal', () => {
  let wrapper

  function mountModal() {
    wrapper = mount(ReviewModal, {})
  }

  it('emits close when close button clicked', () => {
    mountModal()
    let buttons = wrapper.findAllComponents({ name: 'v-btn' })

    buttons.forEach((button) => {
      if (button.text() === 'Close') {
        button.trigger('click')
      }
    })

    expect(wrapper.emitted('close')).toBeTruthy()
  })

  it('sends a review when send button clicked', () => {
    fail()
  })

  it('displays an error when send button is clicked without any review', () => {
    fail()
  })
})

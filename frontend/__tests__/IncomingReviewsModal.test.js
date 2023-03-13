import { mount } from '@vue/test-utils'
import { expect, describe, it, fail } from 'vitest';
import IncomingReviewsModal from '../src/components/modal/job/IncomingReviewsModal.vue'

describe('IncomingReviewsModal', () => {
  let wrapper

  function mountModal() {
    wrapper = mount(IncomingReviewsModal, {})
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

  it('displays a message when there are no reviews', () => {
    fail()
  })

  it("doesn't display that message when there's at least one review", () => {
    fail()
  })
})

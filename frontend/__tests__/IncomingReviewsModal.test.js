import { mount } from '@vue/test-utils'
import { expect, describe, it, vi, beforeEach } from 'vitest';
import IncomingReviewsModal from '../src/components/modal/job/IncomingReviewsModal.vue'
import { postRequest } from '@/helpers/requests.js'

vi.mock('@/helpers/requests.js', () => ({
  postRequest: vi.fn(),
}))

describe('IncomingReviewsModal', () => {
  let wrapper

  const testReviews = [
    {
      response:
        'Excellent cover letter! However, minor spelling mistake, I win.',
    },
  ]

  const testRequests = [
    {
      message:
        'heres my cover letter: https://www.youtube.com/watch?v=dQw4w9WgXcQ :)',
      sender: {},
    },
  ]

  function mountModal() {
    wrapper = mount(IncomingReviewsModal, {})
  }

  beforeEach(() => {
    postRequest.mockImplementation(() => Promise.resolve({ review_requests: [], reviews: [] }))
    mountModal()
  })

  it('emits close when close button clicked', () => {
    let buttons = wrapper.findAllComponents({ name: 'v-btn' })

    buttons.forEach((button) => {
      if (button.text() === 'Close') {
        button.trigger('click')
      }
    })

    expect(wrapper.emitted('close')).toBeTruthy()
  })

  it('displays a message when there are no reviews nor review requests', () => {
    expect(
      wrapper.findComponent({ ref: 'emptyInboxMessage' }).exists(),
    ).toBeTruthy()
  })

  it("doesn't display that message when there's at least one review", async () => {
    wrapper.vm.reviews = testReviews
    await wrapper.vm.$nextTick()

    expect(
      wrapper.findComponent({ ref: 'emptyInboxMessage' }).exists(),
    ).toBeFalsy()
  })

  it("doesn't display that message when there's at least one review request", async () => {
    wrapper.vm.reviewRequests = testRequests
    await wrapper.vm.$nextTick()

    expect(
      wrapper.findComponent({ ref: 'emptyInboxMessage' }).exists(),
    ).toBeFalsy()
  })

  it('opens the review modal when the review button is clicked', async () => {
    wrapper.vm.reviewRequests = testRequests
    await wrapper.vm.$nextTick()

    let buttons = wrapper.findAllComponents({ name: 'v-btn' })
    const reviewClicked = vi.spyOn(wrapper.vm, 'reviewClicked')

    buttons.forEach((button) => {
      if (button.text() === 'Review') {
        button.trigger('click')
      }
    })

    expect(reviewClicked).toHaveBeenCalled()
  })

  it('hides the review request section when there are no review requests', () => {
    expect(
      wrapper.findComponent({ ref: 'requestSection' }).exists(),
    ).toBeFalsy()
  })

  it("shows the review request section when there's at least one review request", async () => {
    wrapper.vm.reviewRequests = testRequests
    await wrapper.vm.$nextTick()

    expect(
      wrapper.findComponent({ ref: 'requestSection' }).exists(),
    ).toBeTruthy()
  })

  it('hides the review section when there are no reviews', () => {
    expect(wrapper.findComponent({ ref: 'reviewSection' }).exists()).toBeFalsy()
  })

  it("shows the review section when there's at least one review", async () => {
    wrapper.vm.reviews = testReviews
    await wrapper.vm.$nextTick()

    expect(
      wrapper.findComponent({ ref: 'reviewSection' }).exists(),
    ).toBeTruthy()
  })
})

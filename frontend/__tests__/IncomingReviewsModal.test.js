import { mount } from '@vue/test-utils'
import { expect, describe, it, vi } from 'vitest'
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
      sender_id: 2,
    },
  ]

  function mountModal() {
    const userData = {
      id: 1,
      friends: [
        {
          id: 2,
        },
      ],
    }
    wrapper = mount(IncomingReviewsModal, {
      propsData: { user: userData },
    })
  }

  const mockPostRequest = () => {
    return Promise.resolve({
      review_requests: testRequests,
      reviews: testReviews,
    })
  }

  const mockEmptyPostRequest = () => {
    return Promise.resolve({
      review_requests: [],
      reviews: [{ reviewer_id: 2 }],
    })
  }

  it('emits close when close button clicked', () => {
    postRequest.mockImplementation(mockEmptyPostRequest)
    mountModal()
    let buttons = wrapper.findAllComponents({ name: 'v-btn' })

    buttons.forEach((button) => {
      if (button.text() === 'Close') {
        button.trigger('click')
      }
    })

    expect(wrapper.emitted('close')).toBeTruthy()
  })

  it('displays a message when there are no reviews nor review requests', () => {
    postRequest.mockImplementation(mockEmptyPostRequest)
    mountModal()
    expect(
      wrapper.findComponent({ ref: 'emptyInboxMessage' }).exists(),
    ).toBeTruthy()
  })

  it("doesn't display that message when there's at least one review", async () => {
    postRequest.mockImplementation(mockPostRequest)
    mountModal()

    wrapper.vm.reviews = [
      { id: 0, reviewer: { first_name: 'first', last_name: 'last' } },
    ]

    expect(wrapper.vm.reviews.length).toBe(1)
  })

  it("doesn't display that message when there's at least one review request", async () => {
    postRequest.mockImplementation(mockPostRequest)
    mountModal()

    wrapper.vm.reviews = [{ id: 0 }]
    wrapper.vm.reviewRequests = [
      { fulfilled: false, sender: { first_name: 'first', last_name: 'last' } },
    ]

    expect(wrapper.vm.pendingReviewRequests.length).toBe(1)
  })

  it('opens the review modal when the review button is clicked', async () => {
    postRequest.mockImplementation(mockPostRequest)
    mountModal()

    await wrapper.vm.$nextTick()

    wrapper.vm.requestData = {
      id: 0,
      sender: { first_name: 'first', last_name: 'last' },
    }

    wrapper.vm.reviewClicked({
      id: 0,
      sender: { first_name: 'first', last_name: 'last' },
    })
    expect(wrapper.vm.currentlySelectedRequest).toEqual({
      id: 0,
      sender: { first_name: 'first', last_name: 'last' },
    })
    expect(wrapper.vm.reviewModalVisible).toBe(true)
  })

  it('hides the review request section when there are no review requests', () => {
    postRequest.mockImplementation(mockEmptyPostRequest)
    mountModal()
    expect(
      wrapper.findComponent({ ref: 'requestSection' }).exists(),
    ).toBeFalsy()
  })

  it("shows the review request section when there's at least one review request", async () => {
    postRequest.mockImplementation(mockPostRequest)
    mountModal()

    wrapper.vm.reviewRequests = [
      { fulfilled: false, sender: { first_name: 'first', last_name: 'last' } },
    ]

    expect(wrapper.vm.pendingReviewRequests).toEqual([
      { fulfilled: false, sender: { first_name: 'first', last_name: 'last' } },
    ])

    expect(wrapper.vm.pendingReviewRequests.length).toEqual(1)
  })

  it('hides the review section when there are no reviews', () => {
    postRequest.mockImplementation(mockEmptyPostRequest)
    mountModal()
    expect(wrapper.findComponent({ ref: 'reviewSection' }).exists()).toBeFalsy()
  })

  it("shows the review section when there's at least one review", async () => {
    postRequest.mockImplementation(mockPostRequest)
    mountModal()

    wrapper.vm.reviews = [
      { fulfilled: false, sender: { first_name: 'first', last_name: 'last' } },
    ]

    expect(wrapper.vm.reviews.length).toEqual(1)
  })

  it('handles reviewModalClosed', async () => {
    mountModal()

    await wrapper.vm.reviewModalClosed()
    expect(wrapper.vm.reviewModalVisible).toBe(false)
  })
})

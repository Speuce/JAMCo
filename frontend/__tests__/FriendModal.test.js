import FriendModal from '@/components/modal/friend/FriendModal.vue'
import { expect, describe, it, vi, afterEach } from 'vitest'
import { shallowMount } from '@vue/test-utils'
import { postRequest } from '@/helpers/requests.js'

vi.mock('@/helpers/requests.js', () => ({
  postRequest: vi.fn(),
}))

describe('FriendModal', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('emits fetchUserData event after accepting friend request', async () => {
    const userData = { id: 1 }
    const request = { id: 2, from_user_id: 3 }
    const wrapper = shallowMount(FriendModal, {
      propsData: { userData },
    })

    postRequest.mockReturnValue(Promise.resolve())

    await wrapper.vm.acceptFriendRequest(request)

    expect(postRequest).toHaveBeenCalledWith(
      'account/api/accept_friend_request',
      {
        request_id: request.id,
        to_user_id: userData.id,
        from_user_id: request.from_user_id,
      },
    )

    expect(wrapper.emitted().fetchUserData).toBeTruthy()
  })

  it('emits fetchUserData event after denying friend request', async () => {
    const userData = { id: 1 }
    const request = { id: 2, from_user_id: 3 }
    const wrapper = shallowMount(FriendModal, {
      propsData: { userData },
    })

    postRequest.mockReturnValue(Promise.resolve())

    await wrapper.vm.denyFriendRequest(request)

    expect(postRequest).toHaveBeenCalledWith(
      'account/api/deny_friend_request',
      {
        request_id: request.id,
        from_user_id: request.from_user_id,
        to_user_id: userData.id,
      },
    )

    expect(wrapper.emitted().fetchUserData).toBeTruthy()
  })

  it('emits fetchUserData event after removing a friend', async () => {
    const userData = { id: 1 }
    const friend = { id: 2 }
    const wrapper = shallowMount(FriendModal, {
      propsData: { userData },
    })

    postRequest.mockReturnValue(Promise.resolve())

    await wrapper.vm.removeFriend(friend)

    expect(postRequest).toHaveBeenCalledWith('account/api/remove_friend', {
      user1_id: userData.id,
      user2_id: friend.id,
    })

    expect(wrapper.emitted().fetchUserData).toBeTruthy()
  })
})

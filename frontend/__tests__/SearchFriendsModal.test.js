import SearchFriendsModal from '@/components/modal/friend/SearchFriendsModal.vue'
import { expect, describe, it, vi, afterEach, beforeEach } from 'vitest'
import { postRequest } from '@/helpers/requests.js'
import { shallowMount } from '@vue/test-utils'

vi.mock('@/helpers/requests.js', () => ({
  postRequest: vi.fn(),
}))

describe('SearchFriendsModal', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  beforeEach(() => {
    postRequest.mockClear()
  })

  it('searches for users when triggerSearch method is called', async () => {
    const searchField = 'John'
    const userData = { id: 1, google_id: 'google123' }
    const response = { user_list: [{ id: 2, google_id: 'google456' }] }
    postRequest.mockResolvedValueOnce(response)

    const wrapper = shallowMount(SearchFriendsModal, {
      propsData: {
        userData,
      },
    })

    wrapper.setData({ searchField })

    await wrapper.vm.triggerSearch()

    expect(postRequest).toHaveBeenCalledWith(
      'account/api/search_users_by_name',
      searchField,
    )
    expect(wrapper.vm.searchResults).toEqual(response.user_list)
  })

  it('does not include current user in search results', async () => {
    const searchField = 'John'
    const userData = { id: 1, google_id: 'google123' }
    const response = {
      user_list: [
        { id: 1, google_id: 'google123' },
        { id: 2, google_id: 'google456' },
      ],
    }
    postRequest.mockResolvedValueOnce(response)

    const wrapper = shallowMount(SearchFriendsModal, {
      propsData: {
        userData,
      },
    })

    wrapper.setData({ searchField })

    await wrapper.vm.triggerSearch()

    expect(wrapper.vm.searchResults).toEqual([
      { id: 2, google_id: 'google456' },
    ])
  })

  it('sends friend request when sendFriendRequest method is called', async () => {
    const userData = { id: 1, google_id: 'google123' }
    const user = { id: 2, google_id: 'google456' }

    const wrapper = shallowMount(SearchFriendsModal, {
      propsData: {
        userData,
      },
    })

    await wrapper.vm.sendFriendRequest(user)

    expect(postRequest).toHaveBeenCalledWith(
      'account/api/create_friend_request',
      {
        from_user_id: userData.id,
        to_user_id: user.id,
      },
    )
    expect(wrapper.emitted().fetchUserData).toBeTruthy()
  })

  it('removes friend when removeFriend method is called', async () => {
    const userData = { id: 1, google_id: 'google123' }
    const user = { id: 2, google_id: 'google456' }

    const wrapper = shallowMount(SearchFriendsModal, {
      propsData: {
        userData,
      },
    })

    await wrapper.vm.removeFriend(user)

    expect(postRequest).toHaveBeenCalledWith('account/api/remove_friend', {
      user1_id: userData.id,
      user2_id: user.id,
    })
    expect(wrapper.emitted().fetchUserData).toBeTruthy()
  })

  it('triggers friend Kanban View when viewFriendKanban is called', () => {
    const userData = { id: 1, google_id: 'google123' }
    const user = { id: 2, google_id: 'google456' }

    const wrapper = shallowMount(SearchFriendsModal, {
      propsData: {
        userData,
      },
    })

    wrapper.vm.viewFriendKanban(user)

    expect(wrapper.emitted().viewKanban[0][0]).toEqual(user)
    expect(wrapper.emitted().close).toBeTruthy()
  })
})

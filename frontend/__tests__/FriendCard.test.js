import FriendCard from '@/components/modal/friend/FriendCard.vue'
import { expect, describe, it, vi, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { postRequest } from '@/helpers/requests.js'

vi.mock('@/helpers/requests.js', () => ({
  postRequest: vi.fn(),
}))

describe('FriendCard', () => {
  let wrapper
  const user = { id: 1, first_name: 'Human', last_name: 'Person' }

  function mountModal(userProp) {
    wrapper = mount(FriendCard, {
      props: {
        userData: userProp,
        isFriend: true,
        sentRequest: false,
      },
    })
  }

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('emits viewKanban due to share setting', async () => {
    postRequest.mockResolvedValue({ share_kanban: true })
    mountModal(user)
    await wrapper.vm.$nextTick()
    expect(postRequest).toHaveBeenCalledWith('account/api/get_user_privacies', {
      user_id: 1,
    })

    await wrapper.vm.$nextTick()
    expect(wrapper.vm.kanbanViewable).toBeTruthy()

    wrapper.vm.requestBoardViewing()
    expect(wrapper.emitted().viewKanban).toBeTruthy()
  })
})

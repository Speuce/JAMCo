import { flushPromises, shallowMount } from '@vue/test-utils'
import MainView from '@/views/MainView.vue'
import { expect, describe, it, vi, afterEach, beforeEach } from 'vitest'
import { postRequest } from '@/helpers/requests.js'
import { getAuthToken } from '@/helpers/auth-cookie.js'

vi.mock('@/helpers/requests.js', () => ({
  postRequest: vi.fn(),
}))

vi.mock('@/helpers/auth-cookie.js', () => ({
  getAuthToken: vi.fn(),
  setAuthToken: vi.fn(),
}))

const mostPostRequest = () => {
  return Promise.resolve({ data: {}, user: { id: -1 } })
}

describe('MainView', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })
  beforeEach(() => {
    postRequest.mockImplementation(mostPostRequest)
  })
  it('sets userData when userSignedIn is called', () => {
    const wrapper = shallowMount(MainView)
    const resp = { data: { id: -1 }, token: 'new_token' }
    wrapper.vm.userSignedIn(resp)
    expect(wrapper.vm.userData).toEqual({ id: -1 })
  })

  it('opens setupModal when a required field is not filled', () => {
    const wrapper = shallowMount(MainView)
    const resp = {
      // no field_of_work present
      data: {
        id: -1,
        first_name: 'Spongeboy',
        last_name: 'Brownpants',
        country: 'Pacific Ocean',
        email: 'test_email',
      },
      token: 'new_token',
    }
    wrapper.vm.userSignedIn(resp)
    expect(wrapper.vm.setupModalVisible).toEqual(true)
  })

  it('posts userData & privacies, closes setupModal on updateUserAccount call', async () => {
    const wrapper = shallowMount(MainView)
    expect(wrapper.vm.setupModalVisible).toEqual(false)
    const resp = { data: { id: -1 }, token: 'new_token' }
    wrapper.vm.userSignedIn(resp)

    expect(wrapper.vm.setupModalVisible).toEqual(true)

    await wrapper.vm.updateUserAccount({ id: -1 }, { id: 1 })

    expect(wrapper.vm.userData).toEqual({ id: -1 })
    expect(wrapper.vm.setupModalVisible).toEqual(false)

    expect(postRequest.mock.calls).toEqual([
      ['account/api/get_user_privacies', { user_id: -1 }],
      ['account/api/update_account', { id: -1 }],
      ['account/api/update_privacies', { privacies: { id: 1 }, user_id: -1 }],
    ])
  })

  it('authenticates token when cookie found', async () => {
    getAuthToken.mockReturnValue('token')
    shallowMount(MainView)
    flushPromises()

    expect(postRequest).toHaveBeenCalledWith(
      'account/api/validate_auth_token',
      'token',
    )
  })

  it('logs out when logoutClicked', () => {
    const wrapper = shallowMount(MainView)
    delete window.location
    window.location = { reload: vi.fn() }
    wrapper.vm.logoutClicked()
    expect(window.location.reload).toHaveBeenCalled()
    expect(wrapper.vm.userData).toBe(null)
  })
})

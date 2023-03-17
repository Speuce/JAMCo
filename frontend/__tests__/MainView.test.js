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

  it('catches Error when auth_token validation fails', async () => {
    getAuthToken.mockReturnValue('token')
    postRequest.mockReturnValue(Error())
    const warnSpy = vi.spyOn(console, 'warn')
    shallowMount(MainView)
    flushPromises()

    expect(postRequest).toHaveBeenCalledWith(
      'account/api/validate_auth_token',
      'token',
    )

    expect(warnSpy).toBeCalledWith('Token Authentication Failed')
  })

  it('logs out when logoutClicked', () => {
    const wrapper = shallowMount(MainView)
    wrapper.vm.logoutClicked()
    expect(wrapper.vm.userData).toBe(null)
    expect(wrapper.vm.userPrivacies).toBe(null)
    expect(wrapper.vm.setupModalVisible).toBe(false)
    expect(wrapper.vm.userInfoModalVisible).toBe(false)
    expect(wrapper.vm.failedAuthentication).toBe(true)
    expect(wrapper.vm.friendModalVisible).toBe(false)
  })

  it('calls the onSignin method with the response and makes the post request', async () => {
    const wrapper = shallowMount(MainView)
    postRequest.mockResolvedValue({ data: { client_id: 'some-client' } })
    const response = { credential: 'some-credential', client_id: 'some-client' }
    wrapper.vm.onSignin(response)
    await wrapper.vm.$nextTick()
    expect(postRequest).toHaveBeenCalledWith(
      'account/api/get_or_create_account',
      response,
    )
  })

  it('displays friends modal when showFriendsModal called', () => {
    const wrapper = shallowMount(MainView)

    expect(wrapper.vm.friendModalVisible).toEqual(false)
    wrapper.vm.showFriendsModal()
    expect(wrapper.vm.friendModalVisible).toEqual(true)
  })

  it('fetches user data when fetchUserData called', async () => {
    const wrapper = shallowMount(MainView)
    postRequest.mockResolvedValue({ user: { id: 0 } })
    wrapper.vm.authtoken = 'valid_token'

    wrapper.vm.fetchUserData()

    await wrapper.vm.$nextTick()

    expect(postRequest).toHaveBeenCalledWith(
      'account/api/get_updated_user_data',
      'valid_token',
    )
  })
})

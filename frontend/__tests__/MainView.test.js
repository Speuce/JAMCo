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

const mostPostRequest = (url) => {
  return Promise.resolve({ data: {}, user: 'gerald' })
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
      // no email present
      data: {
        id: -1,
        first_name: 'Spongeboy',
        last_name: 'Brownpants',
        country: 'Pacific Ocean',
        field_of_work: 'Fry Cook',
      },
      token: 'new_token',
    }
    wrapper.vm.userSignedIn(resp)
    expect(wrapper.vm.setupModalVisible).toEqual(true)
  })

  it('posts userData to update_account, closes setupModal on updateUserAccount call', async () => {
    const wrapper = shallowMount(MainView)
    expect(wrapper.vm.setupModalVisible).toEqual(false)
    const resp = { data: { id: -1 }, token: 'new_token' }
    wrapper.vm.userSignedIn(resp)
    expect(wrapper.vm.setupModalVisible).toEqual(true)

    wrapper.vm.updateUserAccount({ id: -1 })
    await wrapper.vm.$nextTick()
    expect(postRequest).toHaveBeenCalledWith('account/api/update_account', {
      id: -1,
    })

    expect(wrapper.vm.userData).toEqual({ id: -1 })
    expect(wrapper.vm.setupModalVisible).toEqual(false)
  })

  it('authenticates token when cookie found', async () => {
    getAuthToken.mockReturnValue('bruh')
    const wrapper = shallowMount(MainView)
    flushPromises()

    expect(postRequest).toHaveBeenCalledWith(
      'account/api/validate_auth_token',
      'bruh',
    )
    expect(wrapper.vm.userSignedIn).toBeCalledWith({
      data: { id: 0 },
      token: 'new_token',
    })
  })
})

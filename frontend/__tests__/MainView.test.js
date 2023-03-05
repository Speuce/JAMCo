import { flushPromises, shallowMount } from '@vue/test-utils'
import MainView from '@/views/MainView.vue'
import { expect, describe, it, vi, afterEach } from 'vitest'
import { postRequest } from '@/helpers/requests.js'

vi.mock('@/helpers/requests.js', () => ({
  postRequest: vi.fn(),
}))

function initAuthMocks() {
  vi.mock('@/helpers/auth-cookie.js', () => ({
    getAuthToken: vi.fn(),
    setAuthToken: vi.fn(),
  }))
}

describe('MainView', () => {
  afterEach(() => {
    vi.resetAllMocks()
  })

  it('sets userData when userSignedIn is called', () => {
    initAuthMocks()
    const wrapper = shallowMount(MainView)
    const resp = { data: { id: -1 }, token: 'new_token' }
    wrapper.vm.userSignedIn(resp)
    expect(wrapper.vm.userData).toEqual({ id: -1 })
  })

  it('opens setupModal when a required field is not filled', () => {
    initAuthMocks()
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
    initAuthMocks()
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
    vi.mock('@/helpers/auth-cookie.js', () => ({
      getAuthToken: vi.fn().mockReturnValue('bruh'),
      setAuthToken: vi.fn(),
    }))
    const wrapper = shallowMount(MainView)

    flushPromises()

    expect(postRequest).toHaveBeenCalledWith(
      'account/api/validate_auth_token',
      {
        token: 'token',
      },
    )
    expect(wrapper.vm.userSignedIn).toBeCalledWith({
      data: { id: 0 },
      token: 'new_token',
    })
  })

  it('logs out when logoutClicked', () => {
    const wrapper = shallowMount(MainView)
    wrapper.vm.logoutClicked()
    expect(wrapper.vm.userData).toBe(null)
  })
})

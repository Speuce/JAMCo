import { shallowMount } from '@vue/test-utils'
import MainView from '@/views/MainView.vue'
import { expect, describe, it, vi } from 'vitest'
import { postRequest } from '@/helpers/requests.js'

vi.mock('@/helpers/requests.js', () => ({
  postRequest: vi.fn(),
}))

describe('MainView', () => {
  it('sets userData when userSignedIn is called', () => {
    const wrapper = shallowMount(MainView)
    const resp = { data: { id: -1 }, created: true }
    wrapper.vm.userSignedIn(resp)
    expect(wrapper.vm.userData).toEqual({ id: -1 })
  })

  it('opens setupModal when created is true', () => {
    const wrapper = shallowMount(MainView)
    const resp = { data: { id: -1 }, created: true }
    wrapper.vm.userSignedIn(resp)
    expect(wrapper.vm.setupModalVisible).toEqual(true)
  })

  it('doesnt open setupModal when created is false and required fields are filled', () => {
    const wrapper = shallowMount(MainView)
    const resp = {
      data: {
        id: -1,
        first_name: 'Spongeboy',
        last_name: 'Brownpants',
        country: 'Pacific Ocean',
        field_of_work: 'Fry Cook',
        email: 'bob@krab.com',
      },
      created: false,
    }
    wrapper.vm.userSignedIn(resp)
    expect(wrapper.vm.setupModalVisible).toEqual(false)
  })

  it('opens setupModal when created is false and a required field is not filled', () => {
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
      created: false,
    }
    wrapper.vm.userSignedIn(resp)
    expect(wrapper.vm.setupModalVisible).toEqual(true)
  })

  it('posts userData to update_account, closes setupModal on updateUserAccount call', async () => {
    const wrapper = shallowMount(MainView)
    expect(wrapper.vm.setupModalVisible).toEqual(false)
    const resp = { data: { id: -1 }, created: true }
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
})

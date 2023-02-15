import { shallowMount } from '@vue/test-utils'
import MainView from '@/views/MainView.vue'
import { expect, describe, it, vi } from 'vitest'
vi.mock('@/helpers/requests.js')

describe('MainView', () => {
  it('sets userData when userSignedIn is called', () => {
    const wrapper = shallowMount(MainView)
    const resp = { data: 'test data', created: true }
    wrapper.vm.userSignedIn(resp)
    expect(wrapper.vm.userData).toEqual('test data')
  })
})

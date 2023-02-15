import { shallowMount } from '@vue/test-utils'
import LoginModal from '@/components/modal/login/LoginModal.vue'
import { expect, describe, it, vi } from 'vitest'
vi.mock('@/helpers/requests.js')

describe('LoginModal', () => {
  it('is open by default', () => {
    const wrapper = shallowMount(LoginModal)
    expect(wrapper.vm.open).toEqual(true)
  })
})

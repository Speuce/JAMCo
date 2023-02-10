import { mount } from '@vue/test-utils'
import SigninButton from '@/components/signin/GoogleSignin.vue'
import { postRequest } from '@/helpers/requests.js'
import { expect, describe, beforeEach, afterEach, it, vi } from 'vitest'
vi.mock('@/helpers/requests.js')

describe('GoogleSignin.vue', () => {
  let wrapper
  let mockWindow

  beforeEach(() => {
    mockWindow = {
      addEventListener: vi.fn(),
      google: {
        accounts: {
          id: {
            initialize: vi.fn(),
            renderButton: vi.fn(),
          },
        },
      },
    }
    vi.stubGlobal('addEventListener', mockWindow.addEventListener)
    vi.stubGlobal('google', mockWindow.google)
    wrapper = mount(SigninButton, {
      attachToDocument: true,
      stubs: ['router-link'],
    })
  })

  afterEach(() => {
    vi.resetAllMocks()
  })

  it('calls the initialize function on window load', () => {
    expect(mockWindow.addEventListener).toHaveBeenCalledWith(
      'load',
      expect.any(Function)
    )
    const loadCallback = mockWindow.addEventListener.mock.calls[0][1]
    loadCallback()
    expect(mockWindow.google.accounts.id.initialize).toHaveBeenCalled()
  })

  it('calls the renderButton function with the correct parameters', () => {
    const loadCallback = mockWindow.addEventListener.mock.calls[0][1]
    loadCallback()
    expect(mockWindow.google.accounts.id.renderButton).toHaveBeenCalledWith(
      document.getElementById('signin_button'),
      {
        theme: 'outline',
        size: 'large',
        text: 'continue_with',
        shape: 'pill',
      }
    )
  })

  it('calls the onSignin method with the response and makes the post request', async () => {
    const response = { credential: 'some-credential' }
    wrapper.vm.onSignin(response)
    await wrapper.vm.$nextTick()
    expect(postRequest).toHaveBeenCalledWith(
      'account/api/get_or_create_account',
      { credential: response.credential }
    )
  })
})

import { expect, describe, beforeEach, afterEach, it, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import SigninButton from '@/components/signin/GoogleSignin.vue'

vi.mock('@/helpers/requests.js', () => ({
  postRequest: vi.fn(),
}))
describe('GoogleSignin.vue', () => {
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
    mount(SigninButton, {
      attachToDocument: true,
      stubs: ['router-link'],
    })
  })

  afterEach(() => {
    vi.resetAllMocks()
  })

  it('calls the initialize function on mounted', () => {
    expect(mockWindow.google.accounts.id.initialize).toHaveBeenCalled()
    expect(mockWindow.google.accounts.id.renderButton).toHaveBeenCalledWith(
      document.getElementById('signin_button'),
      {
        theme: 'outline',
        size: 'large',
        text: 'continue_with',
        shape: 'pill',
      },
    )
  })
})

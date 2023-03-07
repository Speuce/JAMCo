import { getAuthToken, setAuthToken } from '@/helpers/auth-cookie.js'
import { expect, describe, it, vi } from 'vitest'
import Cookies from 'js-cookie'

describe('getAuthToken function', () => {
  it('returns the value of the auth_token cookie', () => {
    Cookies.get = vi.fn().mockReturnValue('test_auth_token')
    expect(getAuthToken()).toEqual('test_auth_token')
  })
})

describe('setAuthToken function', () => {
  it('sets the value of the auth_token cookie', () => {
    setAuthToken('test_auth_token')
    expect(getAuthToken()).toEqual('test_auth_token')
  })
})

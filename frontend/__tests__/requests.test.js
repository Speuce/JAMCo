import { postRequest, getCSRFToken } from '@/helpers/requests.js'
import { expect, describe, beforeEach, it, vi } from 'vitest'

import Cookies from 'js-cookie'

vi.mock('fetch')

describe('requests.js', () => {
  beforeEach(() => {
    Cookies.get = vi.fn().mockReturnValue('test_csrf_token')
    window.fetch = vi.fn()
  })

  it('sends a POST request to the backend', async () => {
    const mockData = { test: 'data' }
    const mockResponse = { status: 200, json: vi.fn().mockReturnValue({}) }
    fetch.mockReturnValue(Promise.resolve(mockResponse))

    await postRequest('/test', mockData)

    expect(fetch).toHaveBeenCalledWith('http://localhost:8000/test', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': 'test_csrf_token',
      },
      referrerPolicy: 'no-referrer-when-downgrade',
      body: JSON.stringify(mockData),
    })
  })

  it('throws an error if the response status is not 200', async () => {
    const mockData = { test: 'data' }
    const mockResponse = { status: 500, json: vi.fn().mockReturnValue({}) }
    fetch.mockReturnValue(Promise.resolve(mockResponse))
    expect(postRequest('/test', mockData)).rejects.toThrow(
      'Error sending post request'
    )
  })
})

describe('getCSRFToken function', () => {
  it('returns the value of the csrftoken cookie', () => {
    Cookies.get = vi.fn().mockReturnValue('test_csrf_token')

    expect(getCSRFToken()).toEqual('test_csrf_token')
  })
})

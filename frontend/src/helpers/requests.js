/* eslint-disable no-console */
import Cookies from 'js-cookie'

const prodMode = import.meta.env.PROD
const baseUrl = prodMode ? 'https://jamco.pro/' : 'http://localhost:8000/'
/**
 * Send a post request to the backend
 */
export async function postRequest(url, data) {
  // eslint-disable-next-line no-param-reassign
  if (url.startsWith('/')) url = url.substring(1)
  try {
    const response = await fetch(baseUrl + url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
      referrerPolicy: 'no-referrer-when-downgrade',
      body: JSON.stringify(data),
    })
    if (response.status !== 200) {
      console.error(response)
      throw new Error('Error sending post request')
    }
    return response.json()
  } catch (e) {
    console.error(e)
    throw new Error('Error sending post request')
  }
}

export function getCSRFToken() {
  const cookie = document.querySelector('[name=csrfmiddlewaretoken]').value
  if (cookie === undefined) {
    throw new Error('CSRF token not found')
  }
  return cookie
}

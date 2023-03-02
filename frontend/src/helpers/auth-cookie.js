import Cookies from 'js-cookie'

export function getAuthToken() {
  return Cookies.get('auth_token')
}

export function setAuthToken(token) {
  Cookies.remove('auth_token')
  Cookies.set('auth_token', token, { expires: 14 })
}

import { mount } from '@vue/test-utils'
import { expect, describe, it, afterEach } from 'vitest'
import AccountSetupModal from '../src/components/modal/setup/AccountSetupModal.vue'

describe('JobDetailModal', () => {
  let wrapper
  const user = {
    id: 12,
    first_name: 'First',
    last_name: 'Last',
    email: 'email@email',
    field_of_work: 'jobs',
    country: 'CA',
    region: 'MB',
    city: 'WPG',
    birthday: '12/12/1212',
  }

  function mountModal(userProp) {
    wrapper = mount(AccountSetupModal, {
      props: {
        user: userProp,
      },
    })
  }

  afterEach(() => {
    wrapper.vm.firstNameEmpty = false
    wrapper.vm.lastNameEmpty = false
    wrapper.vm.countryEmpty = false
    wrapper.vm.workFieldEmpty = false
    wrapper.vm.emailEmpty = false
  })

  it('populates with default values when no props provided', () => {
    mountModal()
    expect(wrapper.vm.userData).toEqual({
      id: -1,
      first_name: '',
      last_name: '',
      email: '',
      field_of_work: '',
      country: '',
      region: '',
      city: '',
      birthday: '',
    })
  })

  it('displays error when first name is empty & sign up is pressed', () => {
    expect(wrapper.vm.firstNameEmpty).toBe(false)

    let testJob = { ...user }
    testJob.first_name = null
    mountModal(testJob)

    wrapper.vm.signUpClicked()

    expect(wrapper.vm.firstNameEmpty).toBe(true)
  })

  it('displays error when last name is empty & sign up is pressed', () => {
    expect(wrapper.vm.lastNameEmpty).toBe(false)

    let testJob = { ...user }
    testJob.last_name = null
    mountModal(testJob)

    wrapper.vm.signUpClicked()

    expect(wrapper.vm.lastNameEmpty).toBe(true)
  })

  it('displays error when email is empty & sign up is pressed', () => {
    expect(wrapper.vm.emailEmpty).toBe(false)

    let testJob = { ...user }
    testJob.email = null
    mountModal(testJob)

    wrapper.vm.signUpClicked()

    expect(wrapper.vm.emailEmpty).toBe(true)
  })

  it('displays error when country is empty & sign up is pressed', () => {
    expect(wrapper.vm.countryEmpty).toBe(false)

    let testJob = { ...user }
    testJob.country = null
    mountModal(testJob)

    wrapper.vm.signUpClicked()

    expect(wrapper.vm.countryEmpty).toBe(true)
  })

  it('displays error when country is empty & sign up is pressed', () => {
    expect(wrapper.vm.workFieldEmpty).toBe(false)

    let testJob = { ...user }
    testJob.field_of_work = null
    mountModal(testJob)

    wrapper.vm.signUpClicked()

    expect(wrapper.vm.workFieldEmpty).toBe(true)
  })

  it('emits updateUser when sign up clicked', () => {
    mountModal(user)
    wrapper.vm.signUpClicked()

    expect(wrapper.emitted('updateUser')).toBeTruthy()
    expect(wrapper.emitted().updateUser[0][0]).toEqual({
      id: 12,
      first_name: 'First',
      last_name: 'Last',
      email: 'email@email',
      field_of_work: 'jobs',
      country: 'CA',
      region: 'MB',
      city: 'WPG',
      birthday: '12/12/1212',
    })
  })
})

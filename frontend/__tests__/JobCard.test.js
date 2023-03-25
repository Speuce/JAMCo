import { mount } from '@vue/test-utils'
import JobCard from '../src/components/kanban/JobCard.vue'
import stringToTriColourPalatte from '../src/helpers/string-to-tri-colour-palatte'
import { expect, describe, it } from 'vitest'

describe('JobCard', () => {
  let wrapper
  function mountJobCard(job) {
    wrapper = mount(JobCard, {
      props: { job },
    })
  }

  // Testing stringToTriColourPalatte from "assets/string-to-tri-colour-palatte"
  it('calculates the badge colours correctly for assorted strings', () => {
    let job = {}
    job = {
      type: 'TestOne',
      company: 'testing company united',
      position_title: 'long position title',
    }
    mountJobCard(job)

    let badgeColours = wrapper.vm.badgeColours
    let expectedColours = stringToTriColourPalatte(job.type)
    expect(badgeColours).toEqual(expectedColours)

    job = { type: '187325' }
    mountJobCard(job)

    badgeColours = wrapper.vm.badgeColours
    expectedColours = stringToTriColourPalatte(job.type)
    expect(badgeColours).toEqual(expectedColours)

    job = { type: 'l..//...,.-35936' }
    mountJobCard(job)

    badgeColours = wrapper.vm.badgeColours
    expectedColours = stringToTriColourPalatte(job.type)
    expect(badgeColours).toEqual(expectedColours)

    job = { type: '' }
    mountJobCard(job)

    badgeColours = wrapper.vm.badgeColours
    expectedColours = stringToTriColourPalatte(job.type)
    expect(badgeColours).toEqual(expectedColours)
  })
})

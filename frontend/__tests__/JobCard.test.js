import { mount } from '@vue/test-utils'
import JobCard from '../src/components/kanban/JobCard.vue'
import stringToTriColourPalatte from '../src/helpers/string-to-tri-colour-palatte'
import { expect, describe, it } from 'vitest'

describe('JobCard', () => {
  let wrapper
  let job = {}
  function mountJobCard(ajob) {
    wrapper = mount(JobCard, {
      props: { ajob },
    })
  }

  // Testing stringToTriColourPalatte from "assets/string-to-tri-colour-palatte"
  it('calculates the badge colours correctly for assorted strings', () => {
    job = { type: 'TestOne' }
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

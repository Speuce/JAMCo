import { mount } from '@vue/test-utils'
import CardBadge from '../src/components/kanban/CardBadge.vue'
import { expect, describe, it } from 'vitest'

describe('CardBadge', () => {
  it('uses default colours when none received', () => {
    const default_colours = ['#FFF', '#FFF', '#FFF']
    var wrapper = mount(CardBadge)
    expect(wrapper.props().colours).toEqual(default_colours)
  })

  it('uses passed colours when passed via props', async () => {
    const colours = ['#000', '#111', '#222']
    var wrapper = mount(CardBadge, {
      props: { colours },
    })
    await wrapper.setProps({ colours: colours })
    expect(wrapper.props().colours).toEqual(colours)
  })
})

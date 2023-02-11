import { mount } from '@vue/test-utils'
import ColumnCard from '../src/components/modal/column/ColumnCard.vue'
import { expect, describe, it, beforeEach } from 'vitest'

describe('ColumnCard', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(ColumnCard, {
      props: {
        column: {
          id: 0,
          name: 'colName',
          number: -1,
        },
      },
    })
  })

  it('emits updateColumn event when name changed', () => {
    wrapper
      .findComponent({ name: 'v-text-field' })
      .vm.$emit('change', { target: { _value: 'Test Input' } })
    expect(wrapper.emitted('updateColumn')).toBeTruthy()
    expect(wrapper.emitted().updateColumn[0][0]).toEqual({
      id: 0,
      name: 'Test Input',
      number: -1,
    })
  })

  it('emits deleteColumn when delete clicked', () => {
    wrapper.findComponent({ name: 'v-btn' }).trigger('click')
    expect(wrapper.emitted('deleteColumn')).toBeTruthy()
    expect(wrapper.emitted().deleteColumn[0][0]).toEqual(0)
  })
})

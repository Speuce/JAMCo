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

  it('emits updateColumn when column name changed', () => {
    console.log(wrapper ? 'expected' : '')
    expect(true).toBe(false)
  })
})

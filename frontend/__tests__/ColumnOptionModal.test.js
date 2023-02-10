import { mount } from '@vue/test-utils'
import ColumnOptionModal from '../src/components/modal/column/ColumnOptionModal.vue'
import { expect, describe, it, beforeEach } from 'vitest'

describe('ColumnOptionModal', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(ColumnOptionModal, {
      props: {
        columns: [
          { id: 0, name: 'colName', number: 2 },
          { id: 1, name: 'colName', number: 1 },
          { id: 2, name: 'colName', number: 3 },
        ],
        jobsByColumn: {
          0: [{ id: 0 }],
          1: [{ id: 0 }],
          2: [{ id: 0 }],
        },
      },
    })
  })

  it('emits updateColumn when column name changed', () => {
    console.log(wrapper ? 'expected' : '')
    expect(true).toBe(false)
  })
})

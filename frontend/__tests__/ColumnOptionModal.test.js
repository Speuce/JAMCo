import { mount } from '@vue/test-utils'
import ColumnOptionModal from '../src/components/modal/column/ColumnOptionModal.vue'
import ColumnCard from '../src/components/modal/column/ColumnCard.vue'
import { expect, describe, it, beforeEach, fail } from 'vitest'

describe('ColumnOptionModal', () => {
  let wrapper
  const columns = [
    { id: 0, name: 'colName', number: 2 },
    { id: 1, name: 'colName', number: 1 },
    { id: 2, name: 'colName', number: 3 },
  ]

  beforeEach(() => {
    wrapper = mount(ColumnOptionModal, {
      props: {
        columns,
        jobsByColumn: {
          0: [{ id: 0 }],
          1: [{ id: 0 }],
          2: [{ id: 0 }],
        },
      },
    })
  })

  it('emits updateColumn when saveClicked', () => {
    wrapper.vm.saveClicked()
    expect(wrapper.emitted('updateColumn')).toBeTruthy()
    expect(wrapper.emitted().updateColumn[0][0]).toEqual(columns)
  })

  it('deletes Column when deleteColumn event received', () => {
    wrapper.findComponent(ColumnCard).vm.$emit('deleteColumn', 0)
    expect(wrapper.vm.deleteColumn).toBeCalledWith(0)
  })

  it('does not deleteColumn if non-empty', () => {
    fail()
  })

  it('does not emit updateColumn when saved clicked with errors', () => {
    fail()
  })
})

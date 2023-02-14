import { mount } from '@vue/test-utils'
import ColumnOptionModal from '../src/components/modal/column/ColumnOptionModal.vue'
import { expect, describe, it } from 'vitest'

describe('ColumnOptionModal', () => {
  let wrapper
  const columns = [
    { id: 0, name: 'colName', number: 2 },
    { id: 1, name: 'colName', number: 1 },
    { id: 2, name: 'colName', number: 3 },
  ]

  const jobsByColumn = {
    0: [{ id: 0 }],
    1: [{ id: 0 }],
    2: [],
  }

  function mountModal(jobsByCol) {
    wrapper = mount(ColumnOptionModal, {
      props: {
        columns,
        jobsByColumn: jobsByCol,
      },
    })
  }

  it('emits updateColumns when saveClicked', () => {
    mountModal(jobsByColumn)
    wrapper.vm.saveClicked()
    expect(wrapper.emitted('updateColumns')).toBeTruthy()
    expect(wrapper.emitted().updateColumns[0][0]).toEqual(columns)
  })

  it('emits close when close button clicked', () => {
    mountModal(jobsByColumn)
    let buttons = wrapper.findAllComponents({ name: 'v-btn' })

    buttons.forEach((button) => {
      if (button.text() === 'Close') {
        button.trigger('click')
      }
    })

    expect(wrapper.emitted('close')).toBeTruthy()
  })

  it('deletes column if empty', () => {
    mountModal(jobsByColumn)
    expect(wrapper.vm.cols.length).toBe(3)
    wrapper.vm.deleteColumn(2)
    expect(wrapper.vm.unableToDeleteCol).toBe(false)
    expect(wrapper.vm.cols.length).toBe(2)
  })

  it('does not deleteColumn if non-empty', () => {
    mountModal(jobsByColumn)
    expect(wrapper.vm.cols.length).toBe(3)
    wrapper.vm.deleteColumn(0)
    expect(wrapper.vm.unableToDeleteCol).toBe(true)
    expect(wrapper.vm.cols.length).toBe(3)
  })

  it('sets invalidColumns to true if name empty', () => {
    mountModal(jobsByColumn)
    expect(wrapper.vm.invalidColumns).toBe(false)
    wrapper.vm.addColumn()
    wrapper.vm.saveClicked()
    expect(wrapper.vm.invalidColumns).toBe(true)
    expect(wrapper.emitted('close')).toBeFalsy()
  })

  it('updates column when passed', () => {
    mountModal(jobsByColumn)
    const updatedColumns = [
      { id: 0, name: 'newName', number: 0 },
      { id: 1, name: 'colName', number: 1 },
      { id: 2, name: 'colName', number: 2 },
    ]
    expect(wrapper.vm.cols).toEqual(columns)
    wrapper.vm.updateColumn({ id: 0, name: 'newName', number: 0 })
    expect(wrapper.vm.cols).toEqual(updatedColumns)
  })

  it('limits number of columns to 8', () => {
    mountModal(jobsByColumn)
    expect(wrapper.vm.maxColumnsReached).toBe(false)
    expect(wrapper.vm.cols.length).toBe(3)
    wrapper.vm.addColumn()
    wrapper.vm.addColumn()
    wrapper.vm.addColumn()
    wrapper.vm.addColumn()
    wrapper.vm.addColumn()
    expect(wrapper.vm.maxColumnsReached).toBe(false)
    wrapper.vm.addColumn()
    expect(wrapper.vm.maxColumnsReached).toBe(true)
    expect(wrapper.vm.cols.length).toBe(8)
  })

  it('requires minimum of 1 column', () => {
    const jobsByCol = {
      0: [],
      1: [],
      2: [],
    }
    mountModal(jobsByCol)

    expect(wrapper.vm.minColumnsReached).toBe(false)
    wrapper.vm.deleteColumn(0)
    wrapper.vm.deleteColumn(1)
    expect(wrapper.vm.minColumnsReached).toBe(false)
    wrapper.vm.deleteColumn(2)
    expect(wrapper.vm.minColumnsReached).toBe(true)
    expect(wrapper.vm.cols.length).toBe(1)
  })
})

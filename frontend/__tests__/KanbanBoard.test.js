import { mount } from "@vue/test-utils";
import { VueDraggableNext } from "vue-draggable-next";
import KanbanBoard from "../src/components/kanban/KanbanBoard.vue";
import JobCard from "../src/components/kanban/JobCard.vue";
import { expect, beforeEach, describe, it } from "vitest";
import testColumnMapping from "./test_data/test_column_mapping.json";
import testJobs from "./test_data/test_jobs.json";

describe("KanbanBoard", () => {
  let wrapper;

  beforeEach(async () => {
    wrapper = mount(KanbanBoard);
    await wrapper.setData({
      jobs: wrapper.vm.processJobsByColumn(testJobs),
      columns: testColumnMapping,
    });
  });

  it("has the correct number of columns", () => {
    const columns = wrapper.findAll(".column-width");
    expect(columns.length).toBe(Object.keys(testColumnMapping).length);
  });

  it("updates the column of a job when it is moved", () => {
    var column = wrapper.findAllComponents(VueDraggableNext);
    var job = wrapper.findComponent(JobCard);
    expect(job.vm.job.columnId).toBe(1);

    column[1].vm.$emit("change", { added: { element: job.vm.job } }, 2);
    expect(job.vm.job.columnId).toBe(2);
  });
});

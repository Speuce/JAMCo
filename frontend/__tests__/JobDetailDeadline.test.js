import { mount } from "@vue/test-utils";
import JobDetailDeadline from "../src/components/modal/job/JobDetailDeadline.vue";
import { expect, beforeEach, describe, it, vi } from "vitest";
import Datepicker from "@vuepic/vue-datepicker";

describe("JobDetailDeadline", () => {
  let wrapper;
  let deleteDeadline = vi.fn();
  let deadline = {
    id: 1,
    title: "testTitle",
    date: "12/12/1212",
  };

  beforeEach(async () => {
    wrapper = mount(JobDetailDeadline, {
      props: {
        deadline,
        deleteDeadline,
      },
    });
  });

  it("emits updateDeadline when datePicker updated", () => {
    wrapper
      .findComponent(Datepicker)
      .vm.$emit("update:model-value", "01/01/2023");
    expect(wrapper.emitted("updateDeadline")).toBeTruthy();
    expect(wrapper.emitted().updateDeadline[0][0].id).toEqual(1);
    expect(wrapper.emitted().updateDeadline[0][0].title).toEqual("testTitle");
    expect(wrapper.emitted().updateDeadline[0][0].date).toEqual("01/01/2023");
  });

  it("emits updateDeadline when datePicker cleared", () => {
    wrapper.findComponent(Datepicker).vm.$emit("update:model-value", null);
    expect(wrapper.emitted("updateDeadline")).toBeTruthy();
    expect(wrapper.emitted().updateDeadline[0][0].id).toEqual(1);
    expect(wrapper.emitted().updateDeadline[0][0].title).toEqual("testTitle");
    expect(wrapper.emitted().updateDeadline[0][0].date).toEqual(null);
  });

  it("emits updateDeadline event when title changed", () => {
    wrapper
      .findComponent({ name: "v-text-field" })
      .vm.$emit("change", { target: { value: "Test Input" } });
    expect(wrapper.emitted("updateDeadline")).toBeTruthy();
  });

  it("calls deleteDeadline when the remove button is clicked", () => {
    wrapper.findComponent({ name: "v-btn" }).trigger("click");
    expect(wrapper.vm.deleteDeadline).toHaveBeenCalledWith(1);
  });

  it("populates deadlineModel with props", () => {
    expect(wrapper.vm.deadlineModel).toEqual(deadline);
  });
});

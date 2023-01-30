import { mount } from "@vue/test-utils";
import JobCard from "../src/components/kanban/JobCard.vue";
import stringToTriColourPalatte from "../src/assets/string-to-tri-colour-palatte";
import { expect, describe, it } from "vitest";

describe("JobCard", () => {
  var wrapper;
  var job = {};
  function mountJobCard(job) {
    wrapper = mount(JobCard, {
      propsData: { job },
    });
  }

  // Testing stringToTriColourPalatte from "assets/string-to-tri-colour-palatte"
  it("calculates the badge colours correctly for assorted strings", () => {
    job = { type: "TestOne" };
    mountJobCard(job);

    var badgeColours = wrapper.vm.badgeColours;
    var expectedColours = stringToTriColourPalatte(job.type);
    expect(badgeColours).toEqual(expectedColours);

    job = { type: "187325" };
    mountJobCard(job);

    badgeColours = wrapper.vm.badgeColours;
    expectedColours = stringToTriColourPalatte(job.type);
    expect(badgeColours).toEqual(expectedColours);

    job = { type: "l..//...,.-35936" };
    mountJobCard(job);

    badgeColours = wrapper.vm.badgeColours;
    expectedColours = stringToTriColourPalatte(job.type);
    expect(badgeColours).toEqual(expectedColours);

    job = { type: "" };
    mountJobCard(job);

    badgeColours = wrapper.vm.badgeColours;
    expectedColours = stringToTriColourPalatte(job.type);
    expect(badgeColours).toEqual(expectedColours);
  });
});

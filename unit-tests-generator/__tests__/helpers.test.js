import { sum } from "../src/utils/helpers";

describe("sum function", () => {
  it("correctly adds two positive numbers", () => {
    expect(sum(2, 3)).toBe(5);
    expect(sum(10, 5)).toBe(15);
  });

  it("correctly adds two negative numbers", () => {
    expect(sum(-2, -3)).toBe(-5);
    expect(sum(-10, -5)).toBe(-15);
  });

  it("correctly adds a positive and a negative number", () => {
    expect(sum(2, -3)).toBe(-1);
    expect(sum(-10, 5)).toBe(-5);
  });

  it("correctly adds zero to a number", () => {
    expect(sum(0, 5)).toBe(5);
    expect(sum(10, 0)).toBe(10);
    expect(sum(0, 0)).toBe(0);
  });

  it("handles decimal numbers correctly", () => {
    expect(sum(1.5, 2.5)).toBe(4);
    expect(sum(-1.5, 2.5)).toBe(1);
  });
});

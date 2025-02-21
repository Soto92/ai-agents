import React from "react";
import { render, fireEvent } from "@testing-library/react-native";
import Button from "../src/components/Button";

describe("Button Component", () => {
  it("renders correctly", () => {
    const { getByText } = render(
      <Button title="Click Me" onPress={() => {}} />
    );
    expect(getByText("Click Me")).toBeTruthy();
  });

  it("calls onPress when pressed", () => {
    const onPressMock = jest.fn();
    const { getByText } = render(
      <Button title="Click Me" onPress={onPressMock} />
    );
    fireEvent.press(getByText("Click Me"));
    expect(onPressMock).toHaveBeenCalled();
  });

  it("applies correct styles", () => {
    const { getByTestId } = render(
      <Button title="Click Me" onPress={() => {}} />
    );
    const button = getByTestId("button");
    expect(button.props.style.backgroundColor).toBe("blue");
    expect(button.props.style.padding).toBe(10);
    expect(button.props.style.borderRadius).toBe(5);
  });
});

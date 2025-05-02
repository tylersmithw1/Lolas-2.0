import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import SearchBar from "../../components/SearchBar"; // Adjust path as needed

import React from "react"; // Make sure React is imported

describe("SearchBar", () => {
  it("renders correctly with initial empty state", () => {
    render(React.createElement(SearchBar, { onSearch: () => {} }));

    const inputElement = screen.getByPlaceholderText("Search for groceries...");
    const buttonElement = screen.getByText("Search");

    expect(inputElement).toBeInTheDocument();
    expect(buttonElement).toBeInTheDocument();
    expect(inputElement.value).toBe("");
  });

  it("updates input value when typing", () => {
    render(React.createElement(SearchBar, { onSearch: () => {} }));

    const inputElement = screen.getByPlaceholderText("Search for groceries...");

    fireEvent.change(inputElement, { target: { value: "apples" } });

    expect(inputElement.value).toBe("apples");
  });

  it("calls onSearch with query when search button is clicked", () => {
    const mockOnSearch = vi.fn();
    render(React.createElement(SearchBar, { onSearch: mockOnSearch }));

    const inputElement = screen.getByPlaceholderText("Search for groceries...");
    const buttonElement = screen.getByText("Search");

    fireEvent.change(inputElement, { target: { value: "bananas" } });
    fireEvent.click(buttonElement);

    expect(mockOnSearch).toHaveBeenCalledTimes(1);
    expect(mockOnSearch).toHaveBeenCalledWith("bananas");
  });

  it("does not call onSearch when search query is empty", () => {
    const mockOnSearch = vi.fn();
    render(React.createElement(SearchBar, { onSearch: mockOnSearch }));

    const buttonElement = screen.getByText("Search");

    fireEvent.click(buttonElement);

    expect(mockOnSearch).not.toHaveBeenCalled();
  });

  it("does not call onSearch when search query contains only whitespace", () => {
    const mockOnSearch = vi.fn();
    render(React.createElement(SearchBar, { onSearch: mockOnSearch }));

    const inputElement = screen.getByPlaceholderText("Search for groceries...");
    const buttonElement = screen.getByText("Search");

    fireEvent.change(inputElement, { target: { value: "   " } });
    fireEvent.click(buttonElement);

    expect(mockOnSearch).not.toHaveBeenCalled();
  });
});

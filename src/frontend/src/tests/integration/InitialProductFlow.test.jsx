import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import Home from "/Users/dikamanne/Lolas-2.0-1/src/frontend/src/pages/Home.jsx";
import { describe, it, vi, expect } from "vitest";

describe("Home page integration", () => {
  it("should render a product and allow clicking on it", async () => {
    // Mock fetch globally
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        products: [
          {
            product: "Banana",
            image: "banana.jpg",
            price: 0.99,
            energykcal: 90,
            protein: 1,
            fibre: 3,
            servingsize: "1 medium",
            carbohydrates: 23,
            fat: 0.3,
            sugar: 12,
            salt: 1,
          },
        ],
      }),
    });

    render(
      <MemoryRouter>
        <Home />
      </MemoryRouter>
    );

    // Simulate search
    fireEvent.change(screen.getByPlaceholderText("Search products..."), {
      target: { value: "Banana" },
    });

    // Get all buttons and find the submit button (type="submit")
    const buttons = screen.getAllByRole('button');
    const submitButton = buttons.find((btn) => btn.type === 'submit');
    fireEvent.click(submitButton);  // Click the search submit button

    // Wait for product to appear
    await waitFor(() => {
      expect(screen.getByText("Banana")).toBeInTheDocument();
    });

    // Click the card (via image alt text)
    const image = screen.getByAltText("Banana");
    fireEvent.click(image);

    
  });
});

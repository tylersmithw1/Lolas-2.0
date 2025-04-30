import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import ProductDetail from "/Users/dikamanne/Lolas-2.0-1/src/frontend/src/pages/ProductDetail.jsx";
import { describe, it, vi, expect } from "vitest";


const mockProduct = {
  name: 'Test Product',
  brand: 'Mock Brand',
  price: 5.99,
};

beforeEach(() => {
  global.fetch = vi.fn((url) => {
    if (typeof url === 'string' && url.includes('/recommendations')) {
      return Promise.resolve({
        ok: true,
        json: () =>
          Promise.resolve({
            products: [
              { product: 'Apple Juice', brand: 'Juicy Brand', price: 2.5 },
              { product: 'Orange Juice', brand: 'Fresh Co', price: 3.2 },
            ],
          }),
      });
    }

    if (typeof url === 'string' && url.includes('/ai-recommendations')) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ products: [] }),
      });
    }

    if (typeof url === 'string' && url.includes('/product-detail')) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ name: 'Test Product' }),
      });
    }

    return Promise.reject(new Error('Unknown API'));
  });
});

afterEach(() => {
  vi.restoreAllMocks();
});

test('displays recommended products from API', async () => {
  render(
    <MemoryRouter initialEntries={['/product/123']}>
      <Routes>
        <Route path="/product/:id" element={<ProductDetail />} />
      </Routes>
    </MemoryRouter>
  );

  await waitFor(() => {
    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('/recommendations'),
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({
          product_name: 'Test Product',
          column_name: 'sugar',
        }),
      })
    );
  });

  await waitFor(() => {
    expect(screen.getByText(/Apple Juice/i)).toBeInTheDocument();
    expect(screen.getByText(/Orange Juice/i)).toBeInTheDocument();
  });
});

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ProductCard from '../../components/ProductCard'; // Adjust path as needed
import React from 'react';

// Create a mock navigate function
const mockNavigate = vi.fn();
vi.mock('react-router-dom', () => ({
  ...vi.importActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

// Mock the react-router-dom dependency
vi.mock('react-router-dom', () => ({
  useNavigate: () => mockNavigate
}));

// Mock the Material UI components
vi.mock('@mui/material', () => ({
  Card: function Card(props) {
    return React.createElement('div', { 'data-testid': 'card' }, props.children);
  },
  CardActionArea: function CardActionArea(props) {
    return React.createElement('div', { 'data-testid': 'card-action-area', onClick: props.onClick }, props.children);
  },
  CardContent: function CardContent(props) {
    return React.createElement('div', { 'data-testid': 'card-content' }, props.children);
  },
  CardMedia: function CardMedia(props) {
    return React.createElement('img', { 'data-testid': 'card-media', src: props.image, alt: props.alt });
  },
  Typography: function Typography(props) {
    return React.createElement('div', { 'data-testid': 'typography' }, props.children);
  },
  Box: function Box(props) {
    return React.createElement('div', { 'data-testid': 'box' }, props.children);
  },
  IconButton: function IconButton(props) {
    return React.createElement('button', { 'data-testid': 'icon-button', onClick: props.onClick }, props.children);
  }
}));

// Mock the Material UI icons
vi.mock('@mui/icons-material/Add', () => ({
  default: function AddIcon() {
    return React.createElement('span', { 'data-testid': 'add-icon' }, '+');
  }
}));

describe('ProductCard', () => {
  const mockProps = {
    name: 'Test Product',
    price: 9.99,
    image: '/test-image.jpg',
    healthRating: 3
  };
  
  beforeEach(() => {
    // Reset the mock before each test
    mockNavigate.mockReset();
  });
  
  it('renders the product card with correct information', () => {
    render(React.createElement(ProductCard, mockProps));
    
    // Check if the image is displayed correctly
    const image = screen.getByTestId('card-media');
    expect(image).toHaveAttribute('src', mockProps.image);
    expect(image).toHaveAttribute('alt', mockProps.name);
    
    // Check if the product name is displayed
    const content = screen.getByTestId('card-content');
    expect(content.textContent).toContain(mockProps.name);
    
    // Check if the price is formatted correctly
    expect(content.textContent).toContain('$9.99');
  });
  
  it('formats price correctly with two decimal places', () => {
    const propsWithOddPrice = { ...mockProps, price: 10.5 };
    render(React.createElement(ProductCard, propsWithOddPrice));
    
    const content = screen.getByTestId('card-content');
    expect(content.textContent).toContain('$10.50');
  });
  
  it('handles zero or undefined price correctly', () => {
    // Test with price = 0
    const propsWithZeroPrice = { ...mockProps, price: 0 };
    const { rerender } = render(React.createElement(ProductCard, propsWithZeroPrice));
    
    let content = screen.getByTestId('card-content');
    expect(content.textContent).toContain('$0.00');
    
    // Test with undefined price
    const propsWithoutPrice = { ...mockProps, price: undefined };
    rerender(React.createElement(ProductCard, propsWithoutPrice));
    
    content = screen.getByTestId('card-content');
    expect(content.textContent).toContain('$0.00');
  });
  
 
  it('calls onClick when the card is clicked to details page', async () => {
    const mockOnClick = vi.fn();
    const propsWithClick = { ...mockProps, onClick: mockOnClick };
    render(React.createElement(ProductCard, propsWithClick));
  
    const user = userEvent.setup();
    const card = screen.getByTestId('card-action-area');
  
    await user.click(card);
  
    expect(mockOnClick).toHaveBeenCalledTimes(1);
  });
  
  
  it('renders health rating indicators', () => {
    render(React.createElement(ProductCard, mockProps));
    
    // The health rating function should render 5 dots
    const boxes = screen.getAllByTestId('box');
    // First box is the container, then we have 5 dots inside
    expect(boxes.length).toBeGreaterThanOrEqual(5);
  });
});
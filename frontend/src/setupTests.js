// frontend/src/setupTests.js
// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';

// frontend/src/App.test.js
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders login screen when not authenticated', () => {
  render(<App />);
  const loginElement = screen.getByText(/Kirana ERP/i);
  expect(loginElement).toBeInTheDocument();
});
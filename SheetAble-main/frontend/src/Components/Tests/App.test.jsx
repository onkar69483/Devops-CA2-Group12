import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../../App';

test('renders the Login title and submit button', () => {
  render(<App />);
  
  // Check for the Login title text
  const loginTitle = screen.getByText(/login/i);
  expect(loginTitle).toBeInTheDocument();

  // Check for submit button with value="Login"
  const loginButton = screen.getByDisplayValue(/login/i);
  expect(loginButton).toBeInTheDocument();
});

// new changes 
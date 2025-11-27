import { test, expect } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from '../App'

test('mock sign-in flow shows profile after clicking sign in', async () => {
  const user = userEvent.setup()
  render(<App />)

  const signInLink = screen.getByRole('link', { name: /sign in with github/i })
  expect(signInLink).toBeTruthy()

  await user.click(signInLink)

  // loading state should show
  expect(screen.getByText(/signing in.../i)).toBeTruthy()

  // wait for the mock sign-in delay (700ms) and then body should show the mock profile name
  await waitFor(() => {
    expect(screen.getByText(/Ahn Afab/)).toBeTruthy()
  }, { timeout: 2000 })
})

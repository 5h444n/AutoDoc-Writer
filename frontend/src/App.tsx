import './App.css'
import { useState } from 'react'
import type { MouseEvent } from 'react'

function App() {
  // Read Vite environment variables (set VITE_GITHUB_CLIENT_ID and VITE_GITHUB_REDIRECT_URI if you want the button to redirect directly to GitHub)
  const env = (import.meta as unknown as { env?: Record<string, string | undefined> }).env || {}
  const clientId = env.VITE_GITHUB_CLIENT_ID || ''
  const redirectUri = env.VITE_GITHUB_REDIRECT_URI || `${window.location.origin}/auth/callback`

  // Build base authorize URL (we'll append a per-request state when navigating)
  const baseAuthorizeHref = clientId
    ? `https://github.com/login/oauth/authorize?${new URLSearchParams({ client_id: clientId, redirect_uri: redirectUri, scope: 'read:user user:email' })}`
    : '#'

  const ariaDisabled = clientId ? undefined : 'true'

  // Save state to sessionStorage and navigate to GitHub when clientId is present.
  // The onClick handler runs before navigation, so generate state here (not during render) to satisfy lint rules.
  const handleSignIn = (e: MouseEvent<HTMLAnchorElement>) => {
    if (!clientId) {
      e.preventDefault()
      mockSignIn()
      return
    }

    // generate a random state for the OAuth request (best-effort; must be validated on callback to be secure)
    const state = (typeof crypto !== 'undefined' && 'randomUUID' in crypto)
      ? (crypto as any).randomUUID()
      : Math.random().toString(36).slice(2)

    try {
      sessionStorage.setItem('oauth_state', state)
    } catch {
      // ignore storage errors (no binding to avoid lint warnings)
    }

    // programmatically navigate so the state we just stored is in sync with the redirect
    const separator = baseAuthorizeHref.includes('?') ? '&' : '?'
    window.location.href = `${baseAuthorizeHref}${separator}state=${encodeURIComponent(state)}`
  }

  // --- Mock auth client-side state (no backend) ---
  type User = {
    id: number
    name: string
    login: string
    avatar_url: string
    bio?: string
    email?: string
  }

  const mockUser: User = {
    id: 1,
    name: 'Ahn Afab',
    login: 'ahnafabidshan',
    avatar_url: 'https://avatars.githubusercontent.com/u/9919?s=200&v=4',
    bio: 'Frontend tinkerer • Building AutoDoc',
    email: 'ahnafab@example.com'
  }

  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(false)

  const mockSignIn = () => {
    setLoading(true)
    // simulate network delay
    setTimeout(() => {
      setUser(mockUser)
      setLoading(false)
    }, 700)
  }

  const signOut = () => {
    setUser(null)
  }

  // --- Render ---
  if (user) {
    // Minimal profile / dashboard after mock sign-in
    return (
      <div className="login-root">
        <div className="login-card profile-card">
          <div className="profile-top">
            <img src={user.avatar_url} alt={`${user.name} avatar`} className="profile-avatar" />
            <div className="profile-meta">
              <h2 className="profile-name">{user.name}</h2>
              <p className="profile-login">@{user.login}</p>
            </div>
          </div>
          <p className="profile-bio">{user.bio}</p>
          <div className="profile-actions">
            <a className="github-btn secondary" href="#" onClick={(e) => { e.preventDefault(); signOut() }}>
              Sign out
            </a>
            <a className="github-btn" href={baseAuthorizeHref} aria-disabled={ariaDisabled} onClick={handleSignIn}>
              Manage GitHub Connection
            </a>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="login-root">
      <div className="login-card">
        <h1 className="login-title">AutoDoc</h1>
        <p className="login-sub">Sign in to continue</p>

        <a href={baseAuthorizeHref} className="github-btn" aria-label="Sign in with GitHub" aria-disabled={ariaDisabled} onClick={handleSignIn}>
          <svg className="github-logo" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
            <path fill="currentColor" d="M12 .297a12 12 0 00-3.79 23.4c.6.11.82-.26.82-.58v-2.1c-3.34.73-4.04-1.6-4.04-1.6-.55-1.4-1.35-1.77-1.35-1.77-1.1-.75.08-.74.08-.74 1.22.09 1.86 1.25 1.86 1.25 1.08 1.85 2.83 1.31 3.52 1 .11-.78.42-1.31.76-1.61-2.66-.3-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.12-.3-.54-1.52.12-3.17 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 016 0c2.28-1.55 3.29-1.23 3.29-1.23.66 1.65.24 2.87.12 3.17.77.84 1.24 1.91 1.24 3.22 0 4.61-2.82 5.62-5.5 5.92.43.37.81 1.1.81 2.22v3.29c0 .32.22.69.82.57A12 12 0 0012 .297z" />
          </svg>
          <span>{loading ? 'Signing in...' : 'Sign in with GitHub'}</span>
        </a>

        {!clientId && (
          <p className="login-note">No GitHub app configured — this demo uses a mock sign-in to preview the UI.</p>
        )}

        {clientId && (
          <p className="login-note">You will be redirected to GitHub to authorize the app.</p>
        )}
      </div>
    </div>
  )
}

export default App

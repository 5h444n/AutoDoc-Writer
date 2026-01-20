# Manual Testing Guide (QA Protocol)

This guide provides step-by-step instructions for manually verifying all user-facing features of the AutoDoc-Writer application. Use this to ensure the frontend and backend are correctly integrated.

---

## 🛠️ Prerequisites

Before testing, ensure the full stack is running locally:

1.  **Backend** (`Port 8000`):
    ```bash
    cd backend
    source .venv/bin/activate  # or .venv\Scripts\activate on Windows
    python -m uvicorn app.main:app --reload
    ```
    *Verify*: Visit `http://localhost:8000/docs`. You should see the Swagger UI.

2.  **Frontend** (`Port 5173`):
    ```bash
    cd frontend
    npm run dev
    ```
    *Verify*: Visit `http://localhost:5173`. You should see the Login Page.

---

## 🧪 Test Case 1: Authentication Flow

**Objective**: Verify that a user can log in via GitHub and a session is created.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open `http://localhost:5173`. | You see the "AutoDoc Writer" login card with specific background animations. |
| 2 | Click **"Continue with GitHub"**. | Browser redirects to `github.com/login/oauth/...`. |
| 3 | Authorize the application (if prompted). | Browser redirects back to backend, then to `http://localhost:5173/auth/callback`, and finally to `/dashboard`. |
| 4 | Check **Developer Tools** (F12) -> **Application** -> **Local Storage**. | Keys `auth_token` and `username` should exist. |
| 5 | Verify URL. | Current URL should be `http://localhost:5173/dashboard`. |

---

## 🧪 Test Case 2: Repository Management (Dashboard)

**Objective**: Verify that repositories are fetched from GitHub/DB and can be interacted with.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Navigate to `/dashboard` (Home). | A grid of repository cards should appear. If it says "No repositories connected", your GitHub account has no public repos or sync failed. |
| 2 | Look for the **"Branch: main"** and **"Updated"** date on a card. | Data should be formatted correctly (e.g., "1/20/2026"). |
| 3 | Click the **External Link Icon** (top right of card). | Opens the actual GitHub repository in a new tab. |
| 4 | **Test Toggle**: Click the **Power Button** on a repository card. | - **UI**: The status pill changes from "Inactive" (Grey) to "Monitored" (Green). <br> - **Network**: A `PATCH` request to `/api/v1/repos/{name}/toggle` returns `200 OK`. |
| 5 | Refresh the page (`F5`). | The repository you toggled should **remain** in the state you left it (Persistence check). |

---

## 🧪 Test Case 3: AI Playground

**Objective**: Verify the Gemini AI integration for generating documentation.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Click **"AI Playground"** (Sparkles icon) in the Sidebar. | Navigates to `/dashboard/playground`. |
| 2 | In the **Source Code** text area, paste a code snippet: <br>`def add(a, b): return a + b` | Text area accepts input. |
| 3 | Leave **Style** as "Standard Style". | Dropdown value is selected. |
| 4 | Click **"Generate Documentation"**. | - Button shows loading spinner. <br> - After 1-3s, text appears in the right panel. |
| 5 | Verify Output. | The output should explain the function (e.g., "This function calculates the sum of two numbers..."). |
| 6 | Change **Style** to **"Mathematical (LaTeX)"**. | Dropdown updates. |
| 7 | Click **Generate** again. | The output should look mathematical (e.g., $f(a,b) = a + b$). |
| 8 | **Error Case**: Clear input and click Generate. | Should nothing happen or show a validation warning (if implemented) or handle gracefully. |

---

## 🧪 Test Case 4: Settings & Logout

**Objective**: Verify user profile display and session termination.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Click **"Settings"** in the Sidebar. | Navigates to `/dashboard/settings`. |
| 2 | Verify Profile Info. | Should show your GitHub Username and a capitalized initial in the avatar. Should show "Authenticated" badge. |
| 3 | Click the **"Disconnect & Logout"** button. | - LocalStorage is cleared (`auth_token` removed). <br> - User is redirected immediately to the Login Page (`/`). |
| 4 | Try to manually go to `/dashboard`. | Application should redirect you back to `/` (Protected Route check). |

---

## 🐛 Troubleshooting Common Issues

**1. Login Logic Redirects Infinite Loop:**
*   *Cause*: `auth_token` is invalid or backend rejects it.
*   *Fix*: clear LocalStorage manually and try again.

**2. "Failed to fetch repositories" (Network Error):**
*   *Cause*: Backend is not running or CORS is blocking the request.
*   *Fix*: Ensure backend is on `localhost:8000`. Check `backend/main.py` CORS settings.

**3. AI Playground Errors ("Server Error"):**
*   *Cause*: `GEMINI_API_KEY` is missing or invalid in `.env`.
*   *Fix*: detailed in `backend/app/api/v1/endpoints/ai.py` logs.

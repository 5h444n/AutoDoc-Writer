# How We Made It

AutoDoc Writer is built using a hybrid desktop-web architecture to ensure privacy, speed, and offline capability.

## Technical Architecture

### 1. Application Shell: Electron
We used **Electron (Node.js)** to wrap the application as a native desktop experience. This allows the app to have full system access (file system, notifications) while using standard web technologies for the interface.

### 2. Frontend (User Interface)
* **Framework:** React + TypeScript
* **Styling:** Tailwind CSS
* **Role:** The frontend manages the visible dashboard, state management (e.g., active/inactive repositories), and the documentation viewer. It communicates with the local Python backend via API calls.

### 3. Backend (Logic Core)
* **Framework:** Python (FastAPI)
* **Role:** Acts as the brain of the application running locally on the user's machine. It handles:
    * **GitHub API:** Fetching repositories and reading commit diffs using `PyGithub`.
    * **AI Processing:** Sending code chunks to the Google Gemini AI model to generate explanations and LaTeX code.
    * **Templating:** Using `jinja2` to format the academic outputs.

### 4. Database & Storage
* **Database:** SQLite (via SQLAlchemy)
* **Role:** We use a local SQLite database to cache generated documentation.
    * **Offline Access:** Users can view past docs without internet.
    * **Efficiency:** Prevents re-generating text for the same commit ID twice, saving API usage.

## Security & Privacy
* **OAuth 2.0:** We use GitHub OAuth for secure login, ensuring the app never sees or stores the user's password.
* **Local Processing:** All data is processed and stored locally on the user's machine, not on external servers.
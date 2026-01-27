# How to Run AutoDoc Writer

This guide details the complete setup process for running AutoDoc Writer on your local machine. Because this is a hybrid application, you must set up two distinct environments: the **Python Backend** (for logic) and the **Electron Frontend** (for the UI).

## 1. Prerequisites
Before installing, ensure your system has the following core tools installed:

* **Node.js & npm (Latest LTS)**: Required to run the **Electron Application Shell** and the React frontend.
* **Python 3.8 or higher**: Required to run the **FastAPI Backend**, which handles the AI logic and database interactions.
* **Git**: Necessary to download the source code from GitHub.

---

## 2. Cloning the Repository
The first step is to download the project codebase to your local machine.

### Run the Clone Command
Open your terminal (Command Prompt, PowerShell, or Mac Terminal) and navigate to the folder where you want to store the project. Run the following commands:

```bash
# Download the latest version of the code
git clone [https://github.com/5h444n/AutoDoc-Writer.git](https://github.com/5h444n/AutoDoc-Writer.git)
```
# Enter the project directory
cd AutoDoc-Writer


### Verify the Installation

After entering the directory, verify the download was successful by listing the files (type `ls` or `dir` in your terminal). You must see these two main subfolders:

* `backend/`: Contains the Python logic and AI scripts.
* `frontend/`: Contains the React and Electron user interface code.

If you see these folders, you are ready to proceed.

---

## 3. Backend Setup (The Logic Core)

The backend runs locally to handle GitHub connections and AI processing.

**1. Navigate to the backend folder:**

```bash
cd backend

```

**2. Create a Virtual Environment:**
Isolate your Python dependencies to avoid conflicts.

```bash
# Create the environment
python -m venv venv

# Activate it (Windows):
.\venv\Scripts\activate

# Activate it (Mac/Linux):
source venv/bin/activate

```

**3. Install Dependencies:**
Install the required libraries, including `fastapi`, `pygithub`, and `google-generativeai`.

```bash
pip install -r requirements.txt

```

**4. Configure API Keys:**
You need an API key for the AI features to work.

* Create a file named `.env` inside the `backend` folder.
* Add your keys (Google Gemini or OpenAI):

```env
GOOGLE_API_KEY=your_gemini_api_key_here
GITHUB_TOKEN=your_personal_access_token_optional

```

**5. Start the Server:**
Launch the local API server. **Keep this terminal window open.**

```bash
uvicorn main:app --reload

```

*You should see a message saying the server is running at `http://127.0.0.1:8000`.*

---

## 4. Frontend Setup (The User Interface)

The frontend is the desktop window you interact with.

**1. Open a NEW terminal window.**
Do not close the Python terminal!

**2. Navigate to the frontend folder:**

```bash
cd frontend

```

**3. Install Node Modules:**
This downloads all the UI libraries like React and Tailwind CSS.

```bash
npm install

```

**4. Launch the Application:**
This starts the Electron window.

```bash
npm start

```

---

## 5. Troubleshooting

* **"API Key Not Found":** Check that your `.env` file exists in the `backend` folder and contains `GOOGLE_API_KEY`.
* **Window is White/Empty:** Ensure the Python backend is running. The frontend needs the backend to fetch data.


### **Step 3: Fix the 404 Error**

The **404 Not Found** error in your first screenshot happens because MkDocs cannot find the file `docs/setup.md`.

**To fix it:**
1.  Go to your `AutoDoc-Writer/documentation/docs` folder.
2.  Make sure you have created a **new file** named `setup.md`.
3.  Paste the code from **Step 2** above into it.
4.  Do the same for `usage.md`.

Once you save these files, the 404 error will disappear instantly.

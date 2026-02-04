<div align="center">

# 📝 AutoDoc Writer

### **Turn Your Code Into Documentation—Automatically**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6.svg)](https://www.typescriptlang.org/)
[![Electron](https://img.shields.io/badge/Electron-Latest-47848F.svg)](https://www.electronjs.org/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-AI-4285F4.svg)](https://ai.google.dev/)

**Say goodbye to manual documentation.** AutoDoc Writer connects to your GitHub, detects code changes, and generates professional writeups—from plain English explanations to LaTeX-ready academic content.

[✨ Features](#-features) • [🚀 Quick Start](#-quick-start) • [📖 Usage Guide](#-usage-guide) • [🏗️ Architecture](#%EF%B8%8F-architecture) • [🗺️ Roadmap](#%EF%B8%8F-roadmap)

---

</div>

## 📋 Table of Contents

- [The Problem](#-the-problem)
- [The Solution](#-the-solution)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Architecture](#%EF%B8%8F-architecture)
- [Roadmap](#%EF%B8%8F-roadmap)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## 🎯 The Problem

Students and developers often struggle to create proper documentation for their software projects.

| Challenge | Impact |
|-----------|--------|
| **📚 Student Struggles** | Over **65%** of computer science students say writing documentation is harder than writing code |
| **⏰ Industry Reality** | Software engineers spend around **25-30%** of their time just writing documentation |
| **🔧 Tool Limitation** | Most existing tools are too technical or generate only simple comments—not formal reports or LaTeX content |
| **⏱️ Deadline Pressure** | Becomes critical during assignments, thesis submissions, or project reviews when time is limited |

---

## 💡 The Solution

**AutoDoc Writer** is a powerful desktop application that solves documentation pain points by connecting directly to your GitHub account.

### How It Works

```
┌─────────────────┐         ┌──────────────────┐         ┌────────────────────┐
│   Push Code     │ ──────▶ │  Auto-Detect     │ ──────▶ │   Generate Docs    │
│   to GitHub     │         │  Changes         │         │   Automatically    │
└─────────────────┘         └──────────────────┘         └────────────────────┘
                                                                   │
                    ┌──────────────────────────────────────────────┼──────────────────────────────────────────────┐
                    │                                              │                                              │
                    ▼                                              ▼                                              ▼
          ┌─────────────────┐                            ┌─────────────────┐                            ┌─────────────────┐
          │  📝 Plain       │                            │  📚 Research    │                            │  📄 LaTeX       │
          │  English        │                            │  Paragraphs     │                            │  Code           │
          │  Explanations   │                            │  (Academic)     │                            │  (Overleaf)     │
          └─────────────────┘                            └─────────────────┘                            └─────────────────┘
```

Whenever you push new code, the software automatically generates:

1. **🗣️ Simple Explanations** — Plain English summaries of what the code does
2. **📖 Research Paragraphs** — Formal, academic-style writing suitable for thesis reports
3. **📄 LaTeX Code** — Ready-to-use LaTeX environments for Overleaf or academic papers

---

## ✨ Features

### 🔗 GitHub Integration
Connect directly to your version control system with enterprise-grade security.

| Feature | Description |
|---------|-------------|
| **🔐 Secure Login** | Uses GitHub OAuth to log in without storing passwords |
| **📥 Auto-Fetch** | Automatically retrieves all repositories associated with your account |
| **👁️ Real-Time Monitoring** | Detects new commits or push events instantly |

### 🤖 AI-Powered Generation
The core engine transforms code logic into three distinct formats.

| Output Type | Best For |
|-------------|----------|
| **Simple Code Explanation** | README files, onboarding docs, team communication |
| **Research/Thesis Paragraphs** | University reports, academic papers, formal documentation |
| **LaTeX Code Generation** | Overleaf, TeXShop, academic journals |

### 🖥️ Documentation Viewer
A clean, tab-based interface to review your generated content.

- **📑 View Modes** — Switch between "Plain Text," "Research Style," and "LaTeX" tabs
- **✅ Verification** — Review content before using it in your reports
- **📋 One-Click Copy** — Quickly copy generated text to your clipboard

### 📊 Repository Dashboard
A central hub for managing your projects.

- **🟢 Status Indicators** — Visual tags showing "Active" or "Inactive" repositories
- **📈 Activity Feed** — Real-time commit activity across connected projects

### 🕐 Commit Tracking
Granular tracking of your work history.

- **📜 History Log** — Lists recent commits with timestamps and messages
- **🔄 Manual Trigger** — Generate documentation for past commits you might have missed

### 📴 Offline-Ready Experience
The app runs locally on your desktop.

- **💾 Local Caching** — View past write-ups without internet
- **🔒 Privacy** — Data processed and stored only on your machine

### 📤 Export Options
Easily move your documentation to other tools.

| Format | Extension |
|--------|-----------|
| Markdown | `.md` |
| PDF | `.pdf` |
| LaTeX | `.tex` |
| Plain Text | `.txt` |

---

## 🚀 Quick Start

### Prerequisites

Before installing, ensure your system has:

| Tool | Version | Purpose |
|------|---------|---------|
| **Node.js & npm** | Latest LTS | Electron Application Shell + React frontend |
| **Python** | 3.8+ | FastAPI Backend (AI logic & database) |
| **Git** | Latest | Download source code |

### Step 1: Clone the Repository

```bash
# Download the latest version of the code
git clone https://github.com/5h444n/AutoDoc-Writer.git

# Enter the project directory
cd AutoDoc-Writer
```

### Step 2: Backend Setup (The Logic Core)

```bash
# Navigate to the backend folder
cd backend

# Create a virtual environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure API Keys

Create a `.env` file inside the `backend` folder:

```env
# Google Gemini AI Key (required)
GOOGLE_API_KEY=your_gemini_api_key_here

# GitHub Personal Access Token (optional, for private repos)
GITHUB_TOKEN=your_personal_access_token_here

# GitHub OAuth (required for login)
GITHUB_CLIENT_ID=your_github_client_id_here
GITHUB_CLIENT_SECRET=your_github_client_secret_here
REDIRECT_URI=http://localhost:8000/auth/callback

# Security
SECRET_KEY=your_secret_key_here

# Frontend URL
FRONTEND_URL=http://localhost:5173
```

> **💡 Tip:** Get your Google Gemini API key at [Google AI Studio](https://aistudio.google.com/) (free tier available)

### Step 4: Start the Backend Server

```bash
# Keep this terminal window open
uvicorn main:app --reload
```

*You should see: `Uvicorn running on http://127.0.0.1:8000`*

### Step 5: Frontend Setup (New Terminal)

```bash
# Open a new terminal and navigate to frontend
cd frontend

# Install Node modules
npm install

# Launch the application
npm start
```

### Step 6: Access the Application

| Service | URL |
|---------|-----|
| **Frontend App** | http://localhost:5173 |
| **Backend API** | http://localhost:8000 |
| **API Docs (Swagger)** | http://localhost:8000/docs |
| **API Docs (ReDoc)** | http://localhost:8000/redoc |

---

## 📖 Usage Guide

### 1. Login & Connection

```
┌────────────────────────────────────────────────────────┐
│                                                        │
│         🔐 Login with GitHub                          │
│                                                        │
│    [ Click to Authorize with OAuth ]                  │
│                                                        │
│    ✓ Your password is NEVER stored                    │
│    ✓ Secure OAuth 2.0 authentication                  │
│                                                        │
└────────────────────────────────────────────────────────┘
```

1. Click **"Login with GitHub"** to securely authorize the app
2. After logging in, view all your repositories on the dashboard
3. Check visual indicators for "Active" or "Inactive" status
4. Toggle the switch to **"Active"** for repos you want AI to monitor

### 2. Generating Documentation

| Method | How It Works |
|--------|--------------|
| **🔄 Automatic (Real-Time)** | Push code to GitHub (`git push`) → App detects new commit → Generates text automatically |
| **📜 Manual History** | Navigate to "Commit Activity" tab → Select past commit → Click "Generate Docs" |

### 3. Viewing Results

Navigate to the **Documentation Viewer** to see AI-generated output:

| Tab | Description |
|-----|-------------|
| **📝 Plain Text** | Simple, plain English explanation of code changes |
| **📚 Research Style** | Formal, academic paragraphs (ideal for thesis reports) |
| **📄 LaTeX** | Ready-to-use code block for Overleaf |

### 4. Exporting & Offline Access

- **📋 One-Click Copy** — Instantly paste text into your report
- **💾 Export File** — Save as Markdown, PDF, or LaTeX
- **📴 Offline Access** — View past write-ups without internet connection

---

## 🏗️ Architecture

AutoDoc Writer uses a hybrid desktop-web architecture for privacy, speed, and offline capability.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            DESKTOP APPLICATION                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                        ELECTRON SHELL (Node.js)                       │  │
│  │                                                                        │  │
│  │  • Native desktop experience                                          │  │
│  │  • Full system access (file system, notifications)                    │  │
│  │  • Cross-platform (Windows, macOS, Linux)                             │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                      │                                       │
│                                      ▼                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                        FRONTEND (React + TypeScript)                  │  │
│  │                                                                        │  │
│  │  • User Interface & Dashboard                                         │  │
│  │  • State Management (Active/Inactive repos)                           │  │
│  │  • Documentation Viewer                                               │  │
│  │  • Tailwind CSS Styling                                               │  │
│  └────────────────────────────────────┬─────────────────────────────────┘  │
│                                       │ REST API Calls                      │
│                                       ▼                                      │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                        BACKEND (Python + FastAPI)                     │  │
│  │                                                                        │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐       │  │
│  │  │  GitHub API     │  │  AI Processing  │  │  Templating     │       │  │
│  │  │  (PyGithub)     │  │  (Google Gemini)│  │  (Jinja2)       │       │  │
│  │  │                 │  │                 │  │                 │       │  │
│  │  │ • Fetch repos   │  │ • Generate text │  │ • Format output │       │  │
│  │  │ • Read diffs    │  │ • Code analysis │  │ • LaTeX styling │       │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘       │  │
│  └────────────────────────────────────┬─────────────────────────────────┘  │
│                                       │                                      │
│                                       ▼                                      │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                        DATABASE (SQLite + SQLAlchemy)                 │  │
│  │                                                                        │  │
│  │  • Local caching of generated documentation                           │  │
│  │  • Offline access to past write-ups                                   │  │
│  │  • Prevents re-generating for same commit ID (saves API usage)        │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Shell** | Electron (Node.js) | Native desktop wrapper |
| **Frontend** | React + TypeScript | User interface |
| **Styling** | Tailwind CSS | Modern UI design |
| **Backend** | Python + FastAPI | Business logic & API |
| **AI** | Google Gemini | Text generation |
| **GitHub** | PyGithub | Repository access |
| **Database** | SQLite + SQLAlchemy | Local data storage |
| **Templating** | Jinja2 | Output formatting |

### Security & Privacy

| Feature | Implementation |
|---------|----------------|
| **🔐 OAuth 2.0** | Secure GitHub login—app never sees or stores passwords |
| **💻 Local Processing** | All data processed and stored locally on your machine |
| **🚫 No Cloud Storage** | Your code never leaves your computer |

---

## 🗺️ Roadmap

**Methodology:** Extreme Programming (XP) | **Duration:** Nov 2025 - Feb 2026

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            DEVELOPMENT TIMELINE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Sprint 1                Sprint 2                Sprint 3                   │
│  ────────                ────────                ────────                   │
│  Foundation              Intelligence           Heavy Lifting               │
│  & Connectivity          Core                   (Crunch Sprint)             │
│                                                                              │
│  ✓ UI Skeleton           ✓ AI Integration       • Deep Logic                │
│  ✓ GitHub Auth           ✓ Basic Summary        • LaTeX/Research            │
│  ✓ Repo Fetching         ✓ Active Monitoring    • Export Options            │
│  ✓ Electron + React      ✓ Detect New Commits   • Diff Reading              │
│  ✓ FastAPI Server                               • Overleaf Testing          │
│                                                                              │
│  ──────────────────────────────────────────────────────────────────────────│
│                                                                              │
│  Sprint 4                Sprint 5                                           │
│  ────────                ────────                                           │
│  Polish &                Final Demo                                         │
│  Offline Capability      Prep                                               │
│                                                                              │
│  • Offline Mode          • Full Product Demo                                │
│  • Caching               • Bug Bash                                         │
│  • Settings              • Create Installer                                 │
│  • Packaging             • (.exe / .dmg)                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Milestone Progress

| Sprint | Focus | Status |
|--------|-------|--------|
| **Sprint 1** | Foundation & Connectivity | ✅ Complete |
| **Sprint 2** | Intelligence Core | ✅ Complete |
| **Sprint 3** | Heavy Lifting (LaTeX/Research) | 🚧 In Progress |
| **Sprint 4** | Polish & Offline Capability | 📋 Planned |
| **Sprint 5** | Final Demo Prep | 📋 Planned |

---

## 🔧 Troubleshooting

### Common Issues & Solutions

<details>
<summary><b>❌ "API Key Not Found" Error</b></summary>

**Problem:** The application cannot find your Google Gemini API key.

**Solution:**
1. Navigate to the `backend` folder
2. Create or edit the `.env` file
3. Add your API key: `GOOGLE_API_KEY=your_key_here`
4. Restart the backend server

</details>

<details>
<summary><b>⬜ Window is White/Empty</b></summary>

**Problem:** The Electron window loads but shows nothing.

**Solution:**
1. Ensure the Python backend is running in a separate terminal
2. Check that the backend shows `Uvicorn running on http://127.0.0.1:8000`
3. Restart the frontend with `npm start`

</details>

<details>
<summary><b>🔐 GitHub OAuth Authentication Fails</b></summary>

**Problem:** Cannot log in with GitHub.

**Solution:**
1. Verify `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` in `.env`
2. Check callback URL in GitHub OAuth settings matches `REDIRECT_URI`
3. Clear browser cookies and try again

</details>

<details>
<summary><b>📦 Module Not Found Errors</b></summary>

**Problem:** Python or Node.js modules are missing.

**Solution:**
```bash
# Backend
cd backend
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

</details>

<details>
<summary><b>🚫 Port Already in Use</b></summary>

**Problem:** Port 8000 or 5173 is occupied.

**Solution:**
```bash
# Find process using the port
lsof -i :8000  # or lsof -i :5173

# Use alternative ports
uvicorn main:app --reload --port 8001
npm start -- --port 5174
```

</details>

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2025 Ahnaf Abid Shan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

See the [LICENSE](../LICENSE) file for full details.

---

<div align="center">

## 🌟 Star This Project

If you find AutoDoc Writer useful, please consider giving it a ⭐ on GitHub!

[![GitHub stars](https://img.shields.io/github/stars/5h444n/AutoDoc-Writer?style=social)](https://github.com/5h444n/AutoDoc-Writer)

---

**Made with ❤️ by [Ahnaf Abid Shan](https://github.com/5h444n)**

[🔝 Back to Top](#-autodoc-writer)

</div>

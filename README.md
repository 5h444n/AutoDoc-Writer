<div align="center">

# 📝 AutoDoc-Writer

### AI-Powered Code Documentation Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI/CD Pipeline](https://github.com/5h444n/AutoDoc-Writer/actions/workflows/ci.yml/badge.svg)](https://github.com/5h444n/AutoDoc-Writer/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.2-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-3178C6.svg)](https://www.typescriptlang.org/)
[![Test Coverage](https://img.shields.io/badge/tests-16%2F21%20passing-orange.svg)](./backend/README_TESTS.md)

**Transform your codebase into professional documentation with the power of AI**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](#-contributing) • [Support](#-support)

</div>

---

## 📖 Overview

**AutoDoc-Writer** is an intelligent documentation generation platform that leverages Google's Gemini AI to automatically convert source code into high-quality, readable documentation. Whether you need plain English explanations for your team, academic-style research documentation, or publication-ready LaTeX output, AutoDoc-Writer delivers professional results with minimal effort.

### 🎯 Key Value Propositions

- **🚀 Save Time**: Generate comprehensive documentation in seconds, not hours
- **🎓 Multiple Styles**: Plain English, Academic/Research, and LaTeX formats
- **🔐 Secure Integration**: OAuth 2.0 integration with GitHub for seamless repository access
- **🤖 AI-Powered**: Leverages Google Gemini AI for intelligent code understanding
- **🏗️ Modern Architecture**: Built with FastAPI and React for performance and scalability
- **📊 Enterprise-Ready**: Structured for team collaboration and professional use

---

## ✨ Features

### Core Capabilities

#### 📝 Multi-Format Documentation Generation
- **Plain English Style**: Mentor-like explanations perfect for junior developers and README files
- **Research/Thesis Style**: Formal, academic documentation with passive voice and technical precision
- **LaTeX Format**: Publication-ready code ready for Overleaf, TeXShop, and academic journals

#### 🔗 GitHub Integration
- **OAuth Authentication**: Secure GitHub login flow
- **Repository Management**: Browse and select repositories for documentation
- **Real-time Sync**: Track repository updates and documentation status

#### 🎨 Modern User Interface
- **React + TypeScript**: Type-safe, responsive frontend
- **Intuitive Design**: Clean, professional interface for easy navigation
- **Real-time Preview**: See generated documentation instantly

#### 🛡️ Security & Reliability
- **OAuth 2.0**: Industry-standard authentication
- **Environment-based Configuration**: Secure credential management
- **Comprehensive Testing**: 21 automated tests for reliability
- **Error Handling**: Robust error management and user feedback

---

## 🏗️ Architecture

AutoDoc-Writer follows a modern, microservices-inspired architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
│  React 19 + TypeScript + Vite                               │
│  - User Interface                                            │
│  - OAuth Flow Management                                     │
│  - Repository Selection                                      │
│  - Documentation Preview                                     │
└───────────────────────────┬─────────────────────────────────┘
                            │ REST API
                            │ (CORS-enabled)
┌───────────────────────────┴─────────────────────────────────┐
│                        Backend Layer                         │
│  FastAPI + Python 3.8+                                      │
│  ┌─────────────┐ ┌──────────────┐ ┌────────────────┐      │
│  │   Auth API  │ │  GitHub API  │ │   AI Service   │      │
│  │   OAuth 2.0 │ │  PyGithub    │ │ Google Gemini  │      │
│  └─────────────┘ └──────────────┘ └────────────────┘      │
│                                                              │
│  ┌──────────────────────────────────────────────────┐      │
│  │              Database Layer                       │      │
│  │  SQLAlchemy + SQLite                             │      │
│  │  - User Sessions                                  │      │
│  │  - Repository Metadata                            │      │
│  │  - Documentation Cache                            │      │
│  └──────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            │
┌───────────────────────────┴─────────────────────────────────┐
│                   External Services                          │
│  - GitHub API (Repository Access)                           │
│  - Google Gemini AI (Documentation Generation)              │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- **Framework**: FastAPI (modern, high-performance Python web framework)
- **Database**: SQLAlchemy + SQLite (upgradeable to PostgreSQL)
- **AI Integration**: Google Generative AI (Gemini)
- **GitHub API**: PyGithub
- **Authentication**: OAuth 2.0
- **Testing**: pytest + pytest-asyncio

**Frontend:**
- **Framework**: React 19.2
- **Language**: TypeScript 5.9
- **Build Tool**: Vite 7.2
- **Linting**: ESLint with React plugins

**Development:**
- **API Documentation**: Auto-generated OpenAPI/Swagger
- **Environment Management**: python-dotenv
- **Version Control**: Git + GitHub

---

## 📋 Prerequisites

Before installing AutoDoc-Writer, ensure you have:

### System Requirements

- **Python**: 3.8 or higher
- **Node.js**: 16.0 or higher
- **npm**: 8.0 or higher
- **Git**: 2.0 or higher
- **OS**: Linux, macOS, or Windows with WSL2

### External Services

1. **GitHub Account**: For OAuth authentication
   - Create a GitHub OAuth App: [GitHub Developer Settings](https://github.com/settings/developers)
   - Required permissions: `repo` (for repository access)

2. **Google Gemini API Key**: For AI-powered documentation
   - Get your API key: [Google AI Studio](https://aistudio.google.com/)
   - Free tier available for development

### Hardware Recommendations

- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB for application + space for repositories
- **Network**: Stable internet connection for API calls

---

## 🚀 Quick Start

### Step 1: Clone the Repository

```bash
git clone https://github.com/5h444n/AutoDoc-Writer.git
cd AutoDoc-Writer
```

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install
```

### Step 4: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

**Required Configuration:**

```bash
# GitHub OAuth (Create at: https://github.com/settings/developers)
GITHUB_CLIENT_ID=your_github_client_id_here
GITHUB_CLIENT_SECRET=your_github_client_secret_here
REDIRECT_URI=http://localhost:8000/auth/callback

# Google Gemini AI (Get at: https://aistudio.google.com/)
GEMINI_API_KEY=your_google_api_key_here

# Security
SECRET_KEY=generate_a_long_random_string_here

# Frontend URL (default for Vite)
FRONTEND_URL=http://localhost:5173

# Database (SQLite by default)
DATABASE_URL=sqlite:///./autodoc.db

# Environment
ENV=development
```

> **⚠️ Security Note**: Never commit your `.env` file. It's already in `.gitignore`.

### Step 5: Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Activate virtual environment
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Step 6: Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Interactive Swagger UI)
- **Alternative API Docs**: http://localhost:8000/redoc (ReDoc UI)

---

## 📚 Usage Guide

### 1. Authentication

1. Open the application in your browser: `http://localhost:5173`
2. Click **"Login with GitHub"**
3. Authorize the application (first time only)
4. You'll be redirected back to the application

### 2. Select Repository

1. After authentication, you'll see your GitHub repositories
2. Browse or search for the repository you want to document
3. Click on a repository to select it

### 3. Choose Documentation Style

Select your preferred documentation format:

- **Plain English**: For team documentation, READMEs, and onboarding
- **Research/Thesis**: For academic papers and formal documentation
- **LaTeX**: For publication-ready output in academic journals

### 4. Generate Documentation

1. Click **"Generate Documentation"**
2. Wait for AI processing (typically 5-30 seconds depending on code size)
3. Preview the generated documentation
4. Copy or export the documentation

### 5. Export Options

- **Copy to Clipboard**: One-click copy for easy pasting
- **Download as File**: Save as .md, .tex, or .txt
- **Direct Integration**: (Coming soon) Push documentation back to GitHub

---

## 🔧 Configuration

### Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GITHUB_CLIENT_ID` | Yes | - | GitHub OAuth App Client ID |
| `GITHUB_CLIENT_SECRET` | Yes | - | GitHub OAuth App Client Secret |
| `REDIRECT_URI` | Yes | - | OAuth callback URL |
| `GEMINI_API_KEY` | Yes | - | Google Gemini AI API Key |
| `SECRET_KEY` | Yes | - | Application secret for sessions |
| `FRONTEND_URL` | No | `http://localhost:5173` | Frontend application URL |
| `DATABASE_URL` | No | `sqlite:///./autodoc.db` | Database connection string |
| `ENV` | No | `development` | Environment (development/production) |

### GitHub OAuth Setup Guide

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click **"New OAuth App"**
3. Fill in the details:
   - **Application name**: AutoDoc-Writer (or your preferred name)
   - **Homepage URL**: `http://localhost:5173`
   - **Authorization callback URL**: `http://localhost:8000/auth/callback`
4. Click **"Register application"**
5. Copy **Client ID** and **Client Secret** to your `.env` file

### Database Configuration

**Default (SQLite):**
```bash
DATABASE_URL=sqlite:///./autodoc.db
```

**PostgreSQL (Production):**
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/autodoc
```

**MySQL (Alternative):**
```bash
DATABASE_URL=mysql://user:password@localhost:3306/autodoc
```

---

## 🧪 Testing

AutoDoc-Writer includes a comprehensive test suite covering authentication, GitHub integration, database operations, and security.

### Running Tests

```bash
cd backend
source venv/bin/activate
pytest test_backend.py -v
```

### Test Coverage

**Current Status**: 16/21 tests passing (76%)

- ✅ Authentication flow
- ✅ GitHub API integration
- ✅ Database operations
- ✅ Error handling
- ⚠️ AI generation (4 tests pending)
- ⚠️ Security validations (1 test pending)

For detailed test results, see [backend/README_TESTS.md](backend/README_TESTS.md)

### Running Specific Tests

```bash
# Run authentication tests only
pytest test_backend.py -k "test_auth" -v

# Run with coverage report
pytest test_backend.py --cov=app --cov-report=html

# Run in verbose mode with output
pytest test_backend.py -v -s
```

---

## 🚀 Development

### Project Structure

```
AutoDoc-Writer/
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       │   ├── auth.py       # Authentication endpoints
│   │   │       │   └── repos.py      # Repository endpoints
│   │   │       └── router.py         # API router configuration
│   │   ├── core/           # Core functionality
│   │   │   ├── config.py            # Application configuration
│   │   │   ├── security.py          # Security utilities
│   │   │   └── prompts.py           # AI system prompts
│   │   ├── db/             # Database
│   │   │   ├── base.py              # Base models
│   │   │   └── session.py           # Database session
│   │   ├── models/         # SQLAlchemy models
│   │   │   ├── user.py              # User model
│   │   │   └── repository.py        # Repository model
│   │   ├── schemas/        # Pydantic schemas
│   │   │   └── repo.py              # Repository schemas
│   │   ├── services/       # Business logic
│   │   │   └── github_service.py    # GitHub API service
│   │   └── main.py         # Application entry point
│   ├── requirements.txt     # Python dependencies
│   ├── test_backend.py      # Test suite
│   └── README_TESTS.md      # Test documentation
├── frontend/                # React frontend application
│   ├── src/
│   │   ├── App.tsx          # Main application component
│   │   ├── main.tsx         # Application entry point
│   │   └── assets/          # Static assets
│   ├── public/              # Public assets
│   ├── package.json         # Node.js dependencies
│   ├── tsconfig.json        # TypeScript configuration
│   └── vite.config.ts       # Vite configuration
├── design/                  # Design documents and wireframes
├── .env.example             # Example environment configuration
├── .gitignore              # Git ignore rules
├── LICENSE                 # MIT License
├── README.md               # This file
├── BUG_REPORT.md           # Known bugs and issues
├── IMPROVEMENTS.md         # Improvement recommendations
├── TESTING_SUMMARY.md      # Testing overview
├── AI_GUIDELINES.md        # AI persona guidelines
└── GOLDEN_DATASET.md       # AI validation dataset
```

### Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow existing code style
   - Add tests for new features
   - Update documentation

3. **Run tests**
   ```bash
   cd backend
   pytest test_backend.py -v
   ```

4. **Run linters**
   ```bash
   # Frontend linting
   cd frontend
   npm run lint
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

6. **Push and create pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Code Style Guidelines

**Python (Backend):**
- Follow PEP 8 style guide
- Use type hints for function parameters and returns
- Write docstrings for classes and functions
- Maximum line length: 88 characters (Black formatter compatible)

**TypeScript (Frontend):**
- Use TypeScript strict mode
- Follow React hooks best practices
- Use functional components over class components
- Follow ESLint configuration

### Adding New Features

1. **Backend API Endpoint:**
   - Add endpoint in `backend/app/api/v1/endpoints/`
   - Create schema in `backend/app/schemas/`
   - Add business logic in `backend/app/services/`
   - Write tests in `backend/test_backend.py`

2. **Frontend Component:**
   - Create component in `frontend/src/components/`
   - Add type definitions
   - Integrate with API
   - Test user interactions

---

## 🌐 API Documentation

### Interactive API Documentation

Once the backend is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key API Endpoints

#### Authentication

**POST** `/api/v1/auth/login`
- Initiates GitHub OAuth flow
- Redirects to GitHub authorization

**GET** `/api/v1/auth/callback`
- Handles OAuth callback
- Returns access token

#### Repositories

**GET** `/api/v1/repos/`
- Lists user's GitHub repositories
- Requires: `access_token` (query parameter)
- Returns: List of repositories with metadata

**Response Example:**
```json
{
  "total_repos": 25,
  "repos": [
    {
      "name": "AutoDoc-Writer",
      "url": "https://github.com/5h444n/AutoDoc-Writer",
      "last_updated": "2025-12-13T10:30:00"
    }
  ]
}
```

---

## 🚢 Deployment

### Production Deployment Checklist

- [ ] Set `ENV=production` in environment variables
- [ ] Generate strong `SECRET_KEY` (use `openssl rand -hex 32`)
- [ ] Configure production database (PostgreSQL recommended)
- [ ] Update `REDIRECT_URI` to production domain
- [ ] Update `FRONTEND_URL` to production domain
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure CORS for production domain
- [ ] Set up logging and monitoring
- [ ] Configure rate limiting
- [ ] Set up automated backups

### Deployment Options

#### Option 1: Docker (Recommended)

**Coming Soon**: Docker Compose configuration for easy deployment

#### Option 2: Traditional Server

**Backend:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run with production ASGI server
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

**Frontend:**
```bash
# Build for production
npm run build

# Serve with nginx or similar
# The build output is in frontend/dist/
```

#### Option 3: Cloud Platforms

- **Backend**: Deploy to Heroku, Railway, AWS, or Google Cloud
- **Frontend**: Deploy to Vercel, Netlify, or Cloudflare Pages

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute

- 🐛 **Report bugs**: Open an issue with detailed reproduction steps
- 💡 **Suggest features**: Share your ideas in the discussions
- 📝 **Improve documentation**: Help make our docs clearer
- 🔧 **Submit pull requests**: Fix bugs or add features

### Contribution Guidelines

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** following our code style
4. **Add tests** for new functionality
5. **Update documentation** if needed
6. **Commit your changes**: `git commit -m 'feat: add amazing feature'`
7. **Push to your fork**: `git push origin feature/amazing-feature`
8. **Open a Pull Request** with a clear description

### Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

### Code Review Process

1. All pull requests require at least one review
2. **CI/CD pipeline must pass** - All automated checks must succeed
3. Code coverage should not decrease
4. Documentation must be updated for new features
5. Security scans should not introduce new high-severity issues

### CI/CD Requirements

All pull requests automatically run through our CI/CD pipeline:
- ✅ Frontend linting and type checking
- ✅ Backend linting and testing
- ✅ Security vulnerability scanning
- ✅ Code quality analysis with CodeQL

See [CI_CD_GUIDE.md](CI_CD_GUIDE.md) for details.

---

## 🐛 Troubleshooting

### Common Issues

#### Issue: "Module not found" errors

**Solution:**
```bash
# Backend: Ensure virtual environment is activated
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Frontend: Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

#### Issue: GitHub OAuth authentication fails

**Solution:**
1. Verify `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` in `.env`
2. Check that callback URL matches in GitHub OAuth settings
3. Ensure `REDIRECT_URI=http://localhost:8000/auth/callback`
4. Clear browser cookies and try again

#### Issue: Database connection errors

**Solution:**
```bash
# Check DATABASE_URL in .env
# For SQLite (default):
DATABASE_URL=sqlite:///./autodoc.db

# Ensure write permissions in the directory
chmod 755 backend/
```

#### Issue: Port already in use

**Solution:**
```bash
# Find process using the port
lsof -i :8000  # Backend
lsof -i :5173  # Frontend

# Kill the process or use different ports
# Backend with custom port:
uvicorn app.main:app --reload --port 8001

# Frontend with custom port:
npm run dev -- --port 5174
```

#### Issue: Gemini API errors

**Solution:**
1. Verify `GEMINI_API_KEY` is correct in `.env`
2. Check API quota at [Google AI Studio](https://aistudio.google.com/)
3. Ensure stable internet connection
4. Check API status: [Google Cloud Status](https://status.cloud.google.com/)

### Getting Help

If you encounter issues not listed here:

1. **Check existing issues**: [GitHub Issues](https://github.com/5h444n/AutoDoc-Writer/issues)
2. **Review documentation**: See our [detailed docs](#-documentation)
3. **Ask the community**: Open a discussion on GitHub
4. **Report a bug**: Create a detailed issue with reproduction steps

---

## 🔒 Security

### Security Best Practices

✅ **We Follow:**
- OAuth 2.0 for authentication
- Environment-based configuration (no hardcoded secrets)
- CORS protection
- Input validation (in progress)
- Secure session management

### Known Security Issues

⚠️ **Current Vulnerabilities** (documented in [BUG_REPORT.md](BUG_REPORT.md)):

1. **Access tokens in URL query parameters** (High Priority)
   - Currently tokens are passed in URLs
   - Planned fix: Move to Authorization headers

2. **Missing rate limiting** (Medium Priority)
   - No rate limits on API endpoints
   - Planned: Implement rate limiting middleware

3. **No input validation** (Medium Priority)
   - Limited validation on user inputs
   - Planned: Add comprehensive validation

### Reporting Security Vulnerabilities

If you discover a security vulnerability:

1. **DO NOT** open a public issue
2. Email the maintainer directly: [Contact Info]
3. Include detailed information about the vulnerability
4. Allow 48 hours for initial response

### Security Checklist for Users

- [ ] Never commit your `.env` file
- [ ] Regenerate secrets for production deployment
- [ ] Use HTTPS in production
- [ ] Regularly update dependencies
- [ ] Review access permissions for GitHub OAuth
- [ ] Monitor API usage for unusual activity

**⚠️ Critical Notice**: If you forked this repository before 2025-12-10, regenerate your GitHub OAuth credentials as sample credentials may have been exposed in previous commits.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Ahnaf Abid Shan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 📊 Project Status & Roadmap

### Current Status: **Alpha Development** 🚧

**Version**: 0.1.0 (Pre-release)  
**Test Coverage**: 76% (16/21 tests passing)  
**Last Updated**: December 2025

### Development Phases

#### ✅ Phase 1: Foundation (Completed)
- [x] Backend API setup (FastAPI)
- [x] Frontend scaffold (React + TypeScript)
- [x] GitHub OAuth integration
- [x] Database schema design
- [x] Basic test suite

#### 🚧 Phase 2: Core Features (In Progress)
- [x] GitHub repository listing
- [ ] AI documentation generation (Plain English)
- [ ] AI documentation generation (Research style)
- [ ] AI documentation generation (LaTeX)
- [ ] Documentation preview
- [ ] Export functionality

#### 📋 Phase 3: Enhancement (Planned)
- [ ] Advanced repository filtering
- [ ] Batch documentation generation
- [ ] Documentation versioning
- [ ] Custom AI prompt templates
- [ ] Syntax highlighting
- [ ] Dark mode support

#### 🎯 Phase 4: Production Ready (In Progress)
- [ ] Production deployment guide
- [ ] Docker containerization
- [x] CI/CD pipeline
- [ ] Rate limiting
- [ ] Comprehensive logging
- [ ] Performance optimization
- [ ] User analytics dashboard

### Feature Requests & Voting

Vote on features you'd like to see: [GitHub Discussions](https://github.com/5h444n/AutoDoc-Writer/discussions)

---

## 📚 Documentation

### Available Documentation

| Document | Description | Link |
|----------|-------------|------|
| **README.md** | Main project documentation | (This file) |
| **CI_CD_GUIDE.md** | CI/CD pipeline guide and setup | [View](CI_CD_GUIDE.md) |
| **TESTING_GUIDE.md** | Testing guide and best practices | [View](TESTING_GUIDE.md) |
| **BUG_REPORT.md** | Known bugs and issues | [View](BUG_REPORT.md) |
| **IMPROVEMENTS.md** | Improvement recommendations | [View](IMPROVEMENTS.md) |
| **TESTING_SUMMARY.md** | Testing overview and metrics | [View](TESTING_SUMMARY.md) |
| **EXECUTIVE_SUMMARY.md** | Project executive summary | [View](EXECUTIVE_SUMMARY.md) |
| **AI_GUIDELINES.md** | AI persona and prompt guidelines | [View](AI_GUIDELINES.md) |
| **GOLDEN_DATASET.md** | AI validation test dataset | [View](GOLDEN_DATASET.md) |
| **backend/README_TESTS.md** | Detailed test documentation | [View](backend/README_TESTS.md) |

### External Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **React Documentation**: https://react.dev/
- **Google Gemini AI**: https://ai.google.dev/
- **PyGithub Documentation**: https://pygithub.readthedocs.io/

---

## 👥 Team & Credits

### Core Team

- **Ahnaf Abid Shan** - Creator & Lead Developer - [@5h444n](https://github.com/5h444n)

### Contributors

We appreciate all contributions! See our [Contributors](https://github.com/5h444n/AutoDoc-Writer/graphs/contributors) page.

### Acknowledgments

- **FastAPI** - Modern web framework for building APIs
- **React Team** - Powerful UI library
- **Google** - Gemini AI platform
- **GitHub** - OAuth integration and hosting
- **Open Source Community** - For inspiration and support

---

## 💬 Support & Contact

### Community Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/5h444n/AutoDoc-Writer/issues)
- **GitHub Discussions**: [Ask questions or share ideas](https://github.com/5h444n/AutoDoc-Writer/discussions)
- **Documentation**: [Read our comprehensive docs](#-documentation)

### Stay Updated

- **Star this repository** ⭐ to receive updates
- **Watch releases** to get notified of new versions
- **Follow development** in our GitHub projects board

### Connect

- **GitHub**: [@5h444n](https://github.com/5h444n)
- **Repository**: [AutoDoc-Writer](https://github.com/5h444n/AutoDoc-Writer)

---

## 🙏 Acknowledgments

Thank you to everyone who has contributed to making AutoDoc-Writer better!

Special thanks to:
- Early testers and beta users
- Contributors who submitted bug reports and feature requests
- The open-source community for inspiration and tools

---

<div align="center">

**Made with ❤️ by the AutoDoc-Writer Team**

[⬆ Back to Top](#-autodoc-writer)

</div>

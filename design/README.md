# AutoDoc Writer - Design Documentation

This directory contains wireframes and design specifications for the AutoDoc Writer application interface.

## Overview

AutoDoc Writer is a documentation generation tool that monitors repositories and automatically creates documentation from commits. The application features a dashboard-based interface with multiple views for managing repositories, viewing commits, and accessing generated documentation.

## Navigation Flow

The application follows a hierarchical navigation structure:

```
Sidebar (Global Navigation)
├── Dashboard (Home)
│   ├── Overview Statistics
│   ├── Active Repositories Section
│   └── Recent Activity Section
├── Repositories
│   └── Repository Monitoring Management
├── Commits
│   └── Commit Activity Board
├── Documentation
│   ├── Plain Text Viewer
│   ├── Research-Style Viewer
│   └── LaTeX Viewer
└── Settings
```

Users navigate through the application using the persistent sidebar, which provides access to all major sections. The dashboard serves as the landing page, offering quick access to key metrics and recent activities.

## Wireframes

### 1. Sidebar Navigation (`sidebar.png`)

**Purpose**: Provides persistent global navigation throughout the application.

**Components**:
- Application branding (AutoDoc Writer logo and title)
- Navigation menu items:
  - Dashboard (highlighted when active)
  - Repositories
  - Commits
  - Documentation
  - Settings
- Version information footer (AutoDoc Writer v1.0)

**User Flow**: Always visible on the left side of the application. Users click menu items to navigate between major sections.

---

### 2. Dashboard - Home View (`dashboard_home.png`)

**Purpose**: Serves as the main landing page, providing an overview of documentation activity and quick access to active repositories.

**Components**:
- **Header**: 
  - Page title ("Dashboard")
  - User profile section (avatar, name, email)
  - Logout button
- **Welcome Section**:
  - Personalized greeting ("Welcome back!")
  - Activity overview text
- **Statistics Cards** (3 cards in a row):
  - Monitored Repositories (with "Active" status badge)
  - Recent Commits
  - Generated Documents
- **Active Repositories Section**:
  - Section heading
  - Repository cards showing:
    - Repository name
    - Description
    - Repository icon
- **Recent Activity Section**:
  - Section heading
  - Activity feed showing:
    - Repository name
    - Action description
    - Timestamp
    - Status indicator

**User Flow**: First screen users see after login. Users can click on repository names to view details or navigate to other sections via the sidebar.

---

### 3. Dashboard - Active Repositories Detail (`dashboard_active_repositories.png`)

**Purpose**: Shows a detailed scrollable view of active repositories with their recent activities.

**Components**:
- Same header and statistics cards as home view
- **Active Repositories Panel** (left side):
  - Repository cards with:
    - Icon
    - Repository name
    - Description text
- **Recent Activity Panel** (right side):
  - Activity items showing:
    - Repository name
    - Commit message or action
    - Timestamp
    - Status badge (e.g., "Documented")

**User Flow**: Accessible from the dashboard, shows more detailed information about repository activities.

---

### 4. Repositories Management (`repositories.png`)

**Purpose**: Central hub for enabling/disabling automatic documentation generation for repositories.

**Components**:
- **Header** with page title "Repositories"
- **Subtitle**: "Repository Monitoring"
- **Description**: "Enable or disable automatic documentation generation for your repositories."
- **Search and Filter Bar**:
  - Search input field ("Search repositories...")
  - Filter icon
  - Dropdown filter ("All Repositories")
- **Repository Cards Grid**:
  - Each card displays:
    - Repository icon
    - Repository name
    - Description
    - Status label (Active/Inactive)
    - Toggle switch for enabling/disabling monitoring

**User Flow**: Users access this screen from the sidebar to manage which repositories should have automatic documentation generation. Toggle switches allow instant activation/deactivation.

---

### 5. Commits Activity Board (`commits_board.png`)

**Purpose**: Displays a comprehensive view of commit activity across all monitored repositories.

**Components**:
- **Header** with page title "Commits"
- **Subtitle**: "Commit Activity"
- **Description**: "Generate documentation for recent commits across your monitored repositories."
- **Data Table** with columns:
  - Repository (with icon)
  - Commit Message
  - Hash
  - Time
  - Status (Generated/Not Generated)
  - Actions (View Docs button)
- **Generate Button**: For commits not yet documented

**User Flow**: Users can view all recent commits, check documentation generation status, and manually trigger documentation generation if needed.

---

### 6. Documentation Viewer - Plain Text (`documentation_viewer_plainText.png`)

**Purpose**: Displays generated documentation in a simple, plain text format.

**Components**:
- **Header** with page title "Documentation"
- **Document metadata** (repository name, commit hash)
- **Plain text content area** displaying:
  - Documentation sections
  - Code snippets
  - Structured text content
- **Export/Download options** (in header toolbar)

**User Flow**: Accessed from the Commits board or Recent Activity sections by clicking "View Docs" on a documented commit.

---

### 7. Documentation Viewer - Research Style (`document_viewer_research-style.png`)

**Purpose**: Presents documentation in an academic/research paper format with formatted sections.

**Components**:
- Similar header and metadata as plain text viewer
- **Formatted content area** with:
  - Styled section headings
  - Formatted paragraphs
  - References and citations
  - Professional typography
- **Export options** for research-style documents

**User Flow**: Alternative viewing format for the same documentation, selectable via format toggle or settings.

---

### 8. Documentation Viewer - LaTeX Format (`document_viewer_LaTex.png`)

**Purpose**: Displays documentation with LaTeX rendering for mathematical expressions and technical content.

**Components**:
- Similar header and metadata
- **LaTeX-rendered content area** featuring:
  - Mathematical equations
  - Technical symbols
  - Code blocks with syntax highlighting
  - LaTeX-specific formatting
- **Export to PDF/LaTeX options**

**User Flow**: Specialized viewer for technical documentation requiring mathematical notation, accessible via format selection.

---

## Component Hierarchy

### Global Components
- **Sidebar**: Persistent across all views
  - Logo/Branding
  - Navigation Menu
  - Version Footer

- **Page Header**: Present on all main content pages
  - Page Title
  - User Profile Section
  - Action Buttons (context-specific)

### Dashboard Components
- Statistics Cards (reusable component)
- Repository Card Component
- Activity Feed Item Component

### Repository Management Components
- Search/Filter Bar
- Repository Toggle Card
- Status Badge Component

### Commits Components
- Data Table Component
- Status Indicator
- Action Button Group

### Documentation Viewer Components
- Document Header
- Content Renderer (with multiple format modes)
- Export Toolbar

## Design Principles

1. **Consistent Navigation**: Sidebar remains consistent across all views
2. **Clear Hierarchy**: Information is organized from overview to detail
3. **Status Indicators**: Visual cues (colors, badges) show repository and documentation status
4. **Responsive Cards**: Information is presented in card-based layouts for better scanning
5. **Action-Oriented**: Clear calls-to-action (toggle switches, buttons) for user interactions
6. **Multiple View Options**: Documentation can be viewed in different formats based on user needs

## File Naming Convention

Files follow the pattern: `{section}_{subsection}.png`
- `sidebar.png`: Global navigation
- `dashboard_*.png`: Dashboard views
- `repositories.png`: Repository management
- `commits_board.png`: Commit activity view
- `document_viewer_*.png`: Documentation viewer formats
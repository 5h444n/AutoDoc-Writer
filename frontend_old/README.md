# AutoDoc-Writer Frontend

React + TypeScript + Vite frontend for the AutoDoc-Writer application.

## Overview

This is the web interface for AutoDoc-Writer, an AI-powered code documentation generator. The frontend provides a modern, intuitive interface for users to authenticate with GitHub, browse repositories, and generate documentation in multiple formats.

## Tech Stack

- **React 19.2** - UI library
- **TypeScript 5.9** - Type-safe JavaScript
- **Vite 7.2** - Fast build tool and dev server
- **ESLint** - Code linting

## Development

### Prerequisites

- Node.js 16.0 or higher
- npm 8.0 or higher

### Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# The app will be available at http://localhost:5173
```

### Available Scripts

```bash
# Start development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

## Project Structure

```
frontend/
├── src/
│   ├── App.tsx           # Main application component
│   ├── main.tsx          # Application entry point
│   ├── assets/           # Static assets (images, icons)
│   ├── App.css           # Application styles
│   └── index.css         # Global styles
├── public/               # Public static files
├── index.html            # HTML entry point
├── package.json          # Dependencies and scripts
├── tsconfig.json         # TypeScript configuration
├── vite.config.ts        # Vite configuration
└── eslint.config.js      # ESLint configuration
```

## Environment Variables

The frontend connects to the backend API. By default, it expects the backend to be running at `http://localhost:8000`.

## Code Quality

### Linting

This project uses ESLint with TypeScript and React-specific rules. Run linting with:

```bash
npm run lint
```

### Type Checking

TypeScript is configured in strict mode for enhanced type safety. Build the project to check for type errors:

```bash
npm run build
```

## Backend Integration

The frontend communicates with the FastAPI backend for:
- GitHub OAuth authentication
- Repository listing
- Documentation generation
- AI-powered content creation

Ensure the backend is running before starting the frontend. See the main [README](../README.md) for backend setup instructions.

## Contributing

When contributing to the frontend:

1. Follow the existing code style
2. Use TypeScript for all new files
3. Run `npm run lint` before committing
4. Ensure `npm run build` completes without errors
5. Use functional components with hooks (no class components)

## Build and Deployment

### Production Build

```bash
npm run build
```

This creates an optimized production build in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

### Deployment

The built files in `dist/` can be deployed to any static hosting service:
- Vercel
- Netlify
- Cloudflare Pages
- AWS S3 + CloudFront
- GitHub Pages

## Learn More

- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/)
- [Vite Documentation](https://vite.dev/)
- [Main Project README](../README.md)

# leet-info-graph-gpt-5.2-codex-v2

> This project is being developed by an autonomous coding agent.

## Overview

# Research Infograph Assistant - Project Goals

## Overview

Build a full-stack web application that lets users sign in with Google, submit research prompts, 
and receive AI-generated infographics wit...

## Features

*Features will be documented here as they are implemented.*


- Backend skeleton with FastAPI service, Click CLI entry point, and health check endpoint at `/api/v1/health`.
- Frontend skeleton with Vue 3 + Vite, TailwindCSS, Element Plus, and placeholder routes (Login, Chat, History).
- Backend health check integration on app load with connection status banner.
- Initial i18n scaffolding for English, Japanese, and Chinese UI strings.

- Backend health check endpoint available at `/api/v1/health` with FastAPI service initialization.
- Frontend health status indicator with backend connectivity check and basic router placeholders.


DuckDB-backed data stores for users, research sessions, sources, messages, and infographics with automatic table creation and CRUD support.

DuckDB-backed stores for users, sessions, sources, messages, and infographics with CRUD operations and automatic table creation.

Current features: FastAPI backend skeleton with health endpoint; Vue 3 frontend skeleton with health check and placeholder pages; DuckDB CRUD stores for core entities with tests.

- Google OAuth backend authentication endpoints (`/api/v1/auth/google`, `/api/v1/auth/me`, `/api/v1/auth/logout`) with JWT issuance and verification.
- Environment-driven auth configuration (Google client ID, JWT secret) in backend settings.

- Backend authentication service verifies Google ID tokens, creates users, and issues JWTs with 24-hour expiry.
## Getting Started

### Prerequisites

*Prerequisites will be documented here.*

### Installation

```bash
# Installation instructions will be added
```

### Usage

```bash
# Usage examples will be added
```

## Development

See .leet/.todos.json for the current development status.

## Testing

```bash
# Test instructions will be added
```

## License

MIT

# leet-info-graph-gpt-5.2-codex-v2

> This project is being developed by an autonomous coding agent.

## Overview

# Research Infograph Assistant - Project Goals

## Overview

Build a full-stack web application that lets users sign in with Google, submit research prompts, 
and receive AI-generated infographics wit...

## Features

### Authentication
- Google Identity Services login flow with JWT-backed API session.
- Authenticated user info displayed in the header with logout support.
- Route guards redirect unauthenticated users to the login screen.
- Tokens persisted to localStorage and attached to API requests.


### Session Management (In Progress)
- API placeholders for session operations.
- UI scaffolding ready for session history.

## Getting Started

### Prerequisites

- Backend: Python 3.11+, Google OAuth client ID, JWT secret.
- Frontend: Node.js 18+, VITE_GOOGLE_CLIENT_ID configured.

### Installation

```bash
# Installation instructions will be added
```

### Usage

- Start the backend (`python -m infograph.svc.main --port 8000`) and frontend (`yarn dev`). The header shows backend connectivity.
- Authenticate via Google Sign-In on the Login page to access protected routes.

# Usage examples will be added
```

## Development

See .leet/.todos.json for the current development status.

## Testing

- Backend: `pytest tests/ -v`
- Frontend: `yarn test`

# Test instructions will be added
```

## License

MIT

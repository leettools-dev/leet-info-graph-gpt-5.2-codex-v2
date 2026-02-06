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
- Session and message API endpoints: create/list/get/delete sessions and create/list messages under `/api/v1/sessions`.
- Basic session management UI: list research sessions and create new prompts from the chat page.
- Session detail view placeholder for newly created research sessions.
- Session Pinia store for fetching, creating, and removing research sessions.
- Session detail route for reviewing a research session after creation.

### Chat Interface
- Active session overview on the Chat page with prompt context and status.
- Message list with role styling, loading indicator, and auto-scroll to newest message.
- Inline message composer with validation and error messaging.
- ChatInput component for composing and sending research messages with keyboard shortcuts and a send button.

- Chat state management via Pinia with message fetching/sending status tracking.

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


- Use the Chat page to start a new research session. Provide a prompt, then you are taken to the session detail view.
- Use the History page to review, open, or delete previous sessions.

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

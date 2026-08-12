# Secure File Storage Service

A self-contained secure file storage application built with React, TypeScript, Vite, FastAPI, SQLite, and local filesystem storage. It requires no cloud account, no paid API, no external authentication service, and no external storage service.

## Architecture

The browser talks to a FastAPI API under `/api`. Authentication uses opaque server-side sessions in HTTP-only cookies. Metadata persists in SQLite. File bytes are stored under `storage/objects` after streaming through `storage/temp`. Uploaded objects are never served from the frontend public root.

## Security Architecture

- Passwords are hashed with Argon2id.
- Session tokens and share tokens are random, opaque, and hashed at rest.
- Unsafe cookie-authenticated requests require `X-CSRF-Token`.
- File authorization is owner-based and enforced in service-layer database queries.
- Private files are owner-only.
- Public links require a valid unrevoked token and current file visibility of `public`.
- Upload validation uses filename sanitization, extension allowlist, MIME/type detection, magic-byte checks, server-side size limits, streaming writes, checksums, temp files, and cleanup.

## Database Schema

Tables: `users`, `sessions`, `files`, `share_links`, and `rate_limit_events`. Foreign keys use cascades where appropriate. Indexes cover login/session lookup, ownership filtering, share-token lookup, and rate-limit windows. See `docs/ARCHITECTURE.md`.

## API Endpoints

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/me`
- `GET /api/files`
- `POST /api/files`
- `GET /api/files/{id}`
- `PATCH /api/files/{id}`
- `DELETE /api/files/{id}`
- `GET /api/files/{id}/download`
- `POST /api/files/{id}/share`
- `DELETE /api/files/{id}/share`
- `GET /api/share/{token}`
- `GET /api/share/{token}/download`
- `GET /api/health`

Errors use `{ "error": { "code", "message", "details" } }`.

## Local Setup

Backend:

```bash
cd backend
python -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Docker Setup

```bash
docker compose up --build
```

Open `http://localhost:8000`.

## Testing

```bash
cd backend && pytest
cd frontend && npm run test
cd frontend && npm run build
```

Generate a 105 MB local test file:

```bash
python -c "from pathlib import Path; Path('large-test.txt').write_bytes(b'a' * 105 * 1024 * 1024)"
```

Upload it through the UI as `.txt` to verify 100 MB+ progress and streaming behavior.

## Public/Private Sharing

Files are private by default. Owners can make a file public after a confirmation, then create a share link. The public API only exposes safe metadata and never exposes internal IDs, owner IDs, storage names, or paths. Making a file private disables public-token download.

## Threat Model and Trade-offs

This project is designed for local/self-hosted take-home evaluation. SQLite is simple and portable but not ideal for high-concurrency production workloads. Local filesystem storage is secure when rooted outside the web root and accessed only through authorization-aware API endpoints, but production deployments should add quotas, AV scanning, backups, monitoring, and HTTPS.

## Future Migration

To migrate SQLite to PostgreSQL, change the SQLAlchemy database URL and run Alembic migrations. To migrate local files to S3, implement the `StorageProvider` interface in `backend/app/storage/s3_placeholder.py` without changing API or service authorization semantics.

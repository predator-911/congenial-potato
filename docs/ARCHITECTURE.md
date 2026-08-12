# Architecture

## System Architecture

React/Vite serves the user interface. FastAPI exposes `/api` endpoints. SQLite stores metadata and security state. LocalStorageProvider stores file bytes under `storage/objects` and temporary upload data under `storage/temp`.

## Request Flow

Browser requests include credentials. FastAPI dependencies resolve the session cookie, hash it, load the active session, and inject the current user.

## Upload Sequence

1. Frontend sends multipart upload with XMLHttpRequest for progress.
2. Backend authenticates and validates CSRF.
3. Filename is sanitized and extension-checked.
4. Bytes stream to a temp file in 1 MiB chunks.
5. Server enforces max size and computes SHA-256.
6. Server validates file signature/MIME.
7. Temp object is atomically moved to `storage/objects` with a UUID filename.
8. Metadata is committed to SQLite.

## Download Sequence

Private downloads require authentication and ownership. Public downloads require a valid share token and public file visibility. Downloads use file streaming responses with safe headers.

## Authentication Flow

Register/login creates an Argon2id password hash or verifies it, creates a fresh random session token, stores only the hash, and sets an HTTP-only cookie plus CSRF cookie.

## Public Sharing Flow

Owner makes a file public, creates a share link, receives the raw opaque token once, and may revoke it later. The database stores only the token hash.

## Database Relationship Diagram

```text
users 1---N sessions
users 1---N files
files 1---N share_links
```

## Storage Architecture

```text
storage/
  temp/      transient upload files
  objects/   UUID-named validated files
```

`storage_path` is internal metadata and is not returned by public APIs.

## Security Boundaries

The backend is the only authorization boundary. The client is untrusted. Local storage is accessed only through backend-generated safe paths.

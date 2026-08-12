# Security

## Threat Model

Attackers may be unauthenticated visitors, authenticated malicious users, or users with leaked opaque share links. The server, database, and local storage root are trusted application components.

## Attack Surface

- Authentication endpoints
- Cookie sessions
- CSRF-protected mutation endpoints
- Multipart upload parser
- File metadata APIs
- Download APIs
- Public share-token APIs

## File Upload Threats and Mitigations

- Arbitrary executable upload: extension allowlist blocks executable formats.
- MIME spoofing: server checks signatures and content heuristics instead of trusting `Content-Type`.
- Path traversal: original names are sanitized and never used as storage paths.
- Oversized uploads: byte count is enforced while streaming.
- Memory exhaustion: uploads and downloads stream in chunks.
- Partial uploads: temp files are removed on failure.
- Filename attacks: null bytes, path separators, absolute paths, hidden names, and dangerous double extensions are rejected.

## Authentication Threats

Passwords are Argon2id hashes. Session fixation is mitigated by creating a new session on login. Session theft impact is reduced by HTTP-only cookies and hashed session tokens at rest. Brute force is limited by the built-in rate limiter.

## Authorization and IDOR

Every file operation queries by `file_id` and `owner_id`. Non-owners cannot read metadata, download, rename, delete, change visibility, create shares, or revoke shares for another user's file.

## CSRF

Unsafe methods require a CSRF header matching the CSRF cookie. Session cookies use SameSite=Lax.

## XSS

The frontend renders filenames as text and does not use `dangerouslySetInnerHTML`.

## DoS and Storage Exhaustion

The default file cap is 250 MB. Production deployments should add per-user quotas, global quotas, request body limits at the reverse proxy, and monitoring.

## Public File Disclosure

Public links are high-entropy bearer secrets stored hashed at rest. A link works only if not revoked, not expired, and the file is currently public.

## Residual Risks

This local-first project does not include antivirus scanning, distributed rate limiting, object-store durability, WAF rules, or production HTTPS termination. These are documented future improvements, not hidden dependencies.

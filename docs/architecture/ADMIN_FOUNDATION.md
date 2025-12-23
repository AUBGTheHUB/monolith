# Admin API Foundation (Phase 0)

This document gives a brief overview of the current admin backend scaffold.

## Route Group

`/api/v3/admin` – All admin endpoints live under this prefix.

### Current Endpoint Stubs (501 Not Implemented)

- Sponsors: `GET /admin/sponsors`, `GET /admin/sponsors/{id}`, `POST /admin/sponsors`, `PATCH /admin/sponsors/{id}`, `DELETE /admin/sponsors/{id}`
- Mentors: same CRUD pattern
- Judges: same CRUD pattern
- Team Members: same CRUD pattern
- Past Events: same CRUD pattern

## Data Models (Dataclasses)

Located in `src/database/model/admin/`:

- Sponsor (name, tier, logo_url, website_url?)
- Mentor (name, company, job_title, avatar_url, expertise_areas[], linkedin_url?)
- Judge (name, company, job_title, avatar_url, linkedin_url?)
- TeamMember (name, role_title, avatar_url, social_links{platform: url})
- PastEvent (title, cover_picture, tags[])

All inherit timestamps and id from `BaseDbModel`.

## Pydantic Schemas

Located in `src/server/schemas/admin/` – Create / Update / Read variants for each entity.

- Perform input validation (non-empty strings, URL format, list trimming).
- `Update` schemas include `is_empty()` to detect no-op PATCH requests.

## Repositories & Services

Repositories and services exist with placeholder methods returning `Err(NotImplementedError)`.
Files:

- `src/database/repository/admin/*_repository.py`
- `src/service/admin/*_service.py`

## Authentication Stub

`require_admin` (no-op) lives in `src/server/dependencies/admin_auth.py` and is applied to every admin route. Real JWT role/claim verification will replace this in the auth ticket.

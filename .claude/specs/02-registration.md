# Spec: Registration

## Overview

This step wires up the user registration backend so visitors can create an account. The `/register` template and form already exist from the frontend shell — this feature adds the POST handler that validates input, hashes the password, inserts the user into the database, and redirects to login on success. Registration is the first piece of the auth system and must be in place before login, logout, or any authenticated feature can work.

## Depends on

- **Step 01 — Database Setup**: the `users` table and `get_db()` must exist.

## Routes

- `POST /register` — validates form data, creates user, redirects to `/login` — public

The existing `GET /register` route stays but is updated to accept both methods.

## Database changes

No database changes. The `users` table already has the required columns (`name`, `email`, `password_hash`, `created_at`).

## Templates

- **Create:** none
- **Modify:**
  - `templates/register.html` — preserve submitted `name` and `email` values in form fields on validation failure (add `value="{{ name }}"` and `value="{{ email }}"`)

## Files to change

- `app.py` — add POST handling to the `/register` route, add `request`, `redirect`, `url_for` imports, set `app.secret_key`
- `templates/register.html` — add value attributes to retain form data on error

## Files to create

None.

## New dependencies

No new dependencies. `werkzeug.security` is already installed and used in `database/db.py`.

## Rules for implementation

- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never interpolate user input into SQL
- Hash passwords with `werkzeug.security.generate_password_hash`; never store plaintext
- Use CSS variables from the design system — never hardcode hex values
- All templates extend `base.html`
- Validate all three fields (name, email, password) are non-empty
- Enforce minimum password length of 8 characters
- Check for duplicate email before INSERT and show a user-friendly error
- On success: redirect to `/login` (do not auto-login)
- On failure: re-render the form with the error message and previously entered name/email (not password)
- Use `app.secret_key` set from an environment variable with a dev fallback

## Definition of done

- [ ] Visiting `/register` still renders the registration form
- [ ] Submitting the form with valid data creates a new row in the `users` table
- [ ] The stored password is hashed (not plaintext)
- [ ] After successful registration, user is redirected to `/login`
- [ ] Submitting with a blank name, email, or password shows an error message
- [ ] Submitting with a password shorter than 8 characters shows an error message
- [ ] Submitting with an already-registered email shows a "already registered" error
- [ ] On validation failure, the name and email fields retain their values
- [ ] The app starts without errors (`python app.py`)

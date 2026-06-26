# Plan: Registration Backend (Step 02)

## Context

The `/register` route currently only handles GET and renders a static form. The spec at `.claude/specs/02-registration.md` calls for wiring up the POST handler so users can create accounts. The `users` table already exists (from Step 01), the form template is complete with error display support, and `werkzeug` is already installed. This is a two-file change: `app.py` gets the POST handler, and `templates/register.html` gets value retention on error.

---

## Changes

### 1. `app.py`

**Imports to update (line 1):**
```python
import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from database.db import get_db, init_db, seed_db
```

**Secret key — add after `app = Flask(__name__)` (line 4):**
```python
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
```

**Replace the `/register` route (lines 20–22) with:**
```python
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not name or not email or not password:
        return render_template("register.html",
                               error="All fields are required.",
                               name=name, email=email)

    if len(password) < 8:
        return render_template("register.html",
                               error="Password must be at least 8 characters.",
                               name=name, email=email)

    db = get_db()
    existing = db.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    if existing:
        db.close()
        return render_template("register.html",
                               error="An account with that email already exists.",
                               name=name, email=email)

    db.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, generate_password_hash(password)),
    )
    db.commit()
    db.close()
    return redirect(url_for("login"))
```

---

### 2. `templates/register.html`

Add `value` attributes to retain submitted data on validation failure. The password field must stay blank (do not retain).

- Name input: add `value="{{ name or '' }}"`
- Email input: add `value="{{ email or '' }}"`

Current name input (line 23–25):
```html
<input type="text" id="name" name="name"
       class="form-input" placeholder="Nitish Kumar"
       required autofocus>
```
Updated:
```html
<input type="text" id="name" name="name"
       class="form-input" placeholder="Nitish Kumar"
       value="{{ name or '' }}" required autofocus>
```

Current email input (line 28–30):
```html
<input type="email" id="email" name="email"
       class="form-input" placeholder="nitish@example.com"
       required>
```
Updated:
```html
<input type="email" id="email" name="email"
       class="form-input" placeholder="nitish@example.com"
       value="{{ email or '' }}" required>
```

---

## Key reuses

- `get_db()` from `database/db.py` — provides `sqlite3.Row`-enabled connection with foreign keys enabled
- `generate_password_hash` from `werkzeug.security` — already used in `seed_db()`; import directly in `app.py`
- `.auth-error` CSS class in `register.html` — already wired to the `error` template variable; no CSS changes needed

---

## Verification

1. Start the app: `python app.py`
2. Visit `http://localhost:5001/register` — form renders
3. Submit with all fields blank → error "All fields are required." appears; form stays on `/register`
4. Submit with a 5-character password → error about minimum length
5. Submit with the demo email `demo@spendly.com` → "already exists" error
6. Submit with valid new data (e.g., name=Test User, email=test@test.com, password=password123) → redirected to `/login`
7. Check the DB: `sqlite3 expense_tracker.db "SELECT name, email, password_hash FROM users WHERE email='test@test.com';"` — row present, password_hash starts with `scrypt:` or `pbkdf2:`
8. On a validation failure (e.g., duplicate email), confirm name and email fields retain their submitted values
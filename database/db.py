import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "expense_tracker.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id),
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if count > 0:
        conn.close()
        return

    now = datetime.now()
    year = now.year
    month = now.month

    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
    )
    user_id = cursor.lastrowid

    expenses = [
        (user_id, 12.50, "Food", f"{year}-{month:02d}-01", "Lunch at cafe"),
        (user_id, 45.00, "Transport", f"{year}-{month:02d}-03", "Weekly bus pass"),
        (user_id, 120.00, "Bills", f"{year}-{month:02d}-05", "Electricity bill"),
        (user_id, 35.00, "Health", f"{year}-{month:02d}-08", "Pharmacy"),
        (user_id, 25.00, "Entertainment", f"{year}-{month:02d}-10", "Movie tickets"),
        (user_id, 60.00, "Shopping", f"{year}-{month:02d}-12", "New headphones"),
        (user_id, 15.00, "Other", f"{year}-{month:02d}-15", "Gift for a friend"),
        (user_id, 9.75, "Food", f"{year}-{month:02d}-18", "Coffee and pastry"),
    ]
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses,
    )
    conn.commit()
    conn.close()

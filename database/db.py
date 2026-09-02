"""SQLite data layer for Spendly.

get_db()   — returns a SQLite connection with row_factory and foreign keys enabled
init_db()  — creates all tables using CREATE TABLE IF NOT EXISTS
seed_db()  — inserts sample data for development
"""

import sqlite3
from pathlib import Path

from werkzeug.security import generate_password_hash

DB_PATH = Path(__file__).resolve().parent / "expense_tracker.db"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL,
    email         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS expenses (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    amount      REAL NOT NULL CHECK (amount > 0),
    description TEXT NOT NULL,
    category    TEXT NOT NULL CHECK (category IN (
                    'Food', 'Transport', 'Housing', 'Utilities',
                    'Entertainment', 'Health', 'Shopping', 'Other'
                )),
    date        TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
"""

# Demo dev data. Password for both accounts is "password123".
DEMO_USERS = [
    {
        "name": "Ada Lovelace",
        "email": "ada@example.com",
        "password": "password123",
        "expenses": [
            (42.10, "Groceries at Trader Joe's", "Food", "2026-08-05"),
            (15.00, "Metro card top-up", "Transport", "2026-08-07"),
            (1200.00, "September rent", "Housing", "2026-08-01"),
            (60.00, "Electricity bill", "Utilities", "2026-08-15"),
            (35.50, "Movie night", "Entertainment", "2026-08-20"),
            (89.99, "New running shoes", "Shopping", "2026-08-28"),
        ],
    },
    {
        "name": "Grace Hopper",
        "email": "grace@example.com",
        "password": "password123",
        "expenses": [
            (28.75, "Lunch with team", "Food", "2026-08-10"),
            (55.00, "Gas fill-up", "Transport", "2026-08-12"),
            (18.00, "Streaming subscription", "Entertainment", "2026-08-18"),
            (95.00, "Dentist copay", "Health", "2026-08-22"),
            (110.00, "Internet bill", "Utilities", "2026-09-01"),
        ],
    },
]


def get_db():
    """Return a new SQLite connection with dict-like rows and FK enforcement on."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create tables if they don't already exist."""
    conn = get_db()
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()


def seed_db():
    """Insert demo users + expenses. Safe to call repeatedly (no duplicates)."""
    conn = get_db()
    for user in DEMO_USERS:
        cur = conn.execute(
            "INSERT OR IGNORE INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (user["name"], user["email"], generate_password_hash(user["password"])),
        )
        if cur.rowcount == 0:
            continue  # user already seeded — skip to avoid duplicating their expenses
        user_id = cur.lastrowid
        conn.executemany(
            "INSERT INTO expenses (user_id, amount, description, category, date) "
            "VALUES (?, ?, ?, ?, ?)",
            [(user_id, *e) for e in user["expenses"]],
        )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    seed_db()
    print(f"Database ready at {DB_PATH}")

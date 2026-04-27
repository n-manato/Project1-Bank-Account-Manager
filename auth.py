"""User authentication utilities for the Bank Account Manager."""

from __future__ import annotations

import csv
import hashlib
import os
from pathlib import Path


USERS_FILE: str = "users.csv"


def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    """
    Hash a password with a salt.

    Args:
        password: The plain text password.
        salt: The salt value. A new salt is created if this is None.

    Returns:
        A tuple containing the salt and hashed password.
    """
    if salt is None:
        salt = os.urandom(16).hex()

    password_hash = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return salt, password_hash


def load_users(filename: str = USERS_FILE) -> dict[str, dict[str, str]]:
    """
    Load users from a CSV file.

    Args:
        filename: The user CSV file name.

    Returns:
        A dictionary of users.
    """
    path = Path(filename)
    if not path.exists():
        return {}

    users: dict[str, dict[str, str]] = {}

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            username = row.get("username", "").strip()
            if username:
                users[username.lower()] = {
                    "username": username,
                    "salt": row.get("salt", ""),
                    "password_hash": row.get("password_hash", ""),
                }

    return users


def save_users(
    users: dict[str, dict[str, str]],
    filename: str = USERS_FILE,
) -> None:
    """
    Save users to a CSV file.

    Args:
        users: The users to save.
        filename: The user CSV file name.
    """
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["username", "salt", "password_hash"],
        )
        writer.writeheader()

        for user in users.values():
            writer.writerow(user)


def register_user(username: str, password: str) -> tuple[bool, str]:
    """
    Register a new user.

    Args:
        username: The new username.
        password: The new password.

    Returns:
        A tuple containing success status and a message.
    """
    clean_username = username.strip()

    if not clean_username:
        return False, "Username cannot be empty."

    if not password:
        return False, "Password cannot be empty."

    if len(password) < 4:
        return False, "Password must be at least 4 characters."

    users = load_users()

    if clean_username.lower() in users:
        return False, "This username already exists."

    salt, password_hash = hash_password(password)
    users[clean_username.lower()] = {
        "username": clean_username,
        "salt": salt,
        "password_hash": password_hash,
    }

    save_users(users)
    return True, "User registered successfully."


def authenticate_user(username: str, password: str) -> tuple[bool, str]:
    """
    Check whether a username and password are correct.

    Args:
        username: The username.
        password: The password.

    Returns:
        A tuple containing success status and a message.
    """
    clean_username = username.strip()

    if not clean_username or not password:
        return False, "Please enter username and password."

    users = load_users()
    user = users.get(clean_username.lower())

    if user is None:
        return False, "User not found."

    salt = user["salt"]
    saved_hash = user["password_hash"]
    _, entered_hash = hash_password(password, salt)

    if entered_hash != saved_hash:
        return False, "Incorrect password."

    return True, "Login successful."

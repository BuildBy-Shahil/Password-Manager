# 🔐 Password Manager

A desktop Password Manager built with **Python**, **PyQt6**, **SQLite**, and **Cryptography (Fernet)**.  
The application securely stores website credentials by encrypting passwords before saving them to the database.

---

## Features

- Store website credentials securely
- AES encryption using `cryptography.fernet`
- Search by website name
- Search by username/email
- Display all saved accounts
- Copy decrypted passwords to clipboard
- Edit existing credentials
- Delete saved credentials
- Random password generator
- SQLite database storage
- Error logging

---

## Technologies Used

- Python
- PyQt6
- SQLite
- Cryptography (Fernet)
- Pyperclip

---

## Project Structure

```text
PasswordManager/
│
├── manager.py
├── log.py
├── pass_generator.py
├── mainwindow.ui
├── secret.key          # Auto-generated encryption key
├── README.md
└── requirements.txt
```

---

## Database Schema

| Column | Type |
|--------|------|
| id | INTEGER PRIMARY KEY AUTOINCREMENT |
| site | TEXT | NOT NULL
| user_email | TEXT | NOT NULL
| password | TEXT (Encrypted) | NOT NULL

---

## How It Works

1. User enters website, username/email, and password.
2. Password is encrypted using **Fernet** before storage.
3. Encrypted credentials are stored in an SQLite database.
4. Passwords are decrypted only when the user chooses to copy them.
5. Users can search, update, or delete saved credentials.

---

## Security

- Passwords are **never stored in plain text**.
- Each password is encrypted before being saved.
- Encryption uses a locally generated `secret.key`.
- The encryption key is generated automatically on first launch.

> **Note:** If `secret.key` is deleted, previously stored passwords cannot be decrypted.

---

## Requirements

```bash
pip install PyQt6 cryptography pyperclip
```

## Future Improvements

- Master password authentication
- Password strength checker
- Import/Export encrypted database
- Backup and restore functionality
- Dark/Light theme
- Password expiration reminders
- Secure key management using a master password

---

## Author

Shahil

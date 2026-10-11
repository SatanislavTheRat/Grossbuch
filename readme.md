\# Grossbuch



Grossbuch is a desktop bookkeeping application that I use for my own day-to-day income and expense tracking.



It is also the project I started learning Python with. As my skills grew, the application evolved with them: from a simple JSON-based program into a SQLite-backed desktop application with automated tests and a standalone Windows build.



The project includes transaction tracking, category management, filtering, financial statistics, and persistent local data storage.



\## Features



\- Add income and expense operations with date, amount, description, and category

\- Create and manage custom categories

\- Rename and merge categories without losing existing operations

\- Prevent deletion of categories that are already in use

\- Filter operations by date range and category

\- View income, expenses, balance, and number of records

\- View top income and expense categories for a selected date range

\- Store application data in a local SQLite database

\- Create automatic timestamped SQLite backups and keep only the most recent copies



\## Current Limitations



Grossbuch is currently a local, single-user desktop application.



\- Existing operations cannot yet be edited or deleted through the UI

\- The local database is not encrypted



\## Roadmap



Possible future development includes:



\- Editing and deleting existing operations

\- Database encryption and improved data protection

\- API-based access to Grossbuch data

\- Telegram bot integration for adding expenses directly from a phone

\- Mobile client synchronized with the main database

\- AI-assisted receipt recognition with automatic extraction of amount, date, description, and category

\- Automatic creation of operations from recognized receipts



\## Tech Stack



\- Python

\- SQLite

\- CustomTkinter

\- tksheet

\- tkcalendar

\- Pillow

\- pytest

\- PyInstaller

\- Git



\## Project Structure



```text

GrossbuchUI/

├── main.py              # Application entry point and GUI

├── grossbuch.py         # Business logic and financial operations

├── database.py          # SQLite database access layer

├── styles.py            # GUI styles and appearance

├── grossbuch.db         # Demo SQLite database with sample data

├── requirements.txt     # Python dependencies

└── tests/

\\\\\\\\\\\\\\\&#x20;   ├── test\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_grossbuch.py

\\\\\\\\\\\\\\\&#x20;   ├── test\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_database.py

\\\\\\\\\\\\\\\&#x20;   └── test\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_grossbuch.db

```

The application separates its main responsibilities: the GUI is handled in `main.py`, business logic lives in `grossbuch.py`, SQLite operations are isolated in `database.py`, and visual styling is kept in `styles.py`. This structure was introduced gradually as the project grew and was migrated from JSON file storage to SQLite.


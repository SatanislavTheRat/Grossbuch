# Grossbuch



Grossbuch is a desktop bookkeeping application that I use for my own day-to-day income and expense tracking.



It is also the project I started learning Python with. As my skills grew, the application evolved with them: from a simple JSON-based program into a SQLite-backed desktop application with automated tests and a standalone Windows build.



The project includes transaction tracking, category management, filtering, financial statistics, and persistent local data storage.

## Screenshots

### Operations
![Transaction list](screenshots/operations.png)

### Statistics
![Financial statistics](screenshots/statistics.png)

### Categories
![Category management](screenshots/categories.png)

## Download and Run (Windows)

Python installation is not required.

1. Open the [Releases page](https://github.com/SatanislavTheRat/Grossbuch/releases).
2. Download `Grossbuch.zip` from the Assets section.
3. Extract the entire archive.
4. Open the extracted folder and run `main.exe`.

Keep `logo.png` and `icon.ico` alongside the executable.

### Demo Data

The included `grossbuch.db` contains fictional transactions for exploring the application.

To start your own records:
1. Close Grossbuch.
2. Delete the demo `grossbuch.db` from the application folder.
3. Launch Grossbuch again. A new, empty database will be created automatically.

Only delete the demo database. Once you start adding your own transactions, this file contains your personal records.

## Features



- Add income and expense operations with date, amount, description, and category

- Create and manage custom categories

- Rename and merge categories without losing existing operations

- Prevent deletion of categories that are already in use

- Filter operations by date range and category

- View income, expenses, balance, and number of records

- View top income and expense categories for a selected date range

- Store application data in a local SQLite database

- Create automatic timestamped SQLite backups and keep only the most recent copies



## Current Limitations



Grossbuch is currently a local, single-user desktop application.



- Existing operations cannot yet be edited or deleted through the UI

- The local database is not encrypted



## Roadmap



Possible future development includes:



- Editing and deleting existing operations

- Database encryption and improved data protection

- API-based access to Grossbuch data

- Telegram bot integration for adding expenses directly from a phone

- Mobile client synchronized with the main database

- AI-assisted receipt recognition with automatic extraction of amount, date, description, and category

- Automatic creation of operations from recognized receipts


## Tech Stack


- Python

- SQLite

- CustomTkinter

- tksheet

- tkcalendar

- Pillow

- pytest

- PyInstaller

- Git

## Project Structure



```text

GrossbuchUI/
├── main.py              # Application entry point and GUI
├── grossbuch.py         # Business logic and financial operations
├── database.py          # SQLite database access layer
├── styles.py            # GUI styles and appearance
├── grossbuch.db         # Demo SQLite database with sample data
├── requirements.txt     # Python dependencies
└── tests/
    ├── test_grossbuch.py
    ├── test_database.py
    └── test_grossbuch.db

```

The application separates its main responsibilities: the GUI is handled in `main.py`, business logic lives in `grossbuch.py`, SQLite operations are isolated in `database.py`, and visual styling is kept in `styles.py`. This structure was introduced gradually as the project grew and was migrated from JSON file storage to SQLite.

## Run from Source (Windows)

Install Python and Git, then open a terminal.

### 1. Clone the repository

```powershell
git clone https://github.com/SatanislavTheRat/Grossbuch.git
cd Grossbuch
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Install dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Start the application

Run from the project root folder:

```powershell
.\.venv\Scripts\python.exe main.py
```

## Run Tests

From the project root folder, using the same virtual environment:

```powershell
.\.venv\Scripts\python.exe -m pip install pytest
.\.venv\Scripts\python.exe -m pytest
```

Tests cover database operations and business logic, using temporary database copies to avoid modifying the original data.

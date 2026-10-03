import sqlite3

class Database:
    def __init__(self, database_file):
        self.database_file = database_file
        self.connection = sqlite3.connect(database_file)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS operations (
                id INTEGER PRIMARY KEY,
                date TEXT,
                description TEXT,
                category_id INTEGER,
                amount INTEGER,
                FOREIGN KEY(category_id) REFERENCES categories(id)
                ON DELETE RESTRICT
            )
            """
        )
        self.connection.commit()

    def get_category_id(self, name):
        name=name.strip().casefold()
        self.cursor.execute("SELECT id, name FROM categories")
        for row in self.cursor.fetchall():
            if row["name"].casefold() == name:
                return row["id"]
        return None

    def category_exists(self, category):
        return self.get_category_id(category) is not None

    def add_category(self, name):
        name=name.strip()
        if name and not self.category_exists(name):
            self.cursor.execute(
                "INSERT INTO categories (name) VALUES (?)",
                (name,)
            )
            self.connection.commit()
            return True
        return False

    def add_operation(self,operation_date, amount, description, category_name):
        category_id = self.get_category_id(category_name)
        if category_id is None:
            return False
        self.cursor.execute(
            "INSERT INTO operations (date, description, category_id, amount) "
            "VALUES (?, ?, ?, ?)",
            (operation_date.isoformat(), description, category_id, amount)
        )
        self.connection.commit()
        return True

    def is_category_used(self, category_name):
        category_id = self.get_category_id(category_name)
        if category_id is None:
            return False
        self.cursor.execute(
            "SELECT id FROM operations WHERE category_id = ? LIMIT 1",
            (category_id,)
        )
        return self.cursor.fetchone() is not None

    def delete_category(self, category_name):
        delete_id = self.get_category_id(category_name)
        if delete_id is None:
            return False
        self.cursor.execute(
            "SELECT id FROM operations WHERE category_id = ? LIMIT 1",(delete_id,)
        )
        row = self.cursor.fetchone()
        if row is None:
            try:
                self.cursor.execute(
                    "DELETE FROM categories WHERE id = ?",
                    (delete_id,)
                )
                self.connection.commit()
                return True
            except sqlite3.IntegrityError:
                self.connection.rollback()
                return False
        return False


    def rename_category(self, old_name, new_name):
        old_name = old_name.strip()
        new_name = new_name.strip()
        old_id = self.get_category_id(old_name)
        if old_id is None or new_name == "" or self.category_exists(new_name):
            return False
        self.cursor.execute(
            "UPDATE categories SET name = ? WHERE id = ?",
            (new_name, old_id)
        )
        self.connection.commit()
        return True


    def merge_categories(self, cat, into):
        cat_id = self.get_category_id(cat)
        into_id = self.get_category_id(into)
        try:
            if cat_id is not None and into_id is not None and cat_id != into_id:
                self.cursor.execute("""
                UPDATE operations SET category_id = ? WHERE category_id = ?""",(into_id, cat_id))
                self.cursor.execute("DELETE FROM categories WHERE id = ?",(cat_id,))
                self.connection.commit()
                return True
        except sqlite3.IntegrityError:
            self.connection.rollback()
            return False
        return False




    def get_categories(self):
        self.cursor.execute("SELECT * FROM categories")
        categories = []
        for category in self.cursor.fetchall():
            categories.append(category["name"])
        return categories

    def get_operations(self):
        self.cursor.execute("""
            SELECT
                operations.id,
                operations.date,
                operations.description,
                operations.amount,
                categories.name AS category
            FROM operations
            JOIN categories
                ON operations.category_id = categories.id
            ORDER BY operations.date, operations.id
        """)
        operations = []
        for row in self.cursor.fetchall():
            operation = {
                "date": row["date"],
                "description": row["description"],
                "amount": row["amount"],
                "category": row["category"]
            }
            operations.append(operation)
        return operations








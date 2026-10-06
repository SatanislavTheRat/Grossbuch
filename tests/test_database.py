from tkinter.constants import INSERT

import pytest
from database import Database
from datetime import date
import sqlite3

@pytest.fixture
def temp_db(tmp_path):
    database_file = tmp_path / "test.db"
    db = Database(database_file)
    yield db
    db.connection.close()



def test_add_category(temp_db):
    assert temp_db.add_category("new") == True
    assert "new" in temp_db.get_categories()



def test_add_category_duplicate(temp_db):
    assert temp_db.add_category("new") is True
    assert temp_db.add_category("new") is False



def test_add_operation(temp_db):
    temp_db.add_category("Cigarettes")
    assert temp_db.add_operation(
        date.today(),
        100,
        "Luckies",
        "Cigarettes"
    ) is True
    operation = {
        "date": date.today().isoformat(),
        "description": "Luckies",
        "amount": 100,
        "category": "Cigarettes"
    }
    assert operation in temp_db.get_operations()



def test_add_operation_with_missing_category(temp_db):
    assert temp_db.add_operation(
        date.today(),
        100,
        "Luckies",
        "Cigarettes"
    ) is False
    assert temp_db.get_operations() == []



def test_delete_used_category(temp_db):
    temp_db.add_category("Cigarettes")
    temp_db.add_operation(
        date.today(),
        100,
        "Luckies",
        "Cigarettes"
    )
    assert temp_db.delete_category("Cigarettes") is False
    assert "Cigarettes" in temp_db.get_categories()



def test_rename_category(temp_db):
    temp_db.add_category("Food")
    temp_db.add_operation(
        date.today(),
        -100,
        "Groceries",
        "Food"
    )
    assert temp_db.rename_category("Food", "Groceries") is True
    assert "Food" not in temp_db.get_categories()
    assert "Groceries" in temp_db.get_categories()
    operations = temp_db.get_operations()
    assert operations[0]["category"] == "Groceries"


def test_merge_categories(temp_db):
    temp_db.add_category("Food")
    temp_db.add_category("Restaurants")
    temp_db.add_operation(
        date.today(),
        -300,
        "Pizza",
        "Restaurants"
    )
    temp_db.add_operation(
        date.today(),
        -500,
        "Groceries",
        "Food"
    )
    assert temp_db.merge_categories("Restaurants", "Food") is True
    assert "Food" in temp_db.get_categories()
    assert "Restaurants" not in temp_db.get_categories()
    operations = temp_db.get_operations()
    assert operations[0]["category"] == "Food"
    assert operations[1]["category"] == "Food"



def test_foreign_key_constraint(temp_db):
    with pytest.raises(sqlite3.IntegrityError):
        temp_db.cursor.execute(
            "INSERT INTO operations (date, description, category_id, amount) "
             "VALUES (?, ?, ?, ?)",
            ("2026-02-02", "Something", 666, 666)
        )


def test_delete_unused_category(temp_db):
    temp_db.add_category("Unused")
    assert temp_db.delete_category("Unused") is True
    assert "Unused" not in temp_db.get_categories()

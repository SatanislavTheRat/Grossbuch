from grossbuch import Grossbuch
from datetime import date
import shutil
import pytest
from database import Database


@pytest.fixture
def filled_grossbuch(tmp_path):
    database_file = tmp_path / "test.db"
    shutil.copy("tests/test_grossbuch.db", database_file)
    db = Database(database_file)
    grossbuch = Grossbuch(db)
    return grossbuch

@pytest.fixture
def temp_grossbuch(tmp_path):
    database_file = tmp_path / "test.db"
    db = Database(database_file)
    return Grossbuch(db)


def test_calculate_summary(filled_grossbuch):
    operations = filled_grossbuch.filter_by_date(
        date(2026,10,3),
        date(2026,10,4),
    )
    result = filled_grossbuch.calculate_summary(operations)

    assert result["income"] == 0
    assert result["expenses"] == 1180
    assert result["balance"] == -1180
    assert result["records"] == 4


def test_filter_by_date(filled_grossbuch):
    operations = filled_grossbuch.filter_by_date(
        date(2026,9,1),
        date(2026,9,3),
    )
    assert operations[0].date == date(2026,9,1)
    assert operations[-1].date == date(2026,9,3)
    assert len(operations) == 7


def test_top_income_by_category(filled_grossbuch):
    assert filled_grossbuch.top_income_by_category(
        date(2026,9,1),
        date(2026,9,3))[0] == ("Salary", [38000, 1])


def test_add_operation(filled_grossbuch):
    length = filled_grossbuch.calculate_summary()["records"]
    balance = filled_grossbuch.calculate_summary()["balance"]
    result = filled_grossbuch.add_operation(
        -145,
        "Luckies",
        "Cigarettes",
        date(2026, 10, 5))
    assert result is True
    assert filled_grossbuch.history[-1].description == "Luckies"
    assert len(filled_grossbuch.history) == length+1
    assert filled_grossbuch.calculate_summary()["records"] == length + 1
    assert filled_grossbuch.balance == balance - 145
    assert filled_grossbuch.calculate_summary()["balance"] == balance - 145

def test_delete_category_in_use(filled_grossbuch):
    assert filled_grossbuch.delete_category("Alcohol") is False

def test_delete_nonexisting_category(filled_grossbuch):
    assert filled_grossbuch.delete_category("Nonexisting") is False

def test_rename_category(filled_grossbuch):
    count=len(filled_grossbuch.filter_by_category("Salary"))
    filled_grossbuch.rename_category("Salary","Income")
    assert len(filled_grossbuch.filter_by_category("Salary")) == 0
    assert len(filled_grossbuch.filter_by_category("Income")) == count
    reloaded_db = Database(filled_grossbuch.db.database_file)
    reloaded = Grossbuch(reloaded_db)
    assert len(reloaded.filter_by_category("Salary")) == 0
    assert len(reloaded.filter_by_category("Income")) == count

def test_merge_categories(filled_grossbuch):
    count=len(filled_grossbuch.filter_by_category("Restaurants"))+len(filled_grossbuch.filter_by_category("Food"))
    filled_grossbuch.merge_categories("Restaurants","Food")
    assert len(filled_grossbuch.filter_by_category("Restaurants")) == 0
    assert len(filled_grossbuch.filter_by_category("Food")) == count
    reloaded_db = Database(filled_grossbuch.db.database_file)
    reloaded = Grossbuch(reloaded_db)
    assert len(reloaded.filter_by_category("Restaurants")) == 0
    assert len(reloaded.filter_by_category("Food")) == count

def test_delete_unused_categories(temp_grossbuch):
    temp_grossbuch.add_category("unused")
    temp_grossbuch.delete_category("unused")
    assert "unused" not in temp_grossbuch.categories

def test_add_category_once(temp_grossbuch):
    temp_grossbuch.add_category("new")
    assert "new" in temp_grossbuch.categories
    temp_grossbuch.add_category("new")
    assert temp_grossbuch.categories.count("new") == 1

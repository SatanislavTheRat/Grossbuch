from Grossbuch import Operation,Grossbuch
from datetime import date
import shutil
import pytest
from Grossbuch import CategoryInUseError
from Grossbuch import CategoryDoesNotExistError

test_grossbuch = Grossbuch(
    "tests/test_history.json",
    "tests/test_categories.json",
    "tests/test_backups"
)

def test_operation_to_dict():
    operation = Operation(date(2026,8,22),
                          -145,
                          "Luckies",
                          "Sigarettes",
                          0)
    result = operation.to_dict()
    assert result["balance"] == 0


def test_calculate_summary():
    operations = test_grossbuch.filter_by_date(
        date(2026,7,6),
        date(2026,7,6),
    )
    result = test_grossbuch.calculate_summary(operations)

    assert result["income"] == 4542
    assert result["expenses"] == 2241
    assert result["balance"] == 2301
    assert result["records"] == 5


def test_filter_by_date():
    operations = test_grossbuch.filter_by_date(
        date(2026,7,8),
        date(2026,7,10),
    )
    assert operations[0].date == date(2026,7,8)
    assert operations[-1].date == date(2026,7,10)
    assert len(operations) == 13


def test_top_income_by_category():
    assert test_grossbuch.top_income_by_category(
        date(2026,7,6),
        date(2026,7,12))[0] == ("Family", [7102, 2])


@pytest.fixture
def temp_grossbuch(tmp_path):
    history = tmp_path / "history.json"
    categories = tmp_path / "categories.json"
    backups = tmp_path / "backups"

    shutil.copy("tests/test_history.json", history)
    shutil.copy("tests/test_categories.json", categories)

    return Grossbuch(history, categories, backups)



def test_add_operation(temp_grossbuch):

    length = temp_grossbuch.calculate_summary()["records"]
    balance = temp_grossbuch.calculate_summary()["balance"]

    temp_grossbuch.add_operation(
        date(2026, 8, 23),
        -145,
        "Luckies",
        "Sigarettes")


    assert temp_grossbuch.history[-1].description == "Luckies"
    assert len(temp_grossbuch.history) == length+1
    assert temp_grossbuch.calculate_summary()["records"] == length + 1
    assert temp_grossbuch.balance == balance - 145
    assert temp_grossbuch.calculate_summary()["balance"] == balance - 145

def test_delete_category_in_use(temp_grossbuch):

    with pytest.raises(CategoryInUseError):
        temp_grossbuch.delete_category("Alcohol")

def test_delete_nonexisting_category(temp_grossbuch):
    with pytest.raises(CategoryDoesNotExistError):
        temp_grossbuch.delete_category("Nonexisting")

def test_rename_category(temp_grossbuch):
    count=len(temp_grossbuch.filter_by_category("Alcohol"))
    temp_grossbuch.rename_category("Alcohol","Booze")
    assert len(temp_grossbuch.filter_by_category("Alcohol")) == 0
    assert len(temp_grossbuch.filter_by_category("Booze")) == count
    reloaded = Grossbuch(
        temp_grossbuch.history_file,
        temp_grossbuch.categories_file,
        temp_grossbuch.backup_path
    )
    assert len(reloaded.filter_by_category("Alcohol")) == 0
    assert len(reloaded.filter_by_category("Booze")) == count

def test_merge_categories(temp_grossbuch):
    count=len(temp_grossbuch.filter_by_category("Alcohol"))+len(temp_grossbuch.filter_by_category("Drugs"))
    temp_grossbuch.merge_categories("Alcohol","Drugs")
    assert len(temp_grossbuch.filter_by_category("Alcohol")) == 0
    assert len(temp_grossbuch.filter_by_category("Drugs")) == count
    reloaded = Grossbuch(
        temp_grossbuch.history_file,
        temp_grossbuch.categories_file,
        temp_grossbuch.backup_path
    )
    assert len(reloaded.filter_by_category("Alcohol")) == 0
    assert len(reloaded.filter_by_category("Drugs")) == count

def test_delete_unused_categories(temp_grossbuch):
    temp_grossbuch.add_category("unused")
    temp_grossbuch.delete_category("unused")
    assert "unused" not in temp_grossbuch.categories

def test_add_category_once(temp_grossbuch):
    temp_grossbuch.add_category("new")
    assert "new" in temp_grossbuch.categories
    temp_grossbuch.add_category("new")
    count = 0
    for category in temp_grossbuch.categories:
        if category == "new":
            count += 1
    assert count == 1

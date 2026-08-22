from datetime import date,datetime
import json
import os
import shutil

class CategoryInUseError(Exception):
    pass
class CategoryDoesNotExistError(Exception):
    pass


class Operation:
    def __init__(self, date, amount, description, category, balance=0):
        self.date = date
        self.amount = amount
        self.description = description
        self.category = category
        self.balance = balance

    def to_dict(self):
        return {
            "date": self.date.isoformat(),
            "amount": self.amount,
            "description": self.description,
            "category": self.category,
            "balance": self.balance
        }

    def text(self):
        return (
            f"\n{self.date.strftime('%d.%m.%Y, %A')}\n"
            f"{self.description}, {self.amount:+} ₴\n "
            f"category: {self.category}\n"
        )

    def get_amount(self):
        return self.amount

    def get_category(self):
        return self.category


class Grossbuch:
    def __init__(self, history_file, categories_file, backup_path):

        self.history_file = history_file
        self.categories_file = categories_file
        self.backup_path = backup_path

        self.history = []

        self.categories = [
            "Salary",
            "Food",
            "Restaurants",
            "Transportation",
            "Housing",
            "Utilities",
            "Medicine",
            "Clothes",
            "Education",
            "Entertainment",
            "Travel",
            "Gifts",
            "Pets",
            "Taxes",
            "Savings",
            "Investments",
            "Subscriptions",
            "Home Stuff",
            "Electronics",
            "Personal Care",
            "Alcohol",
            "Cigarettes",
            "Other"
        ]

        self.balance = 0

        self.ensure_file_exists()
        self.backup()
        self.load_history()
        self.load_categories()
        self.update_categories()

    def backup(self):
        if not os.path.exists(self.backup_path):
            os.makedirs(self.backup_path)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        shutil.copy(self.history_file, os.path.join(self.backup_path,f"{timestamp}history.json"))
        shutil.copy(self.categories_file, os.path.join(self.backup_path,f"{timestamp}categories.json"))


    def ensure_file_exists(self):
        if not os.path.exists(self.history_file):
            with open(self.history_file, "w") as history:
                history.write("[]")

        if not os.path.exists(self.categories_file):
            with open(self.categories_file, "w") as categories:
                for category in self.categories:
                    categories.write(f"{category}\n")

    def text_list(self):
        current_date=0
        today_list=""
        today_total = 0
        count = 0
        result = []
        for operation in self.history:


            amount = f"{operation.amount:+,}".replace(",", " ")

            if operation.date == current_date:
                today_list+=(f"\n{operation.description}, {amount} ₴\n"
                                  f"category: {operation.category}\n")
                today_total += operation.amount
                count += 1

            else:

                if today_list:
                    today_list+=(f"\n{count} operations, totaling{today_total:+,} ₴\n".replace(",", " "))
                    result.append([today_list])

                today_list = ""
                count = 0
                today_total = 0
                current_date = operation.date

                today_list+=(f"{operation.date.strftime('%d.%m.%Y, %A').upper()}\n\n"
                                  f"{operation.description}, {amount} ₴\n"
                                  f"category: {operation.category}\n")
                today_total += operation.amount
                count += 1

        if today_list:
            today_list+=(f"\n{count} operations, totaling  {today_total:+,} ₴".replace(",", " "))
            result.append([today_list])
        return result

    def load_categories(self):
        self.categories = []

        with open(self.categories_file, "r") as file:
            for line in file:
                self.categories.append(line.strip())

    def save_categories(self):
        with open(self.categories_file, "w") as file:
            for category in self.categories:
                file.write(f"{category}\n")

    def add_category(self, category):
        if category in self.categories:
            return False

        self.categories.append(category)
        self.save_categories()
        return True

    def rename_category(self, old, new):
        for operation in self.history:
            if operation.category == old:
                operation.category = new

        self.categories.remove(old)
        self.categories.append(new)

        self.save_history()
        self.save_categories()

    def delete_category(self, category):
        if category not in self.categories:
            raise CategoryDoesNotExistError(category)

        if self.is_used(category):
            raise CategoryInUseError(f"Category {category} is used")

        self.categories.remove(category)
        self.save_categories()

    def merge_categories(self, old, new):
        for operation in self.history:
            if operation.category == old:
                operation.category = new

        self.delete_category(old)
        self.save_history()

    def update_categories(self):
        for operation in self.history:
            if operation.category not in self.categories:
                self.add_category(operation.category)

    def is_used(self, category):
        for operation in self.history:
            if operation.category == category:
                return True

        return False

    def categories_text(self):
        text = ""

        for category in self.categories:
            text += f"{category}\n"

        return text

    def load_history(self):
        with open(self.history_file, "a+") as file:
            file.seek(0)
            text = file.read()

            if text == "":
                text = "[]"

            history = json.loads(text)

            for element in history:
                operation = from_dict(element)
                self.balance += operation.amount
                operation.balance = self.balance
                self.history.append(operation)

    def save_history(self):
        to_save = []

        for operation in self.history:
            to_save.append(operation.to_dict())

        with open(self.history_file, "w") as file:
            json.dump(to_save, file, ensure_ascii=False, indent=2)

    def show_history(self, start_date=date.min, end_date=date.max):
        found = False

        for operation in self.history:
            if start_date <= operation.date <= end_date:
                operation.show()
                found = True

        return found

    def text(self, start_date=date.min, end_date=date.max):
        text = ""

        for operation in self.history:
            if start_date <= operation.date <= end_date:
                text += (
                    f"{operation.text()}\n"
                    f"Balance: {operation.balance} ₴\n\n"
                )

        return text

    def add_operation(self, date, amount, description, category):
        operation = Operation(
            date,
            amount,
            description,
            category,
            self.balance
        )

        self.balance += operation.amount
        operation.balance = self.balance

        self.history.append(operation)
        self.save_history()

    # -------------------- STATISTICS --------------------

    def first_date(self):
        if not self.history:
            return None

        return self.history[0].date

    def last_date(self):
        if not self.history:
            return None

        return self.history[-1].date

    def filter_by_date(self,start_date=None,end_date=None,operations_list=None):

        if operations_list is None:
            operations_list = self.history

        if start_date is None:
            start_date = self.first_date()

        if end_date is None:
            end_date = self.last_date()

        operations = []

        for operation in operations_list:
            if start_date <= operation.date <= end_date:
                operations.append(operation)

        return operations

    def filter_by_category(self, category, operations_list=None):
        if operations_list is None:
            operations_list = self.history

        operations = []

        for operation in operations_list:
            if operation.category == category:
                operations.append(operation)

        return operations

    def calculate_amount(self, operations):
        total = 0

        for operation in operations:
            total += operation.amount

        return total

    def calculate_summary(self, operations=None):
        if operations is None:
            operations = self.history

        summary = {}
        income = 0
        expenses = 0
        records = 0

        for operation in operations:
            if operation.amount > 0:
                income += operation.amount
            else:
                expenses += -operation.amount

            records += 1

        summary["income"] = income
        summary["expenses"] = expenses
        summary["balance"] = income - expenses
        summary["records"] = records

        return summary

    def sort_by_amount(self, operations, reverse=False):
        return sorted(operations, key=Operation.get_amount, reverse=reverse)


    def top_income_by_category(self, start_date=None, end_date=None):
        operations_list = self.filter_by_date(start_date,end_date,operations_list=self.history)
        categories = {}

        for operation in operations_list:
            if operation.amount > 0:

                if operation.category not in categories:
                    categories[operation.category] = [operation.amount, 1]
                    categories[operation.category][1] = 1
                else:
                    categories[operation.category][0] += operation.amount
                    categories[operation.category][1] += 1

        return sorted(categories.items(), key=lambda x: x[1], reverse=True)

    def top_expenses_by_category(self, start_date=None, end_date=None):
        operations_list = self.filter_by_date(start_date, end_date, operations_list=self.history)
        categories = {}

        for operation in operations_list:
            if operation.amount < 0:

                if operation.category not in categories:
                    categories[operation.category] = [abs(operation.amount), 1]
                    categories[operation.category][1] = 1
                else:
                    categories[operation.category][0] += abs(operation.amount)
                    categories[operation.category][1] += 1

        return sorted(categories.items(), key=lambda x: x[1], reverse=True)


def from_dict(data):
    return Operation(
        date.fromisoformat(data["date"]),
        data["amount"],
        data["description"],
        data["category"],
        data["balance"]
    )
from datetime import date
import json
import os

class CategoryInUseError(Exception):
    pass
class CategoryDoesNotExistError(Exception):
    pass

class Operation:
    def __init__(self,date, amount, description, category, balance=0):
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
        "balance": self.balance}

    def text(self):
        return f"{self.date.strftime("%d.%m.%Y, %A")}\n{self.description}, {self.amount:+} UAH, category: {self.category}"


#####################################################################################################################


class Grossbuch:
    def __init__(self,history_file,categories_file):

        self.history_file = history_file
        self.categories_file = categories_file
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
        self.load_history()
        self.load_categories()
        self.update_categories()

    def ensure_file_exists(self):
        if not os.path.exists(self.history_file):
            with open(self.history_file, "w") as history:
                history.write("[]")
        if not os.path.exists(self.categories_file):
            with open(self.categories_file, "w") as categories:
                for category in self.categories:
                    categories.write(f"{category}\n")


    def load_categories(self):
        self.categories = []
        with open(self.categories_file, "r") as file:
            for line in file:
                self.categories.append(line.strip())

    def save_categories(self):
        with open(self.categories_file, "w") as file:
            for category in self.categories:
                file.write(f"{category}\n")


    def add_category(self,category):
        if category in self.categories:
            return False
        else:
            self.categories.append(category)
            self.save_categories()
            return True

    def rename_category(self,old,new):
        for operation in self.history:
            if operation.category == old:
                operation.category = new
        self.categories.remove(old)
        self.categories.append(new)
        self.save_history()
        self.save_categories()

    def delete_category(self,category):
        if category in self.categories:
            if self.is_used(category):
                raise CategoryInUseError(f"Category {category} is used")
            self.categories.remove(category)
            self.save_categories()
        else:
            raise CategoryDoesNotExistError(category)

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

    def is_used(self,category):
        result = False
        for operation in self.history:
            if operation.category == category:
                result = True
        return result


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

    def show_history(self,start_date=date.min,end_date=date.max):
        found = False
        for operation in self.history:
            if start_date <= operation.date <= end_date:
                operation.show()
                found = True
        return found

    def text(self, start_date=date.min,end_date=date.max):
        text = ""
        for operation in self.history:
            if start_date <= operation.date <= end_date:
                text+=f"{operation.text()}\nBalance: {operation.balance} UAH\n\n"
        return text


    def add_operation(self,date, amount, description, category):
        balance = self.balance
        operation = Operation(date, amount, description, category, balance)
        self.balance += operation.amount
        operation.balance = self.balance
        self.history.append(operation)
        self.save_history()

    def get_statistics(self,category, start_date=date.min,end_date=date.max):
        statistics = {}
        for operation in self.history:
            if start_date <= operation.date <= end_date:
                statistics[category] = 0
                if category == operation.category:
                    statistics[operation.category] += operation.amount
        return statistics

def from_dict(data):
    operation = Operation(date.fromisoformat(data["date"]),
                          data["amount"],
                          data["description"],
                          data["category"],
                          data["balance"])
    return operation
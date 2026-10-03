from datetime import date

DEFAULT_CATEGORIES = [
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


class Operation:
    def __init__(self, date, amount, description, category):
        self.date = date
        self.amount = amount
        self.description = description
        self.category = category

    def get_amount(self):
        return self.amount
    def get_description(self):
        return self.description
    def get_category(self):
        return self.category
    def get_date(self):
        return self.date

    def text(self):
        return (
            f"\n{self.date.strftime('%d.%m.%Y, %A')}\n"
            f"{self.description}, {self.amount:+} ₴\n "
            f"category: {self.category}\n"
        )


class Grossbuch:
    def __init__(self,db):
        self.db=db
        self.history = []
        self.categories = []
        self.balance = 0
        self.load_history()
        self.initialize_categories()

    def initialize_categories(self):
        self.load_categories()

        if not self.categories:
            for category in DEFAULT_CATEGORIES:
                self.db.add_category(category)

            self.load_categories()

    def load_categories(self):
        self.categories = self.db.get_categories()

    def add_category(self, category):
        category = category.strip()
        if self.db.add_category(category):
            self.load_categories()
            return True
        return False

    def rename_category(self, old, new):
        old = old.strip()
        new = new.strip()
        if not old or not new :
            return False
        if self.db.rename_category(old, new):
            self.load_categories()
            self.load_history()
            return True
        return False

    def delete_category(self, category):
        category=category.strip()
        if not category:
            return False
        if self.db.delete_category(category):
            self.load_categories()
            return True
        return False

    def merge_categories(self, cat, into):
        cat = cat.strip()
        into = into.strip()
        if not cat or not into:
            return False
        if self.db.merge_categories(cat, into):
            self.load_categories()
            self.load_history()
            return True
        return False

    def is_used(self, category):
        return self.db.is_category_used(category)

    def load_history(self):
        self.history = []
        self.balance = 0
        operations = self.db.get_operations()
        for operation_data in operations:
            operation = Operation(
                date.fromisoformat(operation_data["date"]),
                operation_data["amount"],
                operation_data["description"],
                operation_data["category"])
            self.history.append(operation)
            self.balance += operation.amount

    def add_operation(self, amount, description, category,operation_date=None):
        if operation_date is None:
            operation_date = date.today()
        description = description.strip()
        category = category.strip()
        if (
                not description
                or not category
                or not isinstance(operation_date, date)
                or not isinstance(amount, int)
                or isinstance(amount, bool)
        ):
            return False
        if self.db.add_operation(operation_date, amount, description, category):
            self.load_history()
            return True
        return False

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
            today_list+=(f"\n{count} operations, totaling {today_total:+,} ₴".replace(",", " "))
            result.append([today_list])
        return result

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

import os
from database import Database
from datetime import datetime

class BudgetTracker:
    def __init__(self):
        self.db = Database()
        self.current_user = None

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        self.clear_screen()
        print("=== Budget Tracker ===")
        if self.current_user:
            print(f"Logged in as: {self.current_user[1]}\n")

    def login_menu(self):
        while True:
            self.print_header()
            print("1. Login")
            print("2. Register")
            print("3. Exit")
            choice = input("\nEnter your choice (1-3): ")

            if choice == '1':
                self.login()
            elif choice == '2':
                self.register()
            elif choice == '3':
                print("\nGoodbye!")
                self.db.close()
                break
            else:
                input("Invalid choice. Press Enter to continue...")

    def login(self):
        username = input("Enter username: ")
        user = self.db.get_user(username)
        if user:
            self.current_user = user
            self.main_menu()
        else:
            input("User not found. Press Enter to continue...")

    def register(self):
        username = input("Enter new username: ")
        if self.db.add_user(username):
            print("Registration successful!")
            input("Press Enter to continue...")
        else:
            input("Username already exists. Press Enter to continue...")

    def main_menu(self):
        while True:
            self.print_header()
            print("1. Manage Income")
            print("2. Manage Expenses")
            print("3. Budget Monitoring")
            print("4. Export Financial Report")
            print("5. Logout")
            choice = input("\nEnter your choice (1-5): ")

            if choice == '1':
                self.income_menu()
            elif choice == '2':
                self.expense_menu()
            elif choice == '3':
                self.budget_menu()
            elif choice == '4':
                self.export_financial_report()
            elif choice == '5':
                self.current_user = None
                break
            else:
                input("Invalid choice. Press Enter to continue...")

    def income_menu(self):
        while True:
            self.print_header()
            print("=== Income Management ===")
            print("1. Add Income")
            print("2. Edit Income")
            print("3. Delete Income")
            print("4. View Income Records")
            print("5. Back to Main Menu")
            choice = input("\nEnter your choice (1-5): ")

            if choice == '1':
                self.add_income()
            elif choice == '2':
                self.edit_income()
            elif choice == '3':
                self.delete_income()
            elif choice == '4':
                self.view_income_records()
            elif choice == '5':
                break
            else:
                input("Invalid choice. Press Enter to continue...")

    def add_income(self):
        self.print_header()
        print("=== Add Income ===\n")
        
        categories = self.db.get_income_categories()
        print("Income Categories:")
        for cat in categories:
            print(f"{cat[0]}. {cat[1]}")

        try:
            category_id = int(input("\nEnter category ID: "))
            amount = float(input("Enter amount: "))
            description = input("Enter description: ")

            self.db.add_income(self.current_user[0], category_id, amount, description)
            print("\nIncome added successfully!")
        except ValueError:
            print("\nInvalid input!")
        
        input("\nPress Enter to continue...")

    def edit_income(self):
        income_id = int(input("Enter income ID to edit: "))
        amount = float(input("Enter new amount: "))
        self.db.edit_income(income_id, amount)
        print("Income updated successfully!")
        input("\nPress Enter to continue...")

    def delete_income(self):
        income_id = int(input("Enter income ID to delete: "))
        self.db.delete_income(income_id)
        print("Income deleted successfully!")
        input("\nPress Enter to continue...")

    def view_income_records(self):
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        incomes = self.db.view_income_records(start_date, end_date)
        print("\nIncome Records:")
        for income in incomes:
            print(f"ID: {income[0]}, Source: {income[1]}, Category: {income[2]}, Amount: ${income[3]}, Date: {income[4]}")
        input("\nPress Enter to continue...")

    def expense_menu(self):
        while True:
            self.print_header()
            print("=== Expense Management ===")
            print("1. Add Expense")
            print("2. Edit Expense")
            print("3. Delete Expense")
            print("4. View Expenses by Category")
            print("5. Back to Main Menu")
            choice = input("\nEnter your choice (1-5): ")

            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.edit_expense()
            elif choice == '3':
                self.delete_expense()
            elif choice == '4':
                self.view_expenses_by_category()
            elif choice == '5':
                break
            else:
                input("Invalid choice. Press Enter to continue...")

    def add_expense(self):
        self.print_header()
        print("=== Add Expense ===\n")
        
        categories = self.db.get_expense_categories()
        print("Expense Categories:")
        for cat in categories:
            print(f"{cat[0]}. {cat[1]}")

        try:
            category_id = int(input("\nEnter category ID: "))
            amount = float(input("Enter amount: "))
            description = input("Enter description: ")

            self.db.add_expense(self.current_user[0], category_id, amount, description)
            print("\nExpense added successfully!")
        except ValueError:
            print("\nInvalid input!")
        
        input("\nPress Enter to continue...")

    def edit_expense(self):
        expense_id = int(input("Enter expense ID to edit: "))
        amount = float(input("Enter new amount: "))
        self.db.edit_expense(expense_id, amount)
        print("Expense updated successfully!")
        input("\nPress Enter to continue...")

    def delete_expense(self):
        expense_id = int(input("Enter expense ID to delete: "))
        self.db.delete_expense(expense_id)
        print("Expense deleted successfully!")
        input("\nPress Enter to continue...")

    def view_expenses_by_category(self):
        category = input("Enter category to view: ")
        expenses = self.db.view_expenses_by_category(category)
        print(f"\nExpenses for category '{category}':")
        for expense in expenses:
            print(f"Date: {expense[1]}, Amount: ${expense[2]}, Description: {expense[3]}")
        input("\nPress Enter to continue...")

    def budget_menu(self):
        while True:
            self.print_header()
            print("=== Budget Monitoring ===")
            print("1. Set Budget")
            print("2. View Budget Status")
            print("3. Back to Main Menu")
            choice = input("\nEnter your choice (1-3): ")

            if choice == '1':
                self.set_budget()
            elif choice == '2':
                self.view_budget_status()
            elif choice == '3':
                break
            else:
                input("Invalid choice. Press Enter to continue...")

    def set_budget(self):
        self.print_header()
        print("=== Set Budget ===\n")
        
        categories = self.db.get_expense_categories()
        print("Expense Categories:")
        for cat in categories:
            print(f"{cat[0]}. {cat[1]}")

        try:
            category_id = int(input("\nEnter category ID: "))
            amount = float(input("Enter budget amount: "))
            month = int(input("Enter month (1-12): "))
            year = int(input("Enter year: "))

            if 1 <= month <= 12 and year >= 2000:
                self.db.set_budget(self.current_user[0], category_id, amount, month, year)
                print("\nBudget set successfully!")
            else:
                print("\nInvalid month or year!")
        except ValueError:
            print("\nInvalid input!")
        
        input("\nPress Enter to continue...")

    def view_budget_status(self):
        budgets = self.db.view_budget_status(self.current_user[0])
        print("\nBudget Status:")
        for budget in budgets:
            print(f"Category: {budget[0]}, Limit: ${budget[1]}, Spent: ${budget[2]}")
        input("\nPress Enter to continue...")

    def export_financial_report(self):
        self.db.export_financial_report(self.current_user[0])
        print("Financial report exported to 'financial_report.csv'.")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    budget_tracker = BudgetTracker()
    budget_tracker.login_menu()

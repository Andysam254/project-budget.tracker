import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('budget.db')
        self.cursor = self.conn.cursor()
        self.setup_database()
        pass
    
    def delete_income(self, income_id):
        try:
            self.cursor.execute('DELETE FROM Income WHERE id = ?', (income_id,))
            self.conn.commit()
            print("Income deleted successfully.")
        except Exception as e:
            print(f"Error deleting income: {e}")
    def export_financial_report(self, user_id):
        try:
            with open('financial_report.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Type', 'Date', 'Amount', 'Category', 'Description/Source'])

                # Export income
                self.cursor.execute('''
                    SELECT source, date, amount, category FROM Income WHERE user_id = ?
                ''', (user_id,))
                for row in self.cursor.fetchall():
                    writer.writerow(['Income', row[1], row[2], row[3], row[0]])

                self.cursor.execute('''
                    SELECT category, date, amount, description FROM Expenses WHERE user_id = ?
                ''', (user_id,))
                for row in self.cursor.fetchall():
                    writer.writerow(['Expense', row[1], row[2], row[0], row[3]])

            print("Financial report successfully exported to 'financial_report.csv'.")
        except Exception as e:
            print(f"Error exporting financial report: {e}")
    def setup_database(self):
       
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS income_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS expense_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category_id INTEGER,
            amount DECIMAL(10,2) NOT NULL,
            description TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (category_id) REFERENCES income_categories (id)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category_id INTEGER,
            amount DECIMAL(10,2) NOT NULL,
            description TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (category_id) REFERENCES expense_categories (id)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category INTEGER,  -- The category of the budget
            limit_amount REAL,  -- The limit for this category
            month INTEGER,  -- Month of the budget
            year INTEGER,  -- Year of the budget
            FOREIGN KEY (user_id) REFERENCES Users(id),
            FOREIGN KEY (category) REFERENCES Categories(id)
        )
        ''')

        

        default_income_categories = ['Salary', 'Freelance', 'Investments', 'Other']
        default_expense_categories = ['Food', 'Transportation', 'Housing', 'Utilities', 'Entertainment', 'Healthcare', 'Other']

        for category in default_income_categories:
            self.cursor.execute('INSERT OR IGNORE INTO income_categories (name) VALUES (?)', (category,))

        for category in default_expense_categories:
            self.cursor.execute('INSERT OR IGNORE INTO expense_categories (name) VALUES (?)', (category,))

        self.conn.commit()
    def view_expenses_by_category(self, category):
        try:
            self.cursor.execute('''
                SELECT id, date, amount, description 
                FROM Expenses 
                WHERE category_id = ?
            ''', (category,))
            return self.cursor.fetchall() 
        except Exception as e:
            print(f"Error fetching expenses by category: {e}")
            return []

    def view_income_records(self):
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")

        incomes = self.db.view_income_records(start_date, end_date)

        print("\nIncome Records:")
        for income in incomes:
            print(f"ID: {income[0]}, Source: {income[1]}, Category: {income[2]}, Amount: ${income[3]}, Date: {income[4]}")
        
        input("\nPress Enter to continue...")

    def close(self):
        self.conn.close()

    def add_user(self, username):
        try:
            self.cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        pass

    def get_user(self, username):
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return self.cursor.fetchone()
        pass

    def add_income(self, user_id, category_id, amount, description):
        self.cursor.execute('''
        INSERT INTO income (user_id, category_id, amount, description)
        VALUES (?, ?, ?, ?)
        ''', (user_id, category_id, amount, description))
        self.conn.commit()
        pass
    def get_income_categories(self):
        self.cursor.execute('SELECT * FROM income_categories')
        return self.cursor.fetchall()
        pass
    def add_expense(self, user_id, category_id, amount, description):
        self.cursor.execute('''
        INSERT INTO expenses (user_id, category_id, amount, description)
        VALUES (?, ?, ?, ?)
        ''', (user_id, category_id, amount, description))
        self.conn.commit()
        pass
    def get_expense_categories(self):
        self.cursor.execute('SELECT * FROM expense_categories')
        return self.cursor.fetchall()
        pass 
    def set_budget(self, user_id, category_id, amount, month, year):
        try:
            self.cursor.execute('''
                INSERT INTO Budgets (user_id, category, limit_amount, month, year)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, category_id, amount, month, year))
            self.conn.commit()
        except Exception as e:
            print(f"Error setting budget: {e}")

    def view_budget_status(self, user_id):
        try:
            
            self.cursor.execute('''
                SELECT b.category, b.limit_amount, COALESCE(SUM(e.amount), 0) AS spent
                FROM Budgets b
                LEFT JOIN Expenses e ON b.category = e.category AND e.user_id = ?
                WHERE b.user_id = ?
                GROUP BY b.category
            ''', (user_id, user_id))

            return self.cursor.fetchall()  
        except Exception as e:
            print(f"Error fetching budget status: {e}")
            return []



    def get_budget(self, user_id, category_id, month, year):
        self.cursor.execute('''
        SELECT amount FROM budgets 
        WHERE user_id = ? AND category_id = ? AND month = ? AND year = ?
        ''', (user_id, category_id, month, year))
        return self.cursor.fetchone()
        pass 
    
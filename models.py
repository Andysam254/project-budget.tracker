import csv
from datetime import datetime

class FinanceManager:
    def __init__(self, db):
        self.db = db

    def add_income(self, user_id, category_id, amount, description, date=None):
        date = date or datetime.now()  
        self.db.cursor.execute(
            'INSERT INTO income (user_id, category_id, amount, description, date) VALUES (?, ?, ?, ?, ?)',
            (user_id, category_id, amount, description, date)
        )
        self.db.conn.commit()

    def edit_income(self, income_id, new_amount):
        self.db.cursor.execute(
            'UPDATE income SET amount = ? WHERE id = ?',
            (new_amount, income_id)
        )
        self.db.conn.commit()

    def delete_income(self, income_id):
        self.db.cursor.execute(
            'DELETE FROM income WHERE id = ?',
            (income_id,)
        )
        self.db.conn.commit()

    def view_income_records(self, user_id, start_date, end_date):
        self.db.cursor.execute(
            'SELECT id, category_id, amount, description, date FROM income WHERE user_id = ? AND date BETWEEN ? AND ?',
            (user_id, start_date, end_date)
        )
        return self.db.cursor.fetchall()

    def add_expense(self, user_id, category_id, amount, description, date=None):
        date = date or datetime.now()  
        self.db.cursor.execute(
            'INSERT INTO expenses (user_id, category_id, amount, description, date) VALUES (?, ?, ?, ?, ?)',
            (user_id, category_id, amount, description, date)
        )
        self.db.conn.commit()

    def edit_expense(self, expense_id, new_amount):
        self.db.cursor.execute(
            'UPDATE expenses SET amount = ? WHERE id = ?',
            (new_amount, expense_id)
        )
        self.db.conn.commit()

    def delete_expense(self, expense_id):
        self.db.cursor.execute(
            'DELETE FROM expenses WHERE id = ?',
            (expense_id,)
        )
        self.db.conn.commit()

    def view_expenses_by_category(self, user_id, category_id):
        self.db.cursor.execute(
            'SELECT id, date, amount, description FROM expenses WHERE user_id = ? AND category_id = ?',
            (user_id, category_id)
        )
        return self.db.cursor.fetchall()

    def view_budget_status(self, user_id):
        self.db.cursor.execute('''
            SELECT b.category_id, b.amount as budget_amount, 
                   COALESCE(SUM(e.amount), 0) as spent
            FROM budgets b
            LEFT JOIN expenses e ON b.category_id = e.category_id AND b.user_id = e.user_id
            WHERE b.user_id = ?
            GROUP BY b.category_id
        ''', (user_id,))
        return self.db.cursor.fetchall()
    
    def set_budget(self, user_id, category_id, amount, month, year):
        self.db.cursor.execute(
            'INSERT OR REPLACE INTO budgets (user_id, category_id, amount, month, year) VALUES (?, ?, ?, ?, ?)',
            (user_id, category_id, amount, month, year)
        )
        self.db.conn.commit()
    def export_financial_report(self, user_id):
        with open(f'{user_id}_financial_report.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Type', 'Date', 'Amount', 'Category', 'Description'])

            self.db.cursor.execute('SELECT category_id, date, amount, description FROM income WHERE user_id = ?', (user_id,))
            for row in self.db.cursor.fetchall():
                writer.writerow(['Income', row[1], row[2], row[0], row[3]])

            self.db.cursor.execute('SELECT category_id, date, amount, description FROM expenses WHERE user_id = ?', (user_id,))
            for row in self.db.cursor.fetchall():
                writer.writerow(['Expense', row[1], row[2], row[0], row[3]])

from database import Database
import csv
from datetime import datetime

class FinanceManager:
    def __init__(self, db):
        self.db = db

    def add_income(self, source, amount):
        date = datetime.now().strftime('%Y-%m-%d')
        self.db.cursor.execute(
            'INSERT INTO income (date, source, amount) VALUES (?, ?, ?)',
            (date, source, amount)
        )
        self.db.conn.commit()

    def add_expense(self, amount, description, category):
        date = datetime.now().strftime('%Y-%m-%d')
        self.db.cursor.execute(
            'INSERT INTO expenses (date, amount, description, category) VALUES (?, ?, ?, ?)',
            (date, amount, description, category)
        )
        self.db.conn.commit()

    def set_budget(self, category, limit_amount):
        self.db.cursor.execute(
            'INSERT OR REPLACE INTO budgets (category, limit_amount) VALUES (?, ?)',
            (category, limit_amount)
        )
        self.db.conn.commit()

    def get_expenses_by_category(self, category):
        self.db.cursor.execute(
            'SELECT * FROM expenses WHERE category = ?', (category,)
        )
        return self.db.cursor.fetchall()

    def export_financial_report(self):
        with open('financial_report.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Type', 'Date', 'Amount', 'Category/Source', 'Description'])
            
            # Export income
            self.db.cursor.execute('SELECT * FROM income')
            for row in self.db.cursor.fetchall():
                writer.writerow(['Income', row[1], row[3], row[2], ''])
            
            # Export expenses
            self.db.cursor.execute('SELECT * FROM expenses')
            for row in self.db.cursor.fetchall():
                writer.writerow(['Expense', row[1], row[2], row[4], row[3]])

class CourseManager:
    def __init__(self, db):
        self.db = db

    def add_instructor(self, name, email):
        self.db.cursor.execute(
            'INSERT INTO instructors (name, email) VALUES (?, ?)',
            (name, email)
        )
        self.db.conn.commit()

    def add_course(self, name, instructor_id):
        self.db.cursor.execute(
            'INSERT INTO courses (name, instructor_id) VALUES (?, ?)',
            (name, instructor_id)
        )
        self.db.conn.commit()

    def enroll_student(self, name, email, course_id):
        self.db.cursor.execute(
            'INSERT INTO students (name, email, course_id) VALUES (?, ?, ?)',
            (name, email, course_id)
        )
        self.db.conn.commit()

    def get_course_enrollment(self, course_id):
        self.db.cursor.execute('''
            SELECT s.name, s.email, c.name as course_name, i.name as instructor_name
            FROM students s
            JOIN courses c ON s.course_id = c.id
            JOIN instructors i ON c.instructor_id = i.id
            WHERE c.id = ?
        ''', (course_id,))
        return self.db.cursor.fetchall()
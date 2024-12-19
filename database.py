import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('education.db')
        self.cursor = self.conn.cursor()
        self.setup_database()

    def setup_database(self):
        # Create tables
        self.cursor.executescript
        ('''
            CREATE TABLE IF NOT EXISTS instructors (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE
            );

            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                instructor_id INTEGER,
                FOREIGN KEY (instructor_id) REFERENCES instructors (id)
            );

            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                course_id INTEGER,
                FOREIGN KEY (course_id) REFERENCES courses (id)
            );

            CREATE TABLE IF NOT EXISTS income (
                id INTEGER PRIMARY KEY,
                date TEXT NOT NULL,
                source TEXT NOT NULL,
                amount REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                category TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY,
                category TEXT UNIQUE NOT NULL,
                limit_amount REAL NOT NULL
            );
        ''')
        self.conn.commit()

    def close(self):
        self.conn.close()
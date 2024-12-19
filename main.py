from database import Database
from models import FinanceManager, CourseManager

def print_menu():
    print("\n=== Educational Management System ===")
    print("1. Finance Management")
    print("2. Course Management")
    print("3. Export Reports")
    print("4. Exit")

def finance_menu():
    print("\n=== Finance Management ===")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. Set Budget")
    print("4. View Expenses by Category")
    print("5. Back to Main Menu")

def course_menu():
    print("\n=== Course Management ===")
    print("1. Add Instructor")
    print("2. Add Course")
    print("3. Enroll Student")
    print("4. View Course Enrollment")
    print("5. Back to Main Menu")

def main():
    db = Database()
    finance_manager = FinanceManager(db)
    course_manager = CourseManager(db)

    while True:
        print_menu()
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            while True:
                finance_menu()
                subchoice = input("Enter your choice (1-5): ")

                if subchoice == '1':
                    source = input("Enter income source: ")
                    amount = float(input("Enter amount: "))
                    finance_manager.add_income(source, amount)
                    print("Income added successfully!")

                elif subchoice == '2':
                    amount = float(input("Enter amount: "))
                    description = input("Enter description: ")
                    category = input("Enter category: ")
                    finance_manager.add_expense(amount, description, category)
                    print("Expense added successfully!")

                elif subchoice == '3':
                    category = input("Enter category: ")
                    limit = float(input("Enter budget limit: "))
                    finance_manager.set_budget(category, limit)
                    print("Budget set successfully!")

                elif subchoice == '4':
                    category = input("Enter category to view: ")
                    expenses = finance_manager.get_expenses_by_category(category)
                    print(f"\nExpenses for category '{category}':")
                    for expense in expenses:
                        print(f"Date: {expense[1]}, Amount: ${expense[2]}, Description: {expense[3]}")

                elif subchoice == '5':
                    break

        elif choice == '2':
            while True:
                course_menu()
                subchoice = input("Enter your choice (1-5): ")

                if subchoice == '1':
                    name = input("Enter instructor name: ")
                    email = input("Enter instructor email: ")
                    course_manager.add_instructor(name, email)
                    print("Instructor added successfully!")

                elif subchoice == '2':
                    name = input("Enter course name: ")
                    instructor_id = int(input("Enter instructor ID: "))
                    course_manager.add_course(name, instructor_id)
                    print("Course added successfully!")

                elif subchoice == '3':
                    name = input("Enter student name: ")
                    email = input("Enter student email: ")
                    course_id = int(input("Enter course ID: "))
                    course_manager.enroll_student(name, email, course_id)
                    print("Student enrolled successfully!")

                elif subchoice == '4':
                    course_id = int(input("Enter course ID: "))
                    enrollments = course_manager.get_course_enrollment(course_id)
                    print("\nCourse Enrollment:")
                    for enrollment in enrollments:
                        print(f"Student: {enrollment[0]}, Email: {enrollment[1]}")
                        print(f"Course: {enrollment[2]}, Instructor: {enrollment[3]}\n")

                elif subchoice == '5':
                    break

        elif choice == '3':
            finance_manager.export_financial_report()
            print("Financial report exported to 'financial_report.csv'")

        elif choice == '4':
            db.close()
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
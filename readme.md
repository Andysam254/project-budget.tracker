# Budget Tracker Project Idea (CLI with Python)

## Description
The Budget Tracker is a streamlined financial management tool tailored to meet the needs of individual users or small organizations. It empowers users to monitor their income and expenses, set financial goals, and maintain control over their budgets. The system emphasizes simplicity, ease of use, and effective visualization of financial data. By categorizing transactions and providing budget monitoring tools, it enables users to achieve financial clarity and make informed decisions.

---

## Problem Statement
Managing personal or organizational finances can be overwhelming without a structured approach. Common challenges include:
- Difficulty in tracking income sources and expenses.
- Inefficient manual record-keeping leading to errors.
- Lack of visibility into category-specific spending habits.
- Overspending due to the absence of budget limits or alerts.
- Inability to generate useful financial insights from raw data.

---

## Proposed Solution
The Budget Tracker addresses these challenges by offering:
- **Income and Expense Tracking**: Record and categorize all transactions with detailed descriptions.
- **Budget Monitoring**: Set limits for specific categories and receive notifications when limits are exceeded.
- **Financial Insights**: Generate reports summarizing income and expenses, and visualize data through charts.
- **Data Export**: Export financial records to a CSV file for offline storage or advanced analysis.
- **User-Friendly Design**: Simple interface designed for individuals and small organizations, making it intuitive and effective.
- **Offline Functionality**: Ensures usability without reliance on an internet connection.

---

## Table Relationships

### Income Categories:
- **Relationship**: One-to-Many
- **Description**: Each income record belongs to a single category, but a category can have multiple income records.
- **Implementation**: An income_category_id in the Income table references the IncomeCategories table.

### Future Enhancements

Add a graphical user interface (GUI) for ease of use.

Implement data visualization for better financial insights.

Add a notification system for budget thresholds.

### License

This project is licensed under the MIT License. See the LICENSE file for details.
Project MVP/User Stories A user:

    As a user, I want to add income records with categories to understand my sources of revenue.
    As a user, I want to edit income records to correct mistakes.
    As a user, I want to delete outdated or incorrect income entries.
    As a user, I want to view a list of all income records within a specific time frame.

Technologies Used 
-Python
-CLI
React Bootstrap


Slides Link :https://docs.google.com/presentation/d/1tuIoyzBIpypRqbtFn4FNZKhnrHfmOGdw0Rd_b9gqb3s/edit#slide=id.g5f461a8324_0_566

import sqlite3
from datetime import datetime

# Categories
income_categories = ['Salary', 'Freelance', 'Investments', 'Gifts', 'Rental Income', 'Other']
expense_categories = ['Food', 'Rent/Mortgage', 'Utilities', 'Transportation', 'Healthcare', 'Entertainment',
                      'Education', 'Clothing', 'Personal Care', 'Insurance', 'Savings', 'Debt Payments',
                      'Gifts & Donations', 'Household Supplies', 'Miscellaneous']

# Database setup functions
def create_connection():
    conn = sqlite3.connect('budget_tracker.db')
    return conn

def create_table(conn):
    sql_create_transactions_table = """ CREATE TABLE IF NOT EXISTS transactions (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        date TEXT NOT NULL,
                                        category TEXT NOT NULL,
                                        description TEXT,
                                        amount REAL NOT NULL,
                                        type TEXT NOT NULL
                                    ); """
    try:
        c = conn.cursor()
        c.execute(sql_create_transactions_table)
    except Exception as e:
        print(e)

# Operations
def add_transaction(conn, transaction):
    sql = ''' INSERT INTO transactions(date, category, description, amount, type)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, transaction)
    conn.commit()
    return cur.lastrowid

def update_transaction(conn, transaction):
    sql = ''' UPDATE transactions
              SET date = ? ,
                  category = ? ,
                  description = ? ,
                  amount = ? ,
                  type = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, transaction)
    conn.commit()

def delete_transaction(conn, id):
    sql = 'DELETE FROM transactions WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

def select_all_transactions(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions")
    rows = cur.fetchall()
    for row in rows:
        print(row)

def select_transactions_by_type(conn, type):
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions WHERE type=?", (type,))
    rows = cur.fetchall()
    for row in rows:
        print(row)

def generate_summary_report(conn):
    cur = conn.cursor()
    cur.execute("SELECT type, SUM(amount) FROM transactions GROUP BY type")
    rows = cur.fetchall()
    for row in rows:
        print(f"{row[0]}: {row[1]}")

def calculate_balance(conn):
    cur = conn.cursor()
    cur.execute("SELECT SUM(amount) FROM transactions WHERE type='income'")
    total_income = cur.fetchone()[0]
    cur.execute("SELECT SUM(amount) FROM transactions WHERE type='expense'")
    total_expense = cur.fetchone()[0]
    if total_income:
        total_income = total_income
    else:
        total_income = 0
    if total_expense:
        total_expense = total_expense
    else:
        total_expense = 0
    balance = total_income - total_expense
    return balance

# Interface
def main():
    conn = create_connection()
    create_table(conn)

    while True:
        print("\nBudget Tracker")
        print("1. Add Transaction")
        print("2. Update Transaction")
        print("3. Delete Transaction")
        print("4. View All Transactions")
        print("5. View Transactions by Type")
        print("6. Generate Summary Report")
        print("7. Calculate Current Balance")
        print("8. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ")
            trans_type = input("Enter type (income/expense): ")
            if trans_type == 'income':
                print("Select category:")
                for i, category in enumerate(income_categories, 1):
                    print(f"{i}. {category}")
                category_choice = int(input("Enter choice: "))
                category = income_categories[category_choice - 1]
            elif trans_type == 'expense':
                print("Select category:")
                for i, category in enumerate(expense_categories, 1):
                    print(f"{i}. {category}")
                category_choice = int(input("Enter choice: "))
                category = expense_categories[category_choice - 1]
            else:
                print("Invalid type. Please try again.")
                continue

            description = input("Enter description: ")
            amount = float(input("Enter amount: "))
            transaction = (date, category, description, amount, trans_type)
            add_transaction(conn, transaction)

        elif choice == '2':
            id = int(input("Enter transaction ID: "))
            date = input("Enter date (YYYY-MM-DD): ")
            trans_type = input("Enter type (income/expense): ")
            if trans_type == 'income':
                print("Select category:")
                for i, category in enumerate(income_categories, 1):
                    print(f"{i}. {category}")
                category_choice = int(input("Enter choice: "))
                category = income_categories[category_choice - 1]
            elif trans_type == 'expense':
                print("Select category:")
                for i, category in enumerate(expense_categories, 1):
                    print(f"{i}. {category}")
                category_choice = int(input("Enter choice: "))
                category = expense_categories[category_choice - 1]
            else:
                print("Invalid type. Please try again.")
                continue

            description = input("Enter description: ")
            amount = float(input("Enter amount: "))
            transaction = (date, category, description, amount, trans_type, id)
            update_transaction(conn, transaction)

        elif choice == '3':
            id = int(input("Enter transaction ID: "))
            delete_transaction(conn, id)

        elif choice == '4':
            select_all_transactions(conn)

        elif choice == '5':
            trans_type = input("Enter type (income/expense): ")
            select_transactions_by_type(conn, trans_type)

        elif choice == '6':
            generate_summary_report(conn)

        elif choice == '7':
            balance = calculate_balance(conn)
            print(f"Current Balance: {balance}")

        elif choice == '8':
            conn.close()
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()

import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

print("Database connected successfully!")


def get_amount():
    while True:
        try:
            amount = float(input("Enter amount: "))
            return amount
        except ValueError:
            print("Please enter a valid amount.")
 
def get_date():
    while True:
        try:
            date_of = input("Enter date (YYYY-MM-DD): ")
            datetime.strptime(date_of, "%Y-%m-%d")
            return date_of
        except ValueError:
            print("Please enter a valid date.")

def add_expense():
    category = input("Enter category: ")

    amount = get_amount()
    date_of = get_date()
    cursor = connection.cursor()

    query = """
    INSERT INTO expenses (category, amount, date_of)
    VALUES (%s, %s, %s)
    """

    values = (category, amount, date_of)
    try:
        cursor.execute(query, values)
        connection.commit()
        print("Expense added successfully!")

    except mysql.connector.Error as err:
        connection.rollback()
        print("Database error:", err)
    print("Expense added successfully!")


def view_expenses():
    cursor = connection.cursor()

    query = "SELECT * FROM expenses"
    cursor.execute(query)

    rows = cursor.fetchall()

    print("\nID | Category | Amount | Date")
    print("--------------------------------------------")

    for row in rows:
        print(
            f"ID: {row[0]} | Category: {row[1]} | "
            f"Amount: {row[2]} | Date: {row[3]}"
        )


def delete_expense():
    expense_id = input("Enter expense ID to delete: ")

    cursor = connection.cursor()

    query = "DELETE FROM expenses WHERE id = %s"
    values = (expense_id,)

    cursor.execute(query, values)

    print("Rows affected:", cursor.rowcount)

    if cursor.rowcount == 1:
        connection.commit()
        print("Expense deleted successfully!")
    else:
        connection.rollback()
        print("Expense not found!")


def update_expense():
    expense_id = input("Enter expense ID to update: ")

    category = input("Enter new category: ")

    amount = get_amount()

    date_of = get_date()

    cursor = connection.cursor()

    query = """
    UPDATE expenses
    SET category = %s,
        amount = %s,
        date_of = %s
    WHERE id = %s
    """

    values = (category, amount, date_of, expense_id)

    cursor.execute(query, values)

    if cursor.rowcount == 1:
        connection.commit()
        print("Expense updated successfully!")
    else:
        connection.rollback()
        print("Expense not found!")


def main():
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Update Expense")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            delete_expense()

        elif choice == "4":
            update_expense()

        elif choice == "5":
            print("Thank you for using Expense Tracker!")
            break

        else:
            print("Invalid choice. Please try again.")


main()
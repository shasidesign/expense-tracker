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


# =========================
# VALIDATION
# =========================

def get_amount():
    while True:
        try:
            amount = float(input("Enter amount: "))

            if amount <= 0:
                print("Amount must be greater than 0.")
                continue

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


# =========================
# ADD
# =========================

def add_expense():
    category = input("Enter category: ")
    amount = get_amount()
    date_of = get_date()

    cursor = connection.cursor()

    query = """
    INSERT INTO expenses (category, amount, date_of)
    VALUES (%s, %s, %s)
    """

    try:
        cursor.execute(query, (category, amount, date_of))
        connection.commit()
        print("Expense added successfully!")

    except mysql.connector.Error as err:
        connection.rollback()
        print("Database error:", err)

    finally:
        cursor.close()


# =========================
# VIEW
# =========================

def view_expenses():
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, category, amount, date_of
        FROM expenses
        ORDER BY date_of DESC, id DESC
    """)

    rows = cursor.fetchall()

    if not rows:
        print("\nNo expenses found.")
    else:
        print("\n========== EXPENSES ==========")

        for row in rows:
            print(
                f"ID: {row[0]} | "
                f"Category: {row[1]} | "
                f"Amount: ₹{row[2]:.2f} | "
                f"Date: {row[3]}"
            )

    cursor.close()


# =========================
# UPDATE
# =========================

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

    try:
        cursor.execute(
            query,
            (category, amount, date_of, expense_id)
        )

        if cursor.rowcount == 1:
            connection.commit()
            print("Expense updated successfully!")
        else:
            connection.rollback()
            print("Expense not found!")

    except mysql.connector.Error as err:
        connection.rollback()
        print("Database error:", err)

    finally:
        cursor.close()


# =========================
# DELETE
# =========================

def delete_expense():
    expense_id = input("Enter expense ID to delete: ")

    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM expenses WHERE id = %s",
            (expense_id,)
        )

        if cursor.rowcount == 1:
            connection.commit()
            print("Expense deleted successfully!")
        else:
            connection.rollback()
            print("Expense not found!")

    except mysql.connector.Error as err:
        connection.rollback()
        print("Database error:", err)

    finally:
        cursor.close()


# =========================
# TOTAL
# =========================

def total_spending():
    cursor = connection.cursor()

    cursor.execute("SELECT SUM(amount) FROM expenses")

    result = cursor.fetchone()
    total = result[0] or 0

    print(f"\nTotal spending: ₹{total:.2f}")

    cursor.close()


# =========================
# COUNT
# =========================

def count_expenses():
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM expenses")

    result = cursor.fetchone()

    print(f"\nNumber of expenses: {result[0]}")

    cursor.close()


# =========================
# CATEGORY SUMMARY
# =========================

def category_summary():
    cursor = connection.cursor()

    query = """
    SELECT category, SUM(amount)
    FROM expenses
    GROUP BY category
    ORDER BY SUM(amount) DESC
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    print("\n========== CATEGORY SUMMARY ==========")

    if not rows:
        print("No expenses found.")
    else:
        for row in rows:
            print(f"{row[0]}: ₹{row[1]:.2f}")

    cursor.close()


# =========================
# STATISTICS
# =========================

def expense_statistics():
    cursor = connection.cursor()

    query = """
    SELECT
        AVG(amount),
        MAX(amount),
        MIN(amount)
    FROM expenses
    """

    cursor.execute(query)

    result = cursor.fetchone()

    average = result[0] or 0
    highest = result[1] or 0
    lowest = result[2] or 0

    print("\n========== STATISTICS ==========")
    print(f"Average expense: ₹{average:.2f}")
    print(f"Highest expense: ₹{highest:.2f}")
    print(f"Lowest expense: ₹{lowest:.2f}")

    cursor.close()


# =========================
# SEARCH CATEGORY
# =========================

def search_by_category():
    category = input("Enter category: ")

    cursor = connection.cursor()

    query = """
    SELECT id, category, amount, date_of
    FROM expenses
    WHERE category = %s
    """

    cursor.execute(query, (category,))

    rows = cursor.fetchall()

    print("\n========== SEARCH RESULTS ==========")

    if not rows:
        print("No expenses found.")
    else:
        for row in rows:
            print(
                f"ID: {row[0]} | "
                f"Category: {row[1]} | "
                f"Amount: ₹{row[2]:.2f} | "
                f"Date: {row[3]}"
            )

    cursor.close()


# =========================
# SEARCH AMOUNT
# =========================

def search_by_amount():
    amount = get_amount()

    cursor = connection.cursor()

    query = """
    SELECT id, category, amount, date_of
    FROM expenses
    WHERE amount >= %s
    ORDER BY amount DESC
    """

    cursor.execute(query, (amount,))

    rows = cursor.fetchall()

    print("\n========== AMOUNT SEARCH ==========")

    if not rows:
        print("No expenses found.")
    else:
        for row in rows:
            print(
                f"ID: {row[0]} | "
                f"Category: {row[1]} | "
                f"Amount: ₹{row[2]:.2f} | "
                f"Date: {row[3]}"
            )

    cursor.close()


# =========================
# SEARCH DATE
# =========================

def search_by_date():
    date_of = get_date()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, category, amount, date_of
        FROM expenses
        WHERE date_of = %s
        """,
        (date_of,)
    )

    rows = cursor.fetchall()

    print("\n========== DATE SEARCH ==========")

    if not rows:
        print("No expenses found.")
    else:
        for row in rows:
            print(
                f"ID: {row[0]} | "
                f"Category: {row[1]} | "
                f"Amount: ₹{row[2]:.2f} | "
                f"Date: {row[3]}"
            )

    cursor.close()


# =========================
# RECENT
# =========================

def recent_expenses():
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, category, amount, date_of
        FROM expenses
        ORDER BY date_of DESC, id DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()

    print("\n========== RECENT EXPENSES ==========")

    if not rows:
        print("No expenses found.")
    else:
        for row in rows:
            print(
                f"ID: {row[0]} | "
                f"Category: {row[1]} | "
                f"Amount: ₹{row[2]:.2f} | "
                f"Date: {row[3]}"
            )

    cursor.close()


# =========================
# MONTHLY REPORT
# =========================

def monthly_report():
    year = input("Enter year (YYYY): ")

    while True:
        try:
            month = int(input("Enter month (1-12): "))

            if 1 <= month <= 12:
                break

            print("Month must be between 1 and 12.")

        except ValueError:
            print("Please enter a valid month.")

    cursor = connection.cursor()

    query = """
    SELECT
        COUNT(*),
        SUM(amount),
        AVG(amount),
        MAX(amount),
        MIN(amount)
    FROM expenses
    WHERE YEAR(date_of) = %s
      AND MONTH(date_of) = %s
    """

    cursor.execute(query, (year, month))

    result = cursor.fetchone()

    count = result[0]
    total = result[1] or 0
    average = result[2] or 0
    highest = result[3] or 0
    lowest = result[4] or 0

    print("\n========== MONTHLY REPORT ==========")
    print(f"Month: {year}-{month:02d}")
    print(f"Number of expenses: {count}")
    print(f"Total spending: ₹{total:.2f}")
    print(f"Average expense: ₹{average:.2f}")
    print(f"Highest expense: ₹{highest:.2f}")
    print(f"Lowest expense: ₹{lowest:.2f}")

    cursor.close()


# =========================
# SET BUDGET
# =========================

def set_budget():
    year = input("Enter year (YYYY): ")

    while True:
        try:
            month = int(input("Enter month (1-12): "))

            if 1 <= month <= 12:
                break

            print("Month must be between 1 and 12.")

        except ValueError:
            print("Please enter a valid month.")

    amount = get_amount()

    cursor = connection.cursor()

    query = """
    INSERT INTO budget (year, month, amount)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE amount = %s
    """

    cursor.execute(
        query,
        (year, month, amount, amount)
    )

    connection.commit()

    print(
        f"Budget set for {year}-{month:02d}: "
        f"₹{amount:.2f}"
    )

    cursor.close()


# =========================
# BUDGET STATUS
# =========================

def budget_status():
    year = input("Enter year (YYYY): ")

    while True:
        try:
            month = int(input("Enter month (1-12): "))

            if 1 <= month <= 12:
                break

            print("Month must be between 1 and 12.")

        except ValueError:
            print("Please enter a valid month.")

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT amount
        FROM budget
        WHERE year = %s AND month = %s
        """,
        (year, month)
    )

    result = cursor.fetchone()

    if result is None:
        print("No budget set for this month.")
        cursor.close()
        return

    budget = result[0]

    cursor.execute(
        """
        SELECT SUM(amount)
        FROM expenses
        WHERE YEAR(date_of) = %s
          AND MONTH(date_of) = %s
        """,
        (year, month)
    )

    result = cursor.fetchone()

    spent = result[0] or 0
    remaining = budget - spent

    print("\n========== BUDGET STATUS ==========")
    print(f"Month: {year}-{month:02d}")
    print(f"Budget: ₹{budget:.2f}")
    print(f"Spent: ₹{spent:.2f}")
    print(f"Remaining: ₹{remaining:.2f}")

    if remaining < 0:
        print("⚠️ Budget exceeded!")
    elif remaining == 0:
        print("⚠️ Budget completely used!")
    else:
        print("✅ You are within budget.")

    cursor.close()


# =========================
# MAIN
# =========================

def main():
    while True:

        print("\n================================")
        print("        EXPENSE TRACKER")
        print("================================")
        print("1.  Add Expense")
        print("2.  View Expenses")
        print("3.  Delete Expense")
        print("4.  Update Expense")
        print("5.  Total Spending")
        print("6.  Count Expenses")
        print("7.  Category Summary")
        print("8.  Expense Statistics")
        print("9.  Search by Category")
        print("10. Search by Amount")
        print("11. Search by Date")
        print("12. Recent Expenses")
        print("13. Monthly Report")
        print("14. Set Monthly Budget")
        print("15. Budget Status")
        print("16. Exit")

        choice = input("\nEnter your choice (1-16): ")

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            delete_expense()

        elif choice == "4":
            update_expense()

        elif choice == "5":
            total_spending()

        elif choice == "6":
            count_expenses()

        elif choice == "7":
            category_summary()

        elif choice == "8":
            expense_statistics()

        elif choice == "9":
            search_by_category()

        elif choice == "10":
            search_by_amount()

        elif choice == "11":
            search_by_date()

        elif choice == "12":
            recent_expenses()

        elif choice == "13":
            monthly_report()

        elif choice == "14":
            set_budget()

        elif choice == "15":
            budget_status()

        elif choice == "16":
            print("Thank you for using Expense Tracker!")
            break

        else:
            print("Invalid choice. Please try again.")


main()
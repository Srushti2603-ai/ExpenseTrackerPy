import sys
import os

# Set encoding to UTF-8 (Fix for Windows console output)
sys.stdout.reconfigure(encoding='utf-8')

from expense import Expense  # Assuming Expense class is defined in expense.py
import os  # For file existence check

def main():
    print(f"Running Expense Tracker!")
    expense_file_path = "expenses.csv"
    budget = 20000

    # Input user for expense
    expense = get_user_expense()  # Removed invalid comment

    # Write expense to file
    save_expense(expense, expense_file_path)

    # Read file and summarize the expenses
    summarize_expenses(expense_file_path, budget)

def get_user_expense():
    print(f"🪂 Getting User Expense")
    expense_name = input("Enter expense name: ")

    while True:
        try:
            expense_amount = float(input("Enter expense amount: "))
            break
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

    print(f"You've entered {expense_name}, {expense_amount}")

    expense_category = [
        "🍕_FOOD", "💸_SAVING", "🪼_FUN", "✈️_BIKE", "💃🏻_CLOTHES", "🤕_AMOUNT_TO_PAY"
    ]

    while True:
        for i, category_name in enumerate(expense_category, 1):
            print(f"{i}. {category_name}")

        selected_index = input(f"Enter a category number [1 - {len(expense_category)}]: ")

        if selected_index.isdigit() and 1 <= int(selected_index) <= len(expense_category):
            selected_category = expense_category[int(selected_index) - 1]
            return Expense(name=expense_name, category=selected_category, amount=expense_amount)

        print("Invalid selection. Try again.")

def save_expense(expense: Expense, expense_file_path):
    print(f"🪂 Saving User Expense: {expense} to {expense_file_path}")
    try:
        with open(expense_file_path, "a", encoding="utf-8") as f:
            f.write(f"{expense.name},{expense.amount},{expense.category}\n")
    except Exception as e:
        print(f"⚠️ Error saving expense: {e}")

def summarize_expenses(expense_file_path, budget):
    print(f"🪂 Summarizing User Expense")

    # Check if file exists before reading
    if not os.path.exists(expense_file_path):
        print("⚠️ No expenses found yet.")
        return

    expenses = []
    try:
        with open(expense_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            stripped_line = line.strip()
            if not stripped_line or stripped_line.count(",") != 2:
                print(f"⚠️ Skipping invalid line: {line}")
                continue

            try:
                expense_name, expense_amount, expense_category = stripped_line.split(",")
                expenses.append(Expense(name=expense_name, amount=float(expense_amount), category=expense_category))
            except ValueError:
                print(f"⚠️ Error processing line: {line}")

    except Exception as e:
        print(f"⚠️ Error reading file: {e}")
        return

    amount_by_category = {}
    for expense in expenses:
        amount_by_category[expense.category] = amount_by_category.get(expense.category, 0) + expense.amount

    print("Expenses By Category:")
    for key, amount in amount_by_category.items():
        print(f"{key}: {amount:.2f}")

    total_spent = sum(exp.amount for exp in expenses)
    print(f"You've spent {total_spent:.2f} this month!")

    remaining_budget = budget - total_spent
    print(green(f"Budget remaining: {remaining_budget:.2f}"))  # Fixed green() call

def green(text):
    return f"\033[92m{text}\033[0m"

if __name__ == "__main__":
    main()
